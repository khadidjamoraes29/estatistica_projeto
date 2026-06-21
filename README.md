# Dashboard Estatístico

Dashboard interativo em **Python**, construído com **Shiny for Python**, para análise estatística de dados quantitativos.

## Funcionalidades

### 1. Análise Descritiva
- Seleção de uma base de dados (pronta ou enviada pelo usuário) e de uma variável quantitativa
- Histograma e boxplot da variável selecionada
- Estatísticas descritivas: média, mediana, desvio-padrão, tamanho da amostra, mínimo e máximo

### 2. Teste de Hipóteses para a Média (variância conhecida)
- Campo numérico para a variância populacional
- Tipo de teste (bilateral, unilateral à direita, unilateral à esquerda)
- Slider para μ₀ (ajustado automaticamente à escala da variável escolhida)
- Slider para o nível de significância (α)
- Retorna a estatística do teste (Z), o p-valor e a decisão (rejeita/não rejeita H0), além do gráfico da curva normal com a região de rejeição

### 3. Intervalo de Confiança Normal para a Média
- Slider para o nível de confiança
- Retorna limite inferior, limite superior e o nível de confiança utilizado

### 4. Regressão Linear Simples
- Seleção de variável resposta (Y) e variável explicativa (X)
- Coeficiente de correlação (R), coeficiente de determinação (R²) e equação da reta ajustada
- Gráfico de dispersão com a linha de regressão

## Bases de dados

O dashboard já vem com três bases prontas para escolha, todas com pelo menos duas variáveis quantitativas:

| Base | Descrição |
|---|---|
| Pinguins | Medidas corporais de pinguins (`data/penguins.csv`) |
| Gorjetas | Valores de conta e gorjeta em restaurante (`data/tips.csv`) |
| Iris | Medidas de pétalas e sépalas de flores (`data/iris.csv`) |

Também é possível enviar uma planilha CSV própria pelo upload.

## Como executar

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # Linux/Mac

# Instalar as dependências
pip install -r requirements.txt

# Rodar o dashboard
shiny run app.py
```

Acesse `http://127.0.0.1:8000` (ou a porta informada no terminal) no navegador.

## Tecnologias

- [Shiny for Python](https://shiny.posit.co/py/)
- pandas / numpy
- matplotlib
- scipy (distribuições estatísticas)
- scikit-learn (regressão linear)

## Equipe

- Khadidja Moraes
- Raphael Cordeiro
- Yago Ferraz

## Vídeo de demonstração

quem upar o video lembra de colocar o link aqui
