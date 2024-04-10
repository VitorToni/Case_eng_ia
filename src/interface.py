import streamlit as st
import datetime
import matplotlib.pyplot as plt
from src.funcs_duckdb import *
from src.funcs_ia import *


def interface_grafica():
    st.title("Projeto de Consulta e Analise de Ativos Listados na Bolsa")

    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data de Início (Default: 10 anos)", datetime.datetime.now() - datetime.timedelta(days=365*10))
    with col2:
        data_fim = st.date_input("Data de Fim (Hoje)", datetime.datetime.now())

    tickers_disponiveis = ["BTC-USD", "ETH-USD", "ITSA4.SA", "PETR4.SA", "VALE3.SA", "TAEE11.SA"]  # Lista de tickers disponíveis
    ticker = st.multiselect("Ticker(s)", tickers_disponiveis, default=["BTC-USD"])  # Seleção de um ou mais tickers


    if st.button("Coletar Dados e Consultar com Gen IA"):
        with st.spinner("Ingestão em andamento..."):
            ingest_dados(data_inicio, data_fim, ticker)
        st.success("Ingestão Realizada")

        st.subheader("Fechamento")
        resultado_mes = consultar_fechamentos("Mes")
        resultado_ano = consultar_fechamentos("Ano")
        if resultado_mes is not None and resultado_ano is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Anual")
                st.dataframe(resultado_ano)
            with col2:
                st.subheader("Mensal")
                st.dataframe(resultado_mes)   

            st.subheader("Exemplo de gráfico")
            fig, ax = plt.subplots(figsize=(12, 6))
            for ticker, group in resultado_ano.groupby("Ticker"):
                ax.plot(group["Ano"], group["Close"], label=ticker, linewidth=2.5)
            ax.set_title("Preço de Fechamento ao Longo do Ano")
            ax.set_xlabel("Ano")
            ax.set_ylabel("Preço de Fechamento")
            ax.invert_xaxis()  # Inverter o eixo x
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            with st.spinner("Consultando IA..."):
                st.subheader("Visão Anual")
                st.markdown(consultar_ia(str("[Pt-br] Analise os dados a seguir e me dê 5 insights importantes como um investidor experiente: "
                                                + resultado_ano.to_string())))
                st.subheader("Visão Mensal")
                st.markdown(consultar_ia(str("[Pt-br] Analise os dados a seguir e me dê 5 insights importantes como um investidor experiente: "
                                                + resultado_mes.to_string())))
        else:
            st.error("Erro ao executar a consulta.")
