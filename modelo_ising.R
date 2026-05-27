# ==========================================================
# MODELO DE ISING VIA METROPOLIS-HASTINGS
# ==========================================================

# ----------------------------------------------------------
# Definindo uma semente para reprodutibilidade
# ----------------------------------------------------------
set.seed(515141)

# ----------------------------------------------------------
# Tamanho da grade n x n
# ----------------------------------------------------------
n <- 100

# ==========================================================
# FUNÇÃO: Cálculo da variação de energia ΔE
# ==========================================================
# Esta função calcula a diferença de energia ao inverter
# um spin específico da rede.
#
# O modelo utiliza condições periódicas de contorno,
# ou seja, as bordas "se conectam".
# ==========================================================

delta_E <- function(configuracao, i, j) {
  
  n <- nrow(configuracao)
  
  # --------------------------------------------------------
  # Índices dos vizinhos (contorno periódico)
  # --------------------------------------------------------
  i_acima    <- ifelse(i == 1, n, i - 1)
  i_abaixo   <- ifelse(i == n, 1, i + 1)
  
  j_esquerda <- ifelse(j == 1, n, j - 1)
  j_direita  <- ifelse(j == n, 1, j + 1)
  
  # --------------------------------------------------------
  # Soma dos spins vizinhos
  # --------------------------------------------------------
  soma_vizinhos <-
    configuracao[i_acima, j] +
    configuracao[i_abaixo, j] +
    configuracao[i, j_esquerda] +
    configuracao[i, j_direita]
  
  # --------------------------------------------------------
  # Variação de energia:
  #
  # ΔE = 2 * s(i,j) * soma_vizinhos
  #
  # Assumimos constante de interação J = 1
  # --------------------------------------------------------
  return(2 * configuracao[i, j] * soma_vizinhos)
}

# ==========================================================
# FUNÇÃO: Simulação do Modelo de Ising
# ==========================================================
# Utiliza o algoritmo de Metropolis-Hastings para gerar
# amostras da distribuição de Boltzmann.
#
# beta = 1 / (kT)
#
# beta pequeno  -> alta temperatura -> desordem
# beta grande   -> baixa temperatura -> alinhamento
# ==========================================================

simular_ising <- function(configuracao, beta, iteracoes) {
  
  n <- nrow(configuracao)
  
  # --------------------------------------------------------
  # Loop principal do algoritmo
  # --------------------------------------------------------
  for (passo in 1:iteracoes) {
    
    # Escolhe posição aleatória
    i <- sample(1:n, 1)
    j <- sample(1:n, 1)
    
    # Calcula variação de energia
    de <- delta_E(configuracao, i, j)
    
    # ------------------------------------------------------
    # Regra de Metropolis
    #
    # Se ΔE <= 0:
    #   aceita automaticamente
    #
    # Caso contrário:
    #   aceita com probabilidade exp(-beta * ΔE)
    # ------------------------------------------------------
    if (de <= 0 || runif(1) < exp(-beta * de)) {
      
      # Inverte o spin
      configuracao[i, j] <- -configuracao[i, j]
    }
  }
  
  return(configuracao)
}

# ==========================================================
# Valores de beta
# ==========================================================
betas <- c(0.5, 1.3, 2.8)

# ==========================================================
# Número de iterações
# ==========================================================
n_iteracoes <- 1000000

# ==========================================================
# Listas para armazenar configurações
# ==========================================================
configuracoes_iniciais <- list()
configuracoes_finais   <- list()

# ==========================================================
# Simulações
# ==========================================================
for (i in seq_along(betas)) {
  
  beta <- betas[i]
  
  # --------------------------------------------------------
  # Configuração inicial aleatória
  # --------------------------------------------------------
  configuracao_inicial <-
    matrix(sample(c(1, -1),
                  n * n,
                  replace = TRUE),
           nrow = n)
  
  configuracoes_iniciais[[i]] <- configuracao_inicial
  
  # --------------------------------------------------------
  # Executa a simulação usando a MESMA configuração inicial
  # --------------------------------------------------------
  configuracoes_finais[[i]] <-
    simular_ising(configuracao_inicial,
                  beta,
                  n_iteracoes)
}

# ==========================================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==========================================================

for (i in seq_along(betas)) {
  
  beta <- betas[i]
  
  par(mfrow = c(1, 2), mar = c(3, 2, 3, 2))
  
  # --------------------------------------------------------
  # Configuração inicial
  # --------------------------------------------------------
  image(configuracoes_iniciais[[i]],
        col = c("blue", "red"),
        main = bquote("Configuração Inicial -" ~ beta == .(beta)),
        axes = FALSE,
        xlab = "",
        ylab = "")
  
  # --------------------------------------------------------
  # Configuração final
  # --------------------------------------------------------
  image(configuracoes_finais[[i]],
        col = c("blue", "red"),
        main = bquote("Configuração Final ->" ~ beta == .(beta)),
        axes = FALSE,
        xlab = "",
        ylab = "")
  
  # --------------------------------------------------------
  # Legenda
  # --------------------------------------------------------
  legend("bottom",
         legend = c("Spin -1", "Spin +1"),
         fill = c("blue", "red"),
         horiz = TRUE,
         bty = "n",
         inset = c(0, -0.2),
         xpd = TRUE)
}

