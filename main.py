import streamlit as st
from groq import Groq
import random
import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    /* Remove completamente o header e a barra lateral */
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
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
        transition: all 0.3s ease;
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

    .biblioteca-card {{
        background-color: #FFFFFF !important;
        border: 1px solid #FFD1DC !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DO MURAL GLOBAL ---
@st.cache_resource
def obter_mural_global():
    return [] 

mural_global = obter_mural_global()

# --- 3. LÓGICA DE CONEXÃO ---
def consultar_ravengar(pergunta, api_key, setor="Destino"):
    prompts = {
        "Amor": "És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética, profunda e empática.",
        "Trabalho": "És o Ravengar, o Estrategista das Sombras. Tua linguagem é direta e focada em poder.",
        "Futuro": "És o Ravengar, o Profeta do Tempo. Tua linguagem é enigmática e mística.",
        "Saude": "És o Ravengar, o Alquimista da Vitalidade. Tua linguagem é serena.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério e sabedoria ancestral.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa o comportamento com precisão cirúrgica.",
        "Noticias": "És o Ravengar. Atuas como um curador de informações místicas.",
        "Tarot": "És o Ravengar, o mestre das cartas. Interpretas o Tarot de forma curta."
    }
    
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Visitante')}."

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
           messages=[{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}],
           model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: Verifique se a sua chave está correta."

# --- 4. IDENTIFICAÇÃO E CHAVE API (TELA DE ENTRADA) ---
if 'usuario_identificado' not in st.session_state:
   st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    col_central = st.columns([1, 2, 1])[1]
    with col_central:
        nome_input = st.text_input("Como as sombras te devem chamar?")
        genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
        chave_input = st.text_input("Digite sua Chave Groq API para entrar:", type="password")
        
        if st.button("ENTRAR NA TENDA"):
            if nome_input and chave_input:
                st.session_state.nome_user = nome_input
                st.session_state.genero_user = genero_input
                st.session_state.chave_api = chave_input
                st.session_state.usuario_identificado = True
                st.rerun()
            else:
                st.warning("É necessário informar o nome e a chave API para despertar o Oráculo.")
else:
    # --- INTERFACE PRINCIPAL ---
    chave_api = st.session_state.chave_api
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço", "🤝 Encontros"])

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
            if pergunta_ora:
                st.session_state['chat_ora'] = [{"content": consultar_ravengar(pergunta_ora, chave_api, setor_atual)}]
        if 'chat_ora' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{st.session_state['chat_ora'][0]['content']}</div>", unsafe_allow_html=True)

    with tabs[6]: # ENCONTROS
        st.markdown("### 💬 Mural de Almas")
        for m in reversed(mural_global[-10:]):
            st.markdown(f"<div class='msg-balao'><b>{m['usuario']}</b>: {m['texto']}</div>", unsafe_allow_html=True)
        msg_input = st.text_input("Manifestar:")
        if st.button("LANÇAR AO MURAL"):
            if msg_input:
                mural_global.append({"usuario": st.session_state.nome_user, "texto": msg_input, "hora": datetime.datetime.now().strftime("%H:%M")})
                st.rerun()
    
    if st.button("🚪 SAIR E LIMPAR SESSÃO"):
        st.session_state.clear()
        st.rerun()

    # --- 6. RODAPÉ ORIGINAL (MANTIDO INTACTO) ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Venha se divertir e concorrer a muitos prêmios com a gente.<br>"
        "<a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold; text-decoration: none;'>"
        "www.quizmaispremios.com.br</a>"
        "</div>", 
        unsafe_allow_html=True
    )
