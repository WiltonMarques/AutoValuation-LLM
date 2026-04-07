import streamlit as st
import yfinance as yf
import pandas as pd
import re
from google import genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AutoValuation LLM", page_icon="📈", layout="wide")

st.title("📈 AutoValuation: Motor Quantitativo com IA")
st.markdown("Bem-vindo ao Screener de Valuation. Digite os Tickers da B3 para a Inteligência Artificial analisar o sentimento do mercado e projetar a taxa de crescimento.")

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    chave_api = st.text_input("Cole sua API Key do Gemini:", type="password")
    tickers_input = st.text_input("Tickers (separados por vírgula):", "WEGE3.SA, VALE3.SA, PETR4.SA")
    btn_analisar = st.button("🚀 Iniciar Análise Automática")

# --- MOTOR DE ANÁLISE (A Função que você já testou) ---
def analisar_acao(ticker, client):
    try:
        empresa = yf.Ticker(ticker)
        noticias = empresa.news
        pacote_noticias = "".join([f"- {n.get('content', {}).get('title', '')}\n" for n in noticias[:4]]) if noticias else "Sem notícias."

        prompt = f"""
        Atue como Analista Quantitativo. Analise as notícias de {ticker}:\n{pacote_noticias}\n
        A taxa de crescimento neutra é 5.0%. Ajuste-a com base nas notícias (mín 0.01, máx 0.15).
        Responda ESTRITAMENTE:\nJUSTIFICATIVA: [Uma frase]\nTAXA: [Numero decimal]
        """
        
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        match = re.search(r"TAXA:\s*([0-9.]+)", resposta.text)
        taxa_ia = float(match.group(1)) if match else 0.05
        
        return {
            "Ticker": ticker,
            "Preço (R$)": round(empresa.info.get('currentPrice', 0), 2),
            "Crescimento (IA)": f"{taxa_ia * 100:.1f}%",
            "Tese de Investimento": resposta.text.split('\n')[0].replace('JUSTIFICATIVA: ', '')
        }
    except Exception as e:
        return {"Ticker": ticker, "Erro": str(e)}

# --- EXECUÇÃO VISUAL ---
if btn_analisar:
    if not chave_api:
        st.warning("⚠️ Por favor, insira a sua API Key do Google Gemini na barra lateral.")
    else:
        # Mostra um spinner de carregamento bonito na tela
        with st.spinner("🤖 A IA está lendo o mercado... Isso pode levar alguns segundos."):
            client = genai.Client(api_key=chave_api)
            lista_tickers = [t.strip() for t in tickers_input.split(",")]
            resultados = []
            
            for t in lista_tickers:
                resultados.append(analisar_acao(t, client))
            
            df = pd.DataFrame(resultados)
            
            st.success("✅ Análise Concluída com Sucesso!")
            st.dataframe(df, use_container_width=True) # Desenha a tabela interativa na tela
            
            st.markdown("---")
            st.markdown("*Disclaimer: Este é um projeto de Engenharia de Dados e IA. Não constitui recomendação de compra ou venda de ativos.*")
