import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
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

# --- 2. LÓGICA DE CONEXÃO ---
def consultar_ravengar(sistema, pergunta, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")

# --- 4. INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>🔮 Gabinete de Ravengar</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção"])

# --- ABA 1 E 2 (INTACTAS) ---
with tab1:
    st.markdown("### Selecione a Esfera")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("❤️ AMOR"): st.session_state.setor = "Amor"
    with c2: 
        if st.button("💼 TRABALHO"): st.session_state.setor = "Trabalho"
    with c3: 
        if st.button("⚖️ EMPREGO"): st.session_state.setor = "Emprego"
    with c4: 
        if st.button("🌿 SAÚDE"): st.session_state.setor = "Saúde"
    
    setor = st.session_state.get('setor', 'Destino')
    st.write(f"Energia atual: **{setor}**")
    pergunta_ora = st.text_area("O que as sombras devem revelar?", key="ora_input")
    if st.button("PROFERIR VEREDITO"):
        if chave_api:
            res = consultar_ravengar(f"Você é o Ravengar. Responda sobre {setor}.", pergunta_ora, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 👁️ O Decifrador")
    texto_dec = st.text_area("Insira o enigma, sonho ou mensagem:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            res = consultar_ravengar("Você é o Ravengar, decifrador de símbolos.", texto_dec, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

# --- ABA 3: TESTE DE INTENÇÃO (SISTEMA DE CHAT CORRIGIDO) ---
with tab3:
    st.markdown("### 🔥 Teste de Intenção Real")
    
    col_a, col_b = st.columns(2)
    with col_a: nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo")
    with col_b: genero = st.radio("Essa pessoa é:", ["Homem", "Mulher"])
    
    comportamento = st.text_area("Descreva o comportamento suspeito:", key="comp_input")

    # Botão para a análise inicial
    if st.button("DEVASSAR INTENÇÃO"):
        if not chave_api or not comportamento:
            st.error("Preencha a chave e o comportamento.")
        else:
            prompt_init = f"Você é o Ravengar. Analise as intenções de {nome_alvo}. Termine com uma pergunta curta e provocativa."
            res_inicial = consultar_ravengar(prompt_init, comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]

    # Se já começou a conversa, mostra o chat
    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            if msg['role'] == "ravengar":
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"👤 **Você:** {msg['content']}")

        # FORMULÁRIO: Garante que o campo limpe sozinho e o Ravengar não fale sozinho
        with st.form(key="form_conversa", clear_on_submit=True):
            resp_usuario = st.text_input("Sua resposta para o Ravengar:")
            col1, col2 = st.columns(2)
            with col1:
                enviar = st.form_submit_button("ENVIAR RESPOSTA")
            with col2:
                reset = st.form_submit_button("🔄 RESETAR CONVERSA")

        if enviar and resp_usuario:
            # 1. Adiciona o que você escreveu no histórico
            st.session_state['historico'].append({"role": "user", "content": resp_usuario})
            
            # 2. Ravengar gera a resposta baseada em tudo o que foi dito
            historico_full = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state['historico']])
            prompt_dialogo = f"Você é o Ravengar. Continue o diálogo. Histórico: {historico_full}"
            
            nova_res = consultar_ravengar(prompt_dialogo, "Responda agora.", chave_api)
            st.session_state['historico'].append({"role": "ravengar", "content": nova_res})
            st.rerun()

        if reset:
            del st.session_state['historico']
            st.rerun()
