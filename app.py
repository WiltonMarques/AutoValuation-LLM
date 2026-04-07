import streamlit as st
import yfinance as yf
import pandas as pd
import re
from google import genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AutoValuation LLM", page_icon="📈", layout="wide")

st.title("📈 AutoValuation: Motor Quantitativo com IA")
st.markdown("Bem-vindo ao Screener de Valuation. Digite os Tickers da B3 para a Inteligência Artificial analisar o sentimento do mercado e projetar a taxa de crescimento.")

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    chave_api = st.text_input("Cole sua API Key do Gemini:", type="password")
    # Coloquei sem o .SA no padrão para mostrar que o nosso sistema de auto-completar funciona!
    tickers_input = st.text_input("Tickers (separados por vírgula):", "PETR4, VALE3, WEGE3")
    btn_analisar = st.button("🚀 Iniciar Análise Automática")

# --- MOTOR DE ANÁLISE (O Cérebro da Operação) ---
def analisar_acao(ticker, client):
    try:
        empresa = yf.Ticker(ticker)
        noticias = empresa.news
        
        # Extrai o título das 4 notícias mais recentes, se existirem
        pacote_noticias = "".join([f"- {n.get('content', {}).get('title', '')}\n" for n in noticias[:4]]) if noticias else "Sem notícias relevantes recentes."

        prompt = f"""
        Atue como Analista Quantitativo. Analise as notícias de {ticker}:\n{pacote_noticias}\n
        A taxa de crescimento neutra é 5.0%. Ajuste-a com base nas notícias (mín 0.01, máx 0.15).
        Responda ESTRITAMENTE:\nJUSTIFICATIVA: [Uma frase]\nTAXA: [Numero decimal]
        """
        
        # Chamada para a API Nova do Gemini
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        
        # Pesca a taxa com RegEx
        match = re.search(r"TAXA:\s*([0-9.]+)", resposta.text)
        taxa_ia = float(match.group(1)) if match else 0.05
        
        # Puxa o preço atual de forma segura
        preco_atual = empresa.info.get('currentPrice', 0)
        
        return {
            "Ticker": ticker,
            "Preço (R$)": round(preco_atual, 2) if preco_atual else "N/A",
            "Crescimento (IA)": f"{taxa_ia * 100:.1f}%",
            "Tese de Investimento": resposta.text.split('\n')[0].replace('JUSTIFICATIVA: ', '').strip()
        }
    except Exception as e:
        return {"Ticker": ticker, "Erro": f"Falha na extração: {str(e)}"}

# --- EXECUÇÃO VISUAL (Front-End) ---
if btn_analisar:
    if not chave_api:
        st.warning("⚠️ Por favor, insira a sua API Key do Google Gemini na barra lateral.")
    else:
        with st.spinner("🤖 A IA está lendo o mercado... Isso pode levar alguns segundos."):
            # Inicializa o cliente com a chave fornecida na tela
            client = genai.Client(api_key=chave_api)
            
            # 🛡️ TRATAMENTO INTELIGENTE DE TICKERS (Auto-completar .SA)
            lista_tickers = []
            for t in tickers_input.split(","):
                t_limpo = t.strip().upper()
                # Se o usuário esqueceu o .SA (ex: PETR4), o código adiciona sozinho
                if not t_limpo.endswith(".SA"):
                    t_limpo += ".SA"
                lista_tickers.append(t_limpo)
            
            # Loop de análise para cada ação
            resultados = []
            for t in lista_tickers:
                resultados.append(analisar_acao(t, client))
            
            # Transforma em Tabela e Plota na Tela
            df = pd.DataFrame(resultados)
            
            st.success("✅ Análise Concluída com Sucesso!")
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("*Disclaimer: Este é um projeto de Engenharia de Dados e IA. Não constitui recomendação de compra ou venda de ativos.*")
