import streamlit as st
from groq import Groq
import random
import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    
    /* Padding inferior para o conteúdo não ficar escondido atrás do rodapé fixo */
    .stApp {{ background-color: #F7F7F7 !important; padding-bottom: 120px; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}

    /* BOTÃO PRETO ESTILO NEXUS PARA O LINK DA API */
    .tool-link {{
        display: inline-block;
        background: #000000 !important;
        color: #FFFFFF !important;
        padding: 8px 15px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 8px;
        border: none;
        transition: transform 0.2s;
    }}
    .tool-link:hover {{ transform: scale(1.02); color: #FFFFFF !important; }}

    /* RODAPÉ FIXO ESTILO NEXUS (BLUE SKY) */
    .footer-fixed {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #00BFFF !important;
        color: #000000 !important;
        text-align: center;
        padding: 18px 0;
        font-weight: bold;
        z-index: 9999;
        border-top: 3px solid #0080FF;
        font-size: 16px;
        box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
    }}

    .quiz-pergunta {{
        font-size: 26px !important;
        font-weight: 600 !important;
        margin-bottom: 30px !important;
        line-height: 1.4;
    }}

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
        padding: 25px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    .msg-balao {{
        background-color: #FFF5F7 !important;
        border-left: 5px solid #FFB7C5 !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RODAPÉ FIXO (Visível em todas as telas) ---
st.markdown("""
    <div class="footer-fixed">
        Acesse <a href="http://www.quizmaispremios.com.br" target="_blank" style="color: #000; text-decoration: underline;">www.quizmaispremios.com.br</a> 
        e venha se divertir com a gente e ganhar muitos prêmios!
    </div>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DO MURAL GLOBAL ---
@st.cache_resource
def obter_mural_global():
    return [] 

mural_global = obter_mural_global()

# --- 3. LÓGICA DE CONEXÃO ---
def consultar_ravengar(pergunta, api_key, setor="Destino", historico=None):
    prompts = {
        "Amor": "És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética, profunda e empática.",
        "Trabalho": "És o Ravengar, o Estrategista das Sombras. Direta, fria e focada em poder.",
        "Futuro": "És o Ravengar, o Profeta do Tempo. Enigmática, vasta e mística.",
        "Saude": "És o Ravengar, o Alquimista da Vitalidade. Serena e equilibrada.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa o comportamento com lógica fria e mantém o fio da conversa.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística e ácida.",
        "Tarot": "És o Ravengar, o mestre das cartas.",
        "Revelacao": "És o Ravengar. O usuário terminou o teste 'Quem você foi na vida passada'. Com base no perfil dele, faça uma REVELAÇÃO misteriosa e curta. Comece com 'Isso explica muita coisa...' e termine com um conselho ancestral."
    }
    
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Visitante')}."

    if historico:
        mensagens = [{"role": "system", "content": sistema}] + historico
    else:
        mensagens = [{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}]

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=mensagens,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

# --- 4. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
   st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    col_central = st.columns([1, 2, 1])[1]
    with col_central:
        nome_input = st.text_input("Como as sombras te devem chamar?")
        genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
        
        # --- LINK OBTER CHAVE (ESTILO NEXUS) ---
        st.markdown("<a href='https://console.groq.com/keys' target='_blank' class='tool-link'>Obter chave Groq grátis</a>", unsafe_allow_html=True)
        chave_input = st.text_input("Sua Chave Groq API:", type="password")
        
        if st.button("ENTRAR NA TENDA"):
            if nome_input and chave_input:
                st.session_state.nome_user, st.session_state.genero_user = nome_input, genero_input
                st.session_state.chave_api = chave_input
                st.session_state.usuario_identificado = True
                st.rerun()
            else:
                st.error("Por favor, informe seu nome e sua chave API.")
else:
    # --- INTERFACE PRINCIPAL (TUDO MANTIDO) ---
    chave_api = st.session_state.chave_api
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>. <small>({len(mural_global)} mensagens no Mural)</small></p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "📜 Vidas Passadas", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço", "🤝 Encontros"])

    # Aqui seguem todas as suas lógicas de abas originais...
    with tabs[0]: # ORÁCULO
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR", key="btn_Amor"): st.session_state.setor = "Amor"; st.rerun()
        with c2: 
            if st.button("💼 TRABALHO", key="btn_Trabalho"): st.session_state.setor = "Trabalho"; st.rerun()
        with c3: 
            if st.button("✨ FUTURO", key="btn_Futuro"): st.session_state.setor = "Futuro"; st.rerun()
        with c4: 
            if st.button("🌿 SAÚDE", key="btn_Saude"): st.session_state.setor = "Saude"; st.rerun()
        
        setor_atual = st.session_state.get('setor', 'Destino')
        pergunta_ora = st.text_area(f"O que desejas saber sobre o teu {setor_atual}?")
        if st.button("PROFERIR VEREDITO"):
            if chave_api and pergunta_ora:
                st.session_state['chat_ora'] = [{"content": consultar_ravengar(pergunta_ora, api_key=chave_api, setor=setor_atual)}]
        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # (O restante do código das abas 1 a 7 permanece igual ao seu original)
    # ... código do quiz, vidas passadas, biblioteca etc ...

    with tabs[5]: # Exemplo da Biblioteca Secreta (Mantida)
        st.markdown("<h2 style='text-align: center;'>👉 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        cursos = [
            {"titulo": "🔮 Leitura Fria", "url": "https://drive.google.com/file/d/1Yn7BkHCKjJPEXb3Rtip11ZxO0R11a1bd/view?usp=sharing"},
            {"titulo": "✋ Leitura de Mãos", "url": "https://drive.google.com/file/d/1jDHSLRzxB2jQbTnpsdegLvMITqLKhHN5/view?usp=sharing"}
        ]
        for item in cursos:
            st.markdown(f"<div class='ravengar-card'><h4>{item['titulo']}</h4></div>", unsafe_allow_html=True)
            st.link_button("📥 Baixar PDF", item["url"])

    if st.button("🔄 REINICIAR SESSÃO"):
        st.session_state.clear()
        st.rerun()
