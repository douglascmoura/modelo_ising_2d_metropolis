import streamlit as st
import numpy as np
from numba import njit
import time

# =====================================================================
# FUNÇÃO AUXILIAR: FORMATAÇÃO PT-BR 
# =====================================================================
def formatar_ptbr(valor, casas=2, inteiro=False):
    """
    Converte valores numéricos para o padrão PT-BR (ex: 1.234.567,89).
    Utiliza str.translate para performance O(n) na manipulação da string.
    """
    if inteiro:
        # Formata com vírgula nos milhares e depois troca por ponto
        return f"{int(valor):,}".replace(",", ".")
    
    # Formata float com as casas decimais e inverte ponto/vírgula
    texto = f"{valor:,.{casas}f}"
    return texto.translate(str.maketrans(",.", ".,"))

# =====================================================================
# CONFIGURAÇÃO DA PÁGINA E INJEÇÃO DE CSS
# =====================================================================
st.set_page_config(page_title="DOCHMO - Ising", layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }
        h1 {
            font-size: 2.5rem !important;
            margin-bottom: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# MOTOR COMPUTACIONAL DE ALTA PERFORMANCE (JIT COMPILED)
# =====================================================================
# O decorador @njit traduz esta função para código de máquina.
# Isso elimina o Global Interpreter Lock (GIL) e o overhead do Python,
# permitindo milhões de iterações por segundo.
@njit
def metropolis_hastings_step(grid: np.ndarray, beta: float, n_steps: int) -> np.ndarray:
    n = grid.shape[0]
    for _ in range(n_steps):
        # Seleção aleatória rápida
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        
        # Condição de contorno periódica usando módulo escalar (muito mais rápido que ifelse)
        i_top = (i - 1) % n
        i_bottom = (i + 1) % n
        j_left = (j - 1) % n
        j_right = (j + 1) % n
        
        # Soma dos vizinhos
        soma_vizinhos = (
            grid[i_top, j] + 
            grid[i_bottom, j] + 
            grid[i, j_left] + 
            grid[i, j_right]
        )
        
        # Variação de energia (ΔE)
        de = 2 * grid[i, j] * soma_vizinhos
        
        # Regra de Aceitação de Metropolis
        if de <= 0 or np.random.rand() < np.exp(-beta * de):
            grid[i, j] *= -1 # Inverte o spin invertendo o sinal
            
    return grid

# =====================================================================
# RENDERIZAÇÃO MATRICIAL DIRETA 
# =====================================================================
def render_grid_to_rgb(grid: np.ndarray) -> np.ndarray:
    """
    Converte a matriz de spins (-1, 1) em uma matriz RGB (H, W, 3)
    para plotagem em tempo real, sem overhead de bibliotecas gráficas.
    """
    # Cria uma matriz 3D vazia do tipo uint8 (padrão de imagem)
    rgb_img = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
    
    # Aplica cores vetorialmente (Vermelho para +1, Azul para -1)
    rgb_img[grid == 1] = [220, 50, 47]   
    rgb_img[grid == -1] = [38, 139, 210] 
    return rgb_img

# =====================================================================
# INTERFACE E LÓGICA DO DASHBOARD
# =====================================================================
def main():
    st.title("⚛️ Modelo de Ising: Dinâmica Termodinâmica")
    st.markdown("""
    Esta aplicação utiliza **MCMC (Metropolis-Hastings)** compilado via `Numba` para simular o ferromagnetismo.
            Ajuste os parâmetros na barra lateral e clique em **Iniciar Simulação** para observar a evolução dos domínios magnéticos.
    """)

    # --- BARRA LATERAL (CONTROLES) ---
    with st.sidebar:
        # INJEÇÃO NATIVA DA IDENTIDADE DO PROJETO
        st.markdown(
            """
            <h2 style="font-family: 'Times New Roman', serif; color: #E54344;">DOUGLAS MOURA</h2>
            <hr style="border: 1px solid #222222; margin-top: 1px; margin-bottom: 15px;">
            """, 
            unsafe_allow_html=True
        )

        st.header("Parâmetros do Sistema")
        
        # Beta crítico teórico para grade 2D é ~0.44 (onde ocorre a transição de fase)
        beta = st.slider("Beta (1/kT) - Inverso da Temperatura:", 
                         min_value=0.0, max_value=3.0, value=0.44, step=0.01,
                         help="Beta alto = Baixa Temp (Ordem). Beta baixo = Alta Temp (Caos). Beta Crítico ≈ 0.44")
        
        n_size = st.slider("Tamanho da Grade (N x N):", 
                           min_value=50, max_value=500, value=150, step=50)
        
        total_iteracoes = st.number_input("Total de Iterações:", 
                                          min_value=100_000, max_value=5_000_000, value=1_000_000, step=100_000)
        
        fps_update = st.slider("Quadros de Atualização (Frames):", 
                               min_value=10, max_value=200, value=50,
                               help="Quantas vezes a tela será atualizada durante as iterações.")
        
        # st.markdown("---")
        delay_ui = st.slider("Atraso por Frame (Segundos):",
                             min_value=0.0, max_value=1.0, value=0.1, step=0.05,
                             help="Aumente para deixar a animação mais lenta e observar a organização das células com calma.")
        
        start_button = st.button("▶ Iniciar Simulação", width="stretch", type="primary")

    # --- ÁREA PRINCIPAL ---
    # Layout em colunas
    # col1, col2 = st.columns([1, 1])
    _, col1, _, col2, _ = st.columns([0.14, 1, 0.07, 1, 0.14])
    
    with col1:
        st.subheader("Estado Inicial")
        placeholder_inicial = st.empty()
        
    with col2:
        st.subheader("Evolução")
        placeholder_animacao = st.empty()
        status_text = st.empty()
        progress_bar = st.progress(0)

    # --- LÓGICA DE EXECUÇÃO ---
    if start_button:
        # 1. Inicializa o estado (matriz N x N com -1 e 1)
        grid = np.random.choice(np.array([-1, 1], dtype=np.int8), size=(n_size, n_size))
        
        # Renderiza a imagem inicial
        img_inicial = render_grid_to_rgb(grid)
        placeholder_inicial.image(img_inicial, width="stretch")
        
        # 2. Configurações da Animação
        passos_por_frame = int(total_iteracoes / fps_update)
        
        # 3. Loop de Animação
        start_time = time.time()
        
        for frame in range(fps_update):
            # Processa o bloco matematicamente na velocidade C
            grid = metropolis_hastings_step(grid, beta, passos_por_frame)
            
            # Renderiza velozmente e envia para a UI
            img_atual = render_grid_to_rgb(grid)
            placeholder_animacao.image(img_atual, width="stretch")
            
            # Atualização de UI com FORMATAÇÃO PT-BR
            iteracoes_atuais = (frame + 1) * passos_por_frame
            progress_bar.progress((frame + 1) / fps_update)
            
            # Aplicando a formatação na string do painel
            iter_fmt = formatar_ptbr(iteracoes_atuais, inteiro=True)
            total_fmt = formatar_ptbr(total_iteracoes, inteiro=True)
            status_text.caption(f"Iterações: {iter_fmt} / {total_fmt}")
            
            # Throttling
            if delay_ui > 0:
                time.sleep(delay_ui)

        elapsed_time = time.time() - start_time
        tempo_real_calculo = elapsed_time - (fps_update * delay_ui)
        
        # Output final com formato PT-BR
        tempo_fmt = formatar_ptbr(tempo_real_calculo, casas=2)
        st.success(f"Simulação finalizada! Tempo de cálculo puro (sem a pausa visual): {tempo_fmt} segundos.")

if __name__ == "__main__":
    main()