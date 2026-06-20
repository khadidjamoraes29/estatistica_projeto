from shiny import App, ui, reactive, render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# INTERFACE

app_ui = ui.page_fluid(

    ui.include_css("style/styles.css"),

    ui.div(
    {"class": "cabecalho"},

    ui.h1("📊 Dashboard Estatístico"),

    ui.p(
        "Faça o upload de um arquivo CSV para iniciar as análises."
    ),

    ui.div(
    ui.p("Selecione um arquivo CSV", class_="texto-upload"),

    ui.input_file(
        "arquivo",
        "",
        accept=[".csv"]
    ),

    class_="upload-centralizado"
    ),
),

    ui.navset_tab(

        
        # ABA 1
        
        ui.nav_panel(
            "Análise Descritiva",

            ui.layout_columns(

                ui.card(
                    ui.h4("Selecione a variável"),
                    ui.input_select(
                        "var_desc",
                        "Variável",
                        choices=[]
                    )
                ),

                ui.card(
                    ui.h4("Estatísticas Descritivas"),
                    ui.output_text_verbatim("estatisticas")
                )
            ),

            ui.layout_columns(

                ui.card(
                    ui.output_plot("histograma")
                ),

                ui.card(
                    ui.output_plot("boxplot")
                )
            )
        ),

        
        # ABA 2
        
        ui.nav_panel(
            "Teste de Hipóteses",

            ui.layout_columns(

                ui.card(

                    ui.input_select(
                        "var_teste",
                        "Variável",
                        choices=[]
                    ),

                    ui.input_numeric(
                        "variancia",
                        "Variância Populacional",
                        value=1,
                        min=0.0001
                    ),

                    ui.input_radio_buttons(
                        "tipo_teste",
                        "Tipo de teste",
                        choices={
                            "bilateral": "Bilateral",
                            "direita": "Unilateral à direita",
                            "esquerda": "Unilateral à esquerda"
                        }
                    ),

                    ui.input_slider(
                        "mu0",
                        "μ₀",
                        min=-100,
                        max=100,
                        value=0
                    ),

                    ui.input_slider(
                        "alpha",
                        "Nível de significância (α)",
                        min=0.01,
                        max=0.20,
                        value=0.05,
                        step=0.01
                    )
                ),

            ui.card(
                ui.h4("Resultado"),
                ui.output_text_verbatim("resultado_teste")
            )

        ),  
            ui.card(
                ui.output_plot("grafico_teste")
            )
    ),  

        
        # ABA 3
        
        ui.nav_panel(
            "Intervalo de Confiança",

            ui.layout_columns(

                ui.card(

                    ui.input_select(
                        "var_ic",
                        "Variável",
                        choices=[]
                    ),

                    ui.input_slider(
                        "confianca",
                        "Nível de confiança",
                        min=0.80,
                        max=0.99,
                        value=0.95,
                        step=0.01
                    )
                ),

                ui.card(
                    ui.h4("Resultado"),
                    ui.output_text_verbatim("resultado_ic")
                )
            )
        ),

        
        # ABA 4
        
        ui.nav_panel(
            "Regressão Linear",

            ui.layout_columns(

                ui.card(

                    ui.input_select(
                        "x_var",
                        "Variável X",
                        choices=[]
                    ),

                    ui.input_select(
                        "y_var",
                        "Variável Y",
                        choices=[]
                    )
                ),

                ui.card(
                    ui.h4("Resultados"),
                    ui.output_text_verbatim("resultado_regressao")
                )
            ),

            ui.card(
                ui.output_plot("grafico_regressao")
            )
        )
    )
)



# SERVER

def server(input, output, session):

    
    # LEITURA DOS DADOS

    @reactive.calc
    def dados():

        arquivo = input.arquivo()

        if arquivo is None:
            return None

        caminho = arquivo[0]["datapath"]

        try:
            return pd.read_csv(caminho)

        except:
            return None


    
    # VARIÁVEIS NUMÉRICAS
    

    @reactive.calc
    def variaveis_numericas():

        df = dados()

        if df is None:
            return []

        return list(
            df.select_dtypes(include=np.number).columns
        )


    
    # ATUALIZA SELECTS

    @reactive.effect
    def atualizar_selects():

        vars_num = variaveis_numericas()

        ui.update_select(
            "var_desc",
            choices=vars_num,
            selected=vars_num[0] if vars_num else None
        )

        ui.update_select(
            "var_teste",
            choices=vars_num,
            selected=vars_num[0] if vars_num else None
        )

        ui.update_select(
            "var_ic",
            choices=vars_num,
            selected=vars_num[0] if vars_num else None
        )

        ui.update_select(
            "x_var",
            choices=vars_num,
            selected=vars_num[0] if vars_num else None
        )

        ui.update_select(
            "y_var",
            choices=vars_num,
            selected=vars_num[1] if len(vars_num) > 1 else None
        )


    
    # ANÁLISE DESCRITIVA

    @output
    @render.text
    def estatisticas():

        df = dados()

        if df is None:
            return "Carregue um arquivo."

        coluna = input.var_desc()

        if coluna not in df.columns:
            return ""

        serie = df[coluna].dropna()

        texto = f"""
Média: {serie.mean():.4f}

Mediana: {serie.median():.4f}

Desvio-padrão: {serie.std():.4f}

Tamanho da amostra: {len(serie)}

Mínimo: {serie.min():.4f}

Máximo: {serie.max():.4f}
"""

        return texto


    @output
    @render.plot
    def histograma():

        df = dados()

        if df is None:
            return

        coluna = input.var_desc()

        fig, ax = plt.subplots()

        ax.hist(
            df[coluna].dropna(),
            bins=20
        )

        ax.set_title("Histograma")
        ax.set_xlabel(coluna)
        ax.set_ylabel("Frequência")

        return fig


    @output
    @render.plot
    def boxplot():

        df = dados()

        if df is None:
            return

        coluna = input.var_desc()

        fig, ax = plt.subplots()

        ax.boxplot(
            df[coluna].dropna()
        )

        ax.set_title("Boxplot")

        return fig


    
    # TESTE Z

    @output
    @render.text
    def resultado_teste():

        df = dados()

        if df is None:
            return "Carregue um arquivo."

        coluna = input.var_teste()

        serie = df[coluna].dropna()

        media = serie.mean()

        n = len(serie)

        mu0 = input.mu0()

        sigma2 = input.variancia()

        sigma = np.sqrt(sigma2)

        z = (media - mu0) / (sigma / np.sqrt(n))

        tipo = input.tipo_teste()

        if tipo == "bilateral":
            p = 2 * (1 - norm.cdf(abs(z)))

        elif tipo == "direita":
            p = 1 - norm.cdf(z)

        else:
            p = norm.cdf(z)

        alpha = input.alpha()

        decisao = (
            "Rejeita H0"
            if p < alpha
            else "Não rejeita H0"
        )

        return f"""
Estatística Z: {z:.4f}

p-valor: {p:.6f}

Decisão: {decisao}
"""
    @output
    @render.plot
    def grafico_teste():

        df = dados()

        if df is None:
            return

        coluna = input.var_teste()

        if coluna not in df.columns:
            return

        serie = df[coluna].dropna()

        media = serie.mean()
        n = len(serie)

        mu0 = input.mu0()
        sigma = np.sqrt(input.variancia())

        z = (media - mu0) / (sigma / np.sqrt(n))

        tipo = input.tipo_teste()
        alpha = input.alpha()

        x = np.linspace(-4, 4, 500)
        y = norm.pdf(x)

        fig, ax = plt.subplots(figsize=(8, 4))

        # Curva normal
        ax.plot(x, y, linewidth=2)

        # Linha do Z calculado
        if abs(z) <= 5:
            ax.axvline(
                z,
                linestyle="--",
                linewidth=2,
                label=f"Z = {z:.2f}"
            )
        else:
            ax.text(
                0.98,
                0.95,
                f"Z = {z:.2f}\n(fora da escala)",
                transform=ax.transAxes,
                ha="right",
                va="top",
                bbox=dict(boxstyle="round")
            )

        if tipo == "bilateral":

            z_crit = norm.ppf(1 - alpha / 2)

            ax.fill_between(x, y, where=(x <= -z_crit), alpha=0.3)
            ax.fill_between(x, y, where=(x >= z_crit), alpha=0.3)

            ax.axvline(-z_crit, linestyle=":")
            ax.axvline(z_crit, linestyle=":")

        elif tipo == "direita":

            z_crit = norm.ppf(1 - alpha)

            ax.fill_between(x, y, where=(x >= z_crit), alpha=0.3)
            ax.axvline(z_crit, linestyle=":")

        else:  # esquerda

            z_crit = norm.ppf(alpha)

            ax.fill_between(x, y, where=(x <= z_crit), alpha=0.3)
            ax.axvline(z_crit, linestyle=":")

        ax.set_title("Teste Z - Distribuição Normal")
        ax.set_xlabel("Valor Z")
        ax.set_ylabel("Densidade")

        ax.set_xlim(-5, 5)

        if abs(z) <= 5:
            ax.legend()

        return fig


    
    # INTERVALO DE CONFIANÇA

    @output
    @render.text
    def resultado_ic():

        df = dados()

        if df is None:
            return "Carregue um arquivo."

        coluna = input.var_ic()

        serie = df[coluna].dropna()

        media = serie.mean()

        n = len(serie)

        sigma = serie.std()

        confianca = input.confianca()

        alpha = 1 - confianca

        z = norm.ppf(
            1 - alpha / 2
        )

        erro = (
            z * sigma / np.sqrt(n)
        )

        li = media - erro
        ls = media + erro

        return f"""
Nível de confiança: {confianca:.2%}

Limite inferior: {li:.4f}

Limite superior: {ls:.4f}
"""


    
    # REGRESSÃO

    @output
    @render.text
    def resultado_regressao():

        df = dados()

        if df is None:
            return "Carregue um arquivo."

        x_var = input.x_var()
        y_var = input.y_var()

        dados_reg = df[
            [x_var, y_var]
        ].dropna()

        X = dados_reg[[x_var]]

        y = dados_reg[y_var]

        modelo = LinearRegression()

        modelo.fit(X, y)

        pred = modelo.predict(X)

        R = np.corrcoef(
            dados_reg[x_var],
            dados_reg[y_var]
        )[0, 1]

        R2 = r2_score(
            y,
            pred
        )

        a = modelo.intercept_
        b = modelo.coef_[0]

        return f"""
Coeficiente de Correlação (R): {R:.4f}

Coeficiente de Determinação (R²): {R2:.4f}

Equação da reta:

y = {a:.4f} + {b:.4f}x
"""


    @output
    @render.plot
    def grafico_regressao():

        df = dados()

        if df is None:
            return

        x_var = input.x_var()
        y_var = input.y_var()

        dados_reg = df[
            [x_var, y_var]
        ].dropna()

        X = dados_reg[[x_var]]

        y = dados_reg[y_var]

        modelo = LinearRegression()

        modelo.fit(X, y)

        pred = modelo.predict(X)

        fig, ax = plt.subplots()

        ax.scatter(
            dados_reg[x_var],
            y
        )

        ax.plot(
            dados_reg[x_var],
            pred
        )

        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)

        ax.set_title(
            "Regressão Linear Simples"
        )

        return fig



# APP
app = App(app_ui, server)
