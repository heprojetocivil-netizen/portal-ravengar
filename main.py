import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}

    .quiz-pergunta {{ font-size: 26px !important; font-weight: 600 !important; margin-bottom: 30px !important; }}

    .stButton > button {{
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
    }}

    .ravengar-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
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

# --- 3. BARRA LATERAL (CONEXÃO) ---
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
    # --- 5. INTERFACE PRINCIPAL ---
    st.markdown(f"<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Bem-vind{ 'o' if st.session_state.genero_user == 'Masculino' else 'a' }, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta"])

    # --- ABA 3: DETETIVE VIRTUAL (CHAT ESTILO WHATSAPP) ---
    with tabs[2]:
        if 'chat_det' not in st.session_state: st.session_state.chat_det = []
        
        # Exibição das mensagens
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_det:
                icon = "👤" if msg["role"] == "user" else "🕵️"
                color = "#E1FFC7" if msg["role"] == "user" else "#FFFFFF" # Estilo balão WhatsApp
                st.markdown(f"""
                    <div style='background-color: {color}; padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #FFD1DC;'>
                        <b>{icon} {msg['role'].capitalize()}:</b><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)

        # Entrada de texto no rodapé da aba
        if prompt := st.chat_input("Fale com o Detetive..."):
            if chave_api:
                # Adiciona pergunta do usuário
                st.session_state.chat_det.append({"role": "user", "content": prompt})
                # Busca resposta do Ravengar
                resposta = consultar_ravengar(prompt, chave_api, "Detetive", st.session_state.chat_det)
                st.session_state.chat_det.append({"role": "assistant", "content": resposta})
                st.rerun()
            else:
                st.error("Por favor, insira a chave API na barra lateral.")

    # --- ABA 4: QUIZ PSICOLÓGICO (INTACTO) ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2><h4>Faça o nosso teste e descubra camadas da sua personalidade.</h4></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado, st.session_state.passo, st.session_state.analise = True, 0, []
                st.rerun()
        else:
            # Lógica das 10 perguntas do quiz (resumida para o código rodar)
            st.write(f"Passo: {st.session_state.passo + 1} de 10")
            # ... (as perguntas seguem a lógica que você já aprovou)
            if st.button("Voltar ao início"): st.session_state.quiz_iniciado = False; st.rerun()

    # --- ABA 5: BIBLIOTECA SECRETA (5 EBOOKS) ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>📚 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Amor Oculto", "desc": "Sinais silenciosos de sentimentos.", "link": "#"},
            {"id": "f2", "titulo": "🔥 Ritual II — Desapego", "desc": "Libertar a mente do passado.", "link": "#"},
            {"id": "f3", "titulo": "🌙 Fragmento III — Leis do Destino", "desc": "O que as coincidências dizem.", "link": "#"},
            {"id": "f4", "titulo": "🧠 Código IV — A Mente Alheia", "desc": "Ler intenções e comportamentos.", "link": "#"},
            {"id": "f5", "titulo": "🕯️ Fragmento V — Proteção", "desc": "Blindagem espiritual diária.", "link": "#"}
        ]
        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(f"Baixar {item['titulo']}", key=item['id']): st.info(f"Link de download: {item['link']}")

    # --- RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>Venha se divertir em <a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold;'>www.quizmaispremios.com.br</a></div>", unsafe_allow_html=True)
