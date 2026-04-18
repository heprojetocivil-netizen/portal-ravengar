import streamlit as st
from groq import Groq

st.set_page_config(page_title="Gabinete de Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    .stApp p, .stApp span, .stApp label, h1, h2, h3 { color: #000000 !important; }
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
    }
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        color: #000000 !important;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def consultar_ravengar(sistema, pergunta, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro: {str(e)}"

with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")

st.markdown("<h1 style='text-align: center;'>🔮 Gabinete de Ravengar</h1>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção"])

with t1:
    pergunta_ora = st.text_area("O que as sombras revelam?", key="ora_input")
    if st.button("PROFERIR VEREDITO"):
        if chave_api:
            st.markdown(f"<div class='ravengar-card'>{consultar_ravengar('Você é o Ravengar.', pergunta_ora, chave_api)}</div>", unsafe_allow_html=True)

with t2:
    texto_dec = st.text_area("Insira o enigma:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            st.markdown(f"<div class='ravengar-card'>{consultar_ravengar('Você é o Ravengar, decifrador.', texto_dec, chave_api)}</div>", unsafe_allow_html=True)

with t3:
    st.markdown("### 🔥 Investigação de Intenção Real")
    nome_alvo = st.text_input("Nome do alvo:", key="nome_alvo")
    comportamento = st.text_area("Descreva a atitude suspeita:", key="comp_input")

    if st.button("DEVASSAR INTENÇÃO"):
        if chave_api and comportamento:
            res_inicial = consultar_ravengar(f"Você é o Ravengar. Analise {nome_alvo}.", comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]

    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            classe = "ravengar-card" if msg['role'] == "ravengar" else ""
            st.markdown(f"<div class='{classe}'>{'🔮' if msg['role']=='ravengar' else '👤'} {msg['content']}</div>", unsafe_allow_html=True)
        
        with st.form(key="form_chat", clear_on_submit=True):
            resp = st.text_input("Sua resposta:")
            col1, col2 = st.columns(2)
            if col1.form_submit_button("ENVIAR") and resp:
                st.session_state['historico'].append({"role": "user", "content": resp})
                hist = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state['historico']])
                st.session_state['historico'].append({"role": "ravengar", "content": consultar_ravengar("Ravengar", hist, chave_api)})
                st.rerun()
            if col2.form_submit_button("🔄 RESET"):
                del st.session_state['historico']
                st.rerun()