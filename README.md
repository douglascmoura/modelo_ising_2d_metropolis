# 🧪 Modelo de Ising 2D: Simulação Estocástica e Transições de Fase

Este repositório é dedicado à modelagem computacional e simulação estatística do **Modelo de Ising Bidimensional**, um dos paradigmas mais importantes da Mecânica Estatística para o estudo de fenômenos coletivos, magnetismo e transições de fase.

O projeto une o rigor matemático dos métodos de Monte Carlo à interatividade moderna, oferecendo uma aplicação visual de alta performance desenvolvida em **Python (Streamlit)** e rotinas de análise complementar em **R**.

---

## 🎯 Fundamentação Teórica

O sistema consiste em uma rede quadrada bidimensional de dimensão $n \times n$ com $N = n^2$ sítios. Cada sítio abriga uma variável aleatória chamada *spin* ($\sigma_i \in \{-1, +1\}$), orientada para cima ou para baixo. 

A energia total de uma configuração é governada pela Hamiltoniana do sistema:

$$H(\sigma) = -J \sum_{\langle i,j \rangle} \sigma_i \sigma_j - h \sum_i \sigma_i$$

Onde:
* $J$ representa a constante de acoplamento entre vizinhos mais próximos ($J > 0$ define o comportamento ferromagnético).
* $h$ representa o campo magnético externo aplicado.

A simulação computacional utiliza a dinâmica estocástica do **Algoritmo de Metropolis-Hastings** para gerar amostras cuja distribuição estacionária converge para a distribuição de Gibbs do modelo. Isso permite observar o surgimento da magnetização espontânea ao cruzar a Temperatura Crítica (Ponto de Curie).

---

## 🚀 Diferenciais Técnicos e Performance

* **Aceleração Just-In-Time (JIT):** O motor de atualização de Monte Carlo em Python foi otimizado utilizando a biblioteca `numba` (`@njit`), permitindo que milhões de inversões de spin sejam calculadas em frações de segundo, contornando o gargalo tradicional de loops nativos do Python.
* **Interface Streamlit Interativa:** Renderização gráfica em tempo real das configurações de spin, com controle dinâmico de parâmetros de entrada (Temperatura/Beta, tamanho da rede, passos de iteração) localizados para o padrão PT-BR.
* **Abordagem Multilinguagem:** Arquitetura flexível contendo códigos estruturados tanto em Python quanto em R para validação estatística e comparação de ecossistemas.

---

## 📂 Estrutura do Repositório

```text
├── Modelo_Ising.pdf                      # Relatório técnico-teórico completo do modelo
├── modelo_ising.R                        # Script em R 
├── app_ising.py                          # Script principal da aplicação interativa Streamlit
└── README.md                             # Este documento de apresentação
```

---

## 🛠️ Tecnologias e Dependências

### Python:
* `streamlit` (Interface do usuário e gerenciamento de estado)
* `numpy` (Estruturas vetoriais da rede de spins)
* `numba` (Compilação JIT para aceleração matemática)

### R:
* Ambiente básico utilizado para a criação inicial da estrutura de simulação do modelo.

---

## 💻 Como Executar a Aplicação Interativa

### 1. Versão Python (Streamlit)
Certifique-se de possuir o Python instalado e as dependências configuradas. No diretório do projeto, execute:

```bash
# Instalação dos pacotes necessários
pip install streamlit numpy numba

# Inicialização do servidor da aplicação
streamlit run app_ising.py
```

---

## 📖 Como Visualizar o Estudo Completo

A dedução matemática detalhada, as análises de custo computacional da função de partição e as considerações sobre criticalidade sistêmica estão consolidadas no documento oficial em anexo.

👉 **[Clique aqui para acessar o Relatório Técnico Completo (PDF)](./Modelo_Ising.pdf)**

