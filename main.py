import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    /* Estilo dos balões de chat */
    .chat-bubble {{
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #FFD1DC;
        max-width: 80%;
    }}
    .user-bubble {{ background-color: #E1FFC7; margin-left: auto; }}
    .ravengar-bubble {{ background-color: #FFFFFF; margin-right: auto; }}
    
    .stButton > button {{
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 50px;
    }}
    .biblioteca-card {{
        background-color: #FFFFFF !important;
        border: 1px solid #FFD1DC !important;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE IA COM MEMÓRIA ---
def consultar_ravengar(pergunta, api_key, setor, historico):
    prompt_sistema = f"És o Ravengar ({setor}). Nome do consulente: {st.session_state.get('nome_user', 'Desconhecido')}."
    
    mensagens = [{"role": "system", "content": prompt_sistema}]
    for msg in historico:
        role = "assistant" if msg["role"] == "assistant" else "user"
        mensagens.append({"role": role, "content": msg["content"]})
    mensagens.append({"role": "user", "content": pergunta})

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(messages=mensagens, model="llama-3.3-70b-versatile")
        return completion.choices[0].message.content
    except Exception as e:
        return f"A conexão mística falhou: {str(e)}"

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")
    if st.button("🔄 REINICIAR SESSÃO"):
        st.session_state.clear()
        st.rerun()

# --- 4. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    nome_input = st.text_input("Como as sombras te devem chamar?")
    genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
    if st.button("ENTRAR NA TENDA"):
        if nome_input:
            st.session_state.nome_user = nome_input
            st.session_state.genero_user = genero_input
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    st.markdown(f"<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Bem-vindo, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta"])

    # --- ABA 3: DETETIVE VIRTUAL (CHAT CONTÍNUO) ---
    with tabs[2]:
        if 'chat_det' not in st.session_state: st.session_state.chat_det = []
        
        # Exibir o histórico de chat
        for msg in st.session_state.chat_det:
            classe = "user-bubble" if msg["role"] == "user" else "ravengar-bubble"
            label = "👤 Você" if msg["role"] == "user" else "🕵️ Detetive Ravengar"
            st.markdown(f"<div class='chat-bubble {classe}'><b>{label}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

        # Entrada de texto (Chat Input)
        if prompt := st.chat_input("Diga ao Detetive o que aconteceu..."):
            if chave_api:
                st.session_state.chat_det.append({"role": "user", "content": prompt})
                res = consultar_ravengar(prompt, chave_api, "Detetive", st.session_state.chat_det)
                st.session_state.chat_det.append({"role": "assistant", "content": res})
                st.rerun()
            else:
                st.error("Insira a chave API na barra lateral.")

    # --- ABA 4: QUIZ (RESTAURADO) ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center;'><h2>Você acha que se conhece bem? 🤔</h2></div>", unsafe_allow_html=True)
            if st.button("INICIAR QUIZ"):
                st.session_state.quiz_iniciado = True
                st.rerun()
        else:
            st.write("O Quiz está ativo. Responda às questões para o veredito.")
            if st.button("Reiniciar Quiz"): st.session_state.quiz_iniciado = False; st.rerun()

    # --- ABA 5: BIBLIOTECA (5 EBOOKS) ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>📚 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        ebooks = [
            "❤️ Fragmento I — Amor Oculto", "🔥 Ritual II — Desapego", 
            "🌙 Fragmento III — Leis do Destino", "🧠 Código IV — A Mente Alheia", 
            "🕯️ Fragmento V — Proteção Energética"
        ]
        for livro in ebooks:
            st.markdown(f"<div class='biblioteca-card'><h4>{livro}</h4><p>Conhecimento guardado para a sua evolução.</p></div>", unsafe_allow_html=True)
            st.button(f"Aceder a {livro.split('—')[0]}", key=livro)

    # --- RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center;'><a href='http://www.quizmaispremios.com.br'>www.quizmaispremios.com.br</a></div>", unsafe_allow_html=True)
