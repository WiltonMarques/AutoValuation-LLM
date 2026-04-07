# 📈 AutoValuation-LLM: Motor Quantitativo com IA Dinâmica

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Finance](https://img.shields.io/badge/Quantitative_Finance-005571?style=for-the-badge)

🔥 **Acesse o Web App rodando em tempo real:** 👉 **[CLIQUE AQUI PARA TESTAR O AUTOVALUATION] (https://autovaluation-wilton.streamlit.app)** 👈

---

## 🎯 Apresentação do Projeto

O mercado financeiro tradicional baseia-se em modelos quantitativos estáticos, como o **Fluxo de Caixa Descontado (DCF)**. O grande problema dessa abordagem é a "miopia" qualitativa: a matemática é cega para o sentimento do mercado, notícias de curto prazo e estratégias da diretoria. 

O **AutoValuation-LLM** nasce para resolver essa dor. Trata-se de uma pipeline de Engenharia de Dados que atua como um Analista Quantitativo Institucional. O sistema ingere notícias financeiras em tempo real, utiliza Inteligência Artificial Generativa (Google Gemini) para interpretar o sentimento (Positivo/Negativo/Alerta de Risco) e converte essa leitura de linguagem natural em um ajuste matemático direto na taxa de crescimento do motor DCF. 

O resultado? Um "Preço Justo" dinâmico que se adapta ao humor do mercado instantaneamente.

---

## ⚙️ Funcionalidades Principais

* **Rastreamento de Dados em Tempo Real:** Conexão com APIs financeiras (via `yfinance`) para captura de balanços, cotações e as manchetes mais recentes do ativo selecionado.
* **Leitura de Sentimento (Outside-In):** Empacotamento de textos não-estruturados (notícias) em prompts restritivos para análise sintática da IA.
* **Motor DCF Integrado:** Recálculo automático do Valuation da empresa (WACC, Valor Terminal e Fluxos Projetados) substituindo premissas engessadas pelas taxas dinâmicas geradas pela IA.
* **Screener de Múltiplos Ativos:** Capacidade de varrer uma lista de *tickers* da B3 simultaneamente, gerando um relatório comparativo de oportunidades.
* **Interface Web App:** Front-end responsivo construído em Streamlit, permitindo o uso da ferramenta por usuários sem conhecimento de programação.

---

## 🛡️ Desafios de Engenharia & Otimizações Aplicadas

Durante o desenvolvimento da arquitetura, problemas reais de engenharia de software e de *Machine Learning* foram mapeados e solucionados:

1. **Mitigação de *Gradient Explosion* (Treinamento LLM):** * *O Desafio:* Durante a construção da primeira versão do modelo (v9) usando LoRA (Rank 32), a rede neural sofreu colapso matemático (*loss* infinita).
   * *A Solução:* Otimização rigorosa dos hiperparâmetros, implementando redução no *learning rate* (`2e-5`) e aplicação de um cinto de segurança matemático mais agressivo via *Gradient Clipping* (`max_grad_norm=0.1`), garantindo a convergência da rede neural.

2. **Resiliência contra Mudanças Ocultas em APIs de Terceiros:**
   * *O Desafio:* A API do Yahoo Finance alterou silenciosamente sua estrutura JSON, aninhando os dados textuais de notícias, o que retornava pacotes vazios para a IA.
   * *A Solução:* Implementação de rotinas de depuração (*debugging*) no dicionário bruto e reescrita do *parser* para varrer dicionários aninhados (acessando a chave oculta `content`), garantindo a extração do Título e do *Summary*.

3. **Gerenciamento de Dependências e Obsolescência:**
   * *O Desafio:* Descontinuação repentina da biblioteca `google.generativeai` pelo Google durante o desenvolvimento do projeto.
   * *A Solução:* Refatoração imediata da base de código para integrar o novo SDK `google.genai`, utilizando a infraestrutura atualizada de clientes virtuais de forma segura, acoplada ao cofre de *Secrets* do ambiente.

---

## 🚀 Roadmap e Propostas de Melhorias Futuras

O projeto base demonstrou que a fusão de NLP e finanças quantitativas é viável e escalável. Os próximos passos para a evolução da ferramenta incluem:

* **Módulo de Análise Ortogonal (Inside-Out):** Integração das bibliotecas `PyPDF2` ou `pdfplumber` para realizar *scraping* automático do site da CVM, baixando Releases de Resultados e extraindo a visão da administração (Notas Explicativas) para cruzar com as notícias de mercado.
* **Ajuste Dinâmico de Risco (WACC):** Atualmente a IA atua apenas na taxa de crescimento. O próximo nível envolve treinar o LLM para ler o cenário macroeconômico (Decisões do COPOM, inflação) e ajustar dinamicamente o custo de capital (WACC) da empresa.
* **Banco de Dados Temporal:** Conectar a pipeline a um banco SQL (como o PostgreSQL) para registrar diariamente a pontuação de sentimento gerada pelo LLM, criando gráficos históricos de "Sentimento vs. Preço da Ação".

---

## 👨‍💻 Autor

**Wilton Marques**
*Engenheiro de Dados & Entusiasta de Finanças Quantitativas*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/wilton-marques-do-amaral-a84a27192)

> *Disclaimer: Este é um projeto de Engenharia de Dados voltado para portfólio. As análises e valores gerados pela Inteligência Artificial não constituem recomendação de compra, venda ou manutenção de ativos financeiros.*
