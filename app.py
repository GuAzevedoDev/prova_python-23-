import pandas as pd
import plotly.express as px
import streamlit as st

# -- TRATAMENTO DE DADOS

df = pd.read_excel("censo_1872.xlsx", engine="openpyxl")
df = df.drop_duplicates()

totais = {
        "Homens livres": df["homens_livres"].sum(),
        "Homens escravizados": df["homens_escravizados"].sum(),
        "Mulheres livres": df["mulheres_livres"].sum(),
        "Mulheres escravizadas": df["mulheres_escravizadas"].sum(),
    }
    

total_homens = totais["Homens livres"] + totais["Homens escravizados"]
total_mulheres = totais["Mulheres livres"] + totais["Mulheres escravizadas"]
linhas = []
for grupo, total in totais.items():
    if grupo.startswith("Homens"):
        bese = total_homens
    else:
        base = total_mulheres
    linhas.append(
        {
                "Grupo": grupo,
                "Total de pessoas": int(total),
                "Percentual (%)": round(total / base * 100, 2),
        }
    )



tabela = pd.DataFrame(linhas)

# -- STREAMLIT

st.title("Censo de 1872: população livre e escravizada")

visualizacao = st.sidebar.radio("Visualização", ["Tabela", "Gráficos"])

if visualizacao == "Tabela":
    st.header("Totais e percentuais por grupo")
    st.dataframe(tabela, width="stretch", hide_index=True)
    st.caption("O percentual de cada grupo é calculado dentro do próprio sexo.")
else:
    st.header("Percentual de livres e escravizados por sexo")
    homens = tabela[tabela["Grupo"].str.startswith("Homens")]
    mulheres = tabela[tabela["Grupo"].str.startswith("Mulheres")]
    st.plotly_chart(
        px.pie(homens, names="Grupo", values="Total de pessoas", title="Homens"),
        width="stretch",
    )
    st.plotly_chart(
        px.pie(mulheres, names="Grupo", values="Total de pessoas", title="Mulheres"),
        width="stretch",
    )

st.markdown(f"Fonte dos dados: [https://basedosdados.org/](https://basedosdados.org/)")
