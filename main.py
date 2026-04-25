import streamlit as st
from groq import Groq
import random
import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap');

    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    :root {
        --preto: #0A0A0F;
        --roxo-escuro: #1A0A2E;
        --roxo: #6B21A8;
        --roxo-claro: #A855F7;
        --ouro: #D4AF37;
        --ouro-claro: #F5D97A;
        --rosa: #FFB7C5;
        --branco: #F8F4FF;
        --cinza: #C4B5D4;
    }

    html, body, .stApp {
        background-color: var(--roxo-escuro) !important;
        background-image:
            radial-gradient(ellipse at 20% 20%, rgba(107,33,168,0.3) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(212,175,55,0.1) 0%, transparent 50%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236B21A8' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        font-family: 'Raleway', sans-serif !important;
        padding-bottom: 100px;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: var(--ouro) !important;
        letter-spacing: 2px;
    }

    p, label, div, span, .stMarkdown {
        color: var(--branco) !important;
        font-family: 'Raleway', sans-serif !important;
    }

    /* Corrige elementos internos do Streamlit que ficam brancos */
    [data-testid="stExpander"],
    [data-testid="stExpanderDetails"],
    .stAlert,
    .stInfo,
    [data-testid="stNotification"],
    [data-baseweb="notification"],
    [data-baseweb="toast"],
    [data-testid="element-container"],
    .element-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    section[data-testid="stSidebar"],
    [data-testid="stForm"],
    .stForm,
    div[class*="block-container"],
    div[class*="stColumn"],
    [data-testid="column"] {
        background-color: transparent !important;
    }

    /* Força texto visível em qualquer fundo claro gerado pelo Streamlit */
    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    [data-baseweb="textarea"] *,
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"] {
        color: #1A0A2E !important;
        background-color: #F8F4FF !important;
    }

    /* Dropdown e opções do selectbox */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #1A0A2E !important;
    }
    [data-baseweb="menu"] li,
    [role="option"] {
        color: var(--branco) !important;
        background-color: #1A0A2E !important;
    }
    [data-baseweb="menu"] li:hover,
    [role="option"]:hover {
        background-color: #6B21A8 !important;
    }

    /* Radio buttons */
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] div,
    [data-testid="stRadio"] p,
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {
        color: var(--branco) !important;
    }

    /* Métricas */
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] div {
        color: var(--cinza) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--ouro) !important;
    }

    /* Date input */
    input[type="date"],
    [data-baseweb="datepicker"] input {
        color: var(--branco) !important;
        background-color: rgba(255,255,255,0.05) !important;
    }

    /* Number input */
    input[type="number"] {
        color: var(--branco) !important;
        background-color: rgba(255,255,255,0.05) !important;
    }

    /* Spinner texto */
    [data-testid="stSpinner"] p {
        color: var(--ouro) !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(255,255,255,0.05) !important;
        color: var(--branco) !important;
        border: 1px solid rgba(212,175,55,0.3) !important;
    }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #1A0A2E, #0F0520) !important;
        color: var(--ouro) !important;
        border: 1px solid var(--ouro) !important;
    }

    /* Link button */
    [data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, var(--roxo), #4C1D95) !important;
        color: var(--ouro-claro) !important;
        border: 1px solid var(--ouro) !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-family: 'Cinzel', serif !important;
        text-decoration: none !important;
    }

    /* Tabs conteúdo */
    [data-baseweb="tab-panel"] {
        background-color: transparent !important;
    }

    /* INPUTS - força fundo escuro em todos os campos */
    input, textarea, select,
    .stTextInput input,
    .stTextArea textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    [data-baseweb="base-input"],
    [data-baseweb="base-input"] input,
    [data-baseweb="base-input"] textarea,
    [data-baseweb="textarea"] textarea,
    [data-baseweb="input"] input,
    [class*="st-"] input,
    [class*="st-"] textarea {
        background-color: rgba(26, 10, 46, 0.95) !important;
        border: 1px solid rgba(212,175,55,0.4) !important;
        color: #F8F4FF !important;
        border-radius: 10px !important;
        caret-color: #D4AF37 !important;
    }

    /* Placeholder */
    input::placeholder, textarea::placeholder {
        color: rgba(196, 181, 212, 0.5) !important;
    }

    /* Wrapper dos inputs */
    [data-baseweb="base-input"],
    [data-baseweb="textarea"],
    [data-baseweb="input"] {
        background-color: rgba(26, 10, 46, 0.95) !important;
        border-color: rgba(212,175,55,0.4) !important;
    }

    /* Chat input area */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] textarea {
        background-color: rgba(26, 10, 46, 0.95) !important;
        color: #F8F4FF !important;
        border-color: rgba(212,175,55,0.4) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--roxo), #4C1D95) !important;
        color: var(--ouro-claro) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
        border: 1px solid var(--ouro) !important;
        border-radius: 10px !important;
        width: 100%;
        padding: 12px !important;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--ouro), #B8860B) !important;
        color: var(--preto) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212,175,55,0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 15px;
        padding: 5px;
        gap: 5px;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--cinza) !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.75em !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--roxo), #4C1D95) !important;
        color: var(--ouro) !important;
        border-bottom: 2px solid var(--ouro) !important;
    }

    .card-ravengar {
        background: linear-gradient(135deg, rgba(26,10,46,0.95), rgba(10,10,15,0.95));
        border: 1px solid rgba(212,175,55,0.3);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 15px;
        box-shadow: 0 4px 30px rgba(107,33,168,0.2);
        backdrop-filter: blur(10px);
    }

    .card-ouro {
        background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(245,217,122,0.05));
        border: 1px solid var(--ouro);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 15px;
    }

    .card-resultado {
        background: linear-gradient(135deg, #1A0A2E, #0F0520);
        border: 2px solid var(--ouro);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 40px rgba(212,175,55,0.15), inset 0 0 40px rgba(107,33,168,0.1);
    }

    .pergunta-quiz {
        font-family: 'Cinzel', serif !important;
        font-size: 1.2em !important;
        color: var(--ouro-claro) !important;
        margin: 20px 0 !important;
        line-height: 1.6;
        text-align: center;
    }

    .contexto-quiz {
        background: rgba(107,33,168,0.2);
        border-left: 3px solid var(--roxo-claro);
        padding: 12px 18px;
        border-radius: 8px;
        font-style: italic;
        color: var(--cinza) !important;
        margin-bottom: 15px;
        font-size: 0.9em;
    }

    .msg-balao {
        background: rgba(107,33,168,0.15);
        border-left: 3px solid var(--rosa);
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .biblioteca-card {
        background: linear-gradient(135deg, rgba(26,10,46,0.9), rgba(10,10,15,0.9));
        border: 1px solid rgba(212,175,55,0.2);
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 12px;
        transition: border-color 0.3s;
    }

    .badge-perfil {
        display: inline-block;
        background: linear-gradient(135deg, var(--ouro), #B8860B);
        color: var(--preto) !important;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: 700;
        font-family: 'Cinzel', serif !important;
        margin-bottom: 10px;
    }

    .footer-nexus {
        position: fixed;
        left: 0; bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, var(--roxo-escuro), #2D0A5A, var(--roxo-escuro));
        border-top: 1px solid var(--ouro);
        color: var(--ouro) !important;
        text-align: center;
        padding: 12px 0;
        font-family: 'Cinzel', serif;
        font-size: 13px;
        z-index: 9999;
        letter-spacing: 1px;
    }

    .titulo-secao {
        font-family: 'Cinzel', serif;
        color: var(--ouro);
        font-size: 1.5em;
        text-align: center;
        margin: 20px 0;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .estrelas {
        color: var(--ouro);
        font-size: 1.2em;
        letter-spacing: 4px;
    }

    .tool-link {
        display: inline-block;
        background: var(--ouro) !important;
        color: var(--preto) !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        font-family: 'Cinzel', serif;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }

    .progresso-bar-bg {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        height: 6px;
        margin: 10px 0 20px 0;
        overflow: hidden;
    }

    .stRadio > div {
        background: transparent !important;
    }

    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: var(--ouro-claro) !important;
        font-family: 'Cinzel', serif !important;
        font-size: 0.85em !important;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: var(--ouro) !important;
        font-family: 'Cinzel', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- RODAPÉ FIXO ---
st.markdown("""
    <div class="footer-nexus">
        ✦ Acesse <a href="http://www.quizmaispremios.com.br" target="_blank" style="color: #F5D97A; text-decoration: underline;">www.quizmaispremios.com.br</a> 
        — divirta-se e ganhe prêmios! ✦
    </div>
""", unsafe_allow_html=True)

# --- MURAL GLOBAL ---
@st.cache_resource
def obter_mural_global():
    return []

mural_global = obter_mural_global()

# --- FUNÇÃO CENTRAL DE IA ---
def consultar_ravengar(pergunta, api_key, setor="Destino", historico=None):
    prompts = {
        "Amor": "És o Ravengar, Guardião dos Afetos. Linguagem poética, profunda e empática.",
        "Trabalho": "És o Ravengar, Estrategista das Sombras. Direta, fria e focada em poder.",
        "Futuro": "És o Ravengar, Profeta do Tempo. Enigmática, vasta e mística.",
        "Saude": "És o Ravengar, Alquimista da Vitalidade. Serena e equilibrada.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério.",
        "Detetive": "És o Ravengar, Detetive Virtual. Analisa comportamento com lógica fria.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística e ácida.",
        "Tarot": "És o Ravengar, mestre das cartas.",
        "Revelacao": "És o Ravengar. Faça uma REVELAÇÃO mística e curta baseada no perfil. Comece com 'Isso explica muita coisa...' e termine com conselho ancestral.",
        "Quiz_Amor": "És o Ravengar, especialista em afetos e compatibilidade. Analisa o perfil de amor da pessoa com profundidade poética e precisão psicológica.",
        "Quiz_Trabalho": "És o Ravengar, oráculo das carreiras e talentos. Analisa vocação, força profissional e caminho ideal com autoridade e mistério.",
        "Quiz_Carreira": "És o Ravengar, guia das trajetórias profissionais. Revela o emprego/carreira ideal com base no perfil psicológico com precisão ancestral.",
        "Quiz_Personalidade": "És o Ravengar, conhecedor das almas. Desvenda a personalidade profunda com linguagem mística mas psicologicamente precisa.",
        "Quiz_Dinheiro": "És o Ravengar, guardião da prosperidade. Revela a relação da pessoa com dinheiro e seu potencial financeiro com sabedoria ancestral.",
        "Quiz_Proposito": "És o Ravengar, oráculo do propósito. Revela a missão de vida e propósito profundo com linguagem filosófica e mística.",
        "Quiz_Energia": "És o Ravengar, mestre das energias vitais. Analisa o tipo de energia da pessoa e como ela impacta o mundo ao redor.",
        "Numerologia": "És o Ravengar, mestre dos números sagrados. Interpreta a numerologia com profundidade mística e precisão.",
        "Horoscopo": "És o Ravengar, guardião dos astros. Faz previsões astrológicas com linguagem poética e mística.",
        "Meditacao": "És o Ravengar, guia espiritual. Cria meditações guiadas personalizadas com linguagem serena e poderosa.",
    }
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Visitante')}. Seja sempre em português do Brasil."

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

# --- FUNÇÃO UTILITÁRIA: renderizar quiz ---
def renderizar_quiz(chave, perguntas, setor_ia, titulo, descricao, icone, callback_resultado):
    if chave not in st.session_state:
        st.session_state[chave] = {"passo": 0, "pontos": {}, "respostas": []}

    estado = st.session_state[chave]

    if estado["passo"] == 0:
        st.markdown(f"<div class='card-resultado'><div style='font-size:3em'>{icone}</div><h2>{titulo}</h2><p style='color:#C4B5D4'>{descricao}</p></div>", unsafe_allow_html=True)
        if st.button(f"✦ INICIAR RITUAL ✦", key=f"iniciar_{chave}"):
            estado["passo"] = 1
            st.rerun()

    elif estado["passo"] <= len(perguntas):
        total = len(perguntas)
        atual = estado["passo"]
        pct = int((atual - 1) / total * 100)
        q = perguntas[atual - 1]

        st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:5px'><span style='color:#C4B5D4;font-size:0.8em'>Pergunta {atual} de {total}</span><span style='color:#D4AF37;font-size:0.8em'>{pct}%</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='progresso-bar-bg'><div style='width:{pct}%;height:6px;background:linear-gradient(90deg,#6B21A8,#D4AF37);border-radius:20px;transition:width 0.5s'></div></div>", unsafe_allow_html=True)

        if "contexto" in q:
            st.markdown(f"<div class='contexto-quiz'>✦ {q['contexto']}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='pergunta-quiz'>{q['p']}</div>", unsafe_allow_html=True)

        cols = st.columns(min(len(q['o']), 2))
        for i, (key_op, val_op) in enumerate(q['o'].items()):
            with cols[i % 2]:
                if st.button(val_op, key=f"{chave}_{atual}_{key_op}"):
                    for k, pts in q['pontos'].get(key_op, {key_op: 1}).items():
                        estado["pontos"][k] = estado["pontos"].get(k, 0) + pts
                    estado["respostas"].append({"pergunta": q["p"], "resposta": val_op, "simbolo": key_op})
                    estado["passo"] += 1
                    st.rerun()

    else:
        callback_resultado(estado, st.session_state.chave_api)
        if st.button(f"🔄 REPETIR RITUAL", key=f"reset_{chave}"):
            del st.session_state[chave]
            chaves_ia = [f"ia_{chave}", f"revelacao_{chave}"]
            for k in chaves_ia:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

# ============================================================
# IDENTIFICAÇÃO
# ============================================================
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align:center;font-size:2.5em'>🔮 TENDA DO RAVENGAR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#C4B5D4;font-style:italic'>O oráculo aguarda. As sombras guardam segredos. Você está pronto?</p>", unsafe_allow_html=True)
    st.markdown("<div class='estrelas' style='text-align:center'>✦ ✦ ✦</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("<div class='card-ouro'>", unsafe_allow_html=True)
        nome_input = st.text_input("Como as sombras te devem chamar?")
        genero_input = st.radio("O teu gênero:", ["Masculino", "Feminino"])
        st.markdown("<a href='https://console.groq.com/keys' target='_blank' class='tool-link'>⚡ Obter Chave Groq Grátis</a>", unsafe_allow_html=True)
        chave_input = st.text_input("Chave Groq API:", type="password")
        if st.button("✦ ENTRAR NA TENDA ✦"):
            if nome_input and chave_input:
                st.session_state.nome_user = nome_input
                st.session_state.genero_user = genero_input
                st.session_state.chave_api = chave_input
                st.session_state.usuario_identificado = True
                st.rerun()
            else:
                st.error("O oráculo precisa do seu nome e da chave mística.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    chave_api = st.session_state.chave_api
    nome = st.session_state.nome_user

    st.markdown(f"<h1 style='text-align:center'>🔮 TENDA DO RAVENGAR</h1>", unsafe_allow_html=True)
    qtd_almas = len(mural_global)
    texto_almas = f"{qtd_almas} almas" if qtd_almas > 0 else "nenhuma alma"
    st.markdown(f"<p style='text-align:center;color:#C4B5D4'>✦ Boas-vindas, <b style='color:#D4AF37'>{nome}</b> · {texto_almas} no Mural ✦</p>", unsafe_allow_html=True)

    tabs = st.tabs([
        "🔮 Oráculo",
        "📜 Vidas Passadas",
        "💘 Quiz Amor",
        "💼 Quiz Trabalho",
        "🚀 Quiz Carreira",
        "🧠 Quiz Personalidade",
        "💰 Quiz Dinheiro",
        "🌟 Quiz Propósito",
        "⚡ Quiz Energia",
        "👁️ Decifrador",
        "🕵️ Detetive",
        "🧘 Seu Espaço",
        "📚 Biblioteca",
        "🤝 Encontros",
    ])

    # ============================================================
    # TAB 0: ORÁCULO
    # ============================================================
    with tabs[0]:
        st.markdown("<div class='titulo-secao'>O Oráculo Fala</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        botoes_setor = [("❤️ Amor", "Amor"), ("💼 Trabalho", "Trabalho"), ("✨ Futuro", "Futuro"), ("🌿 Saúde", "Saude")]
        for col, (label, setor) in zip([c1, c2, c3, c4], botoes_setor):
            with col:
                if st.button(label, key=f"btn_{setor}"):
                    st.session_state.setor = setor
                    st.rerun()

        setor_atual = st.session_state.get('setor', 'Destino')
        st.markdown("<br>", unsafe_allow_html=True)
        pergunta_ora = st.text_area(f"O que desejas saber?", placeholder="Faça sua pergunta ao oráculo...", key="input_oraculo")
        if st.button("✦ PROFERIR VEREDITO ✦"):
            if chave_api and pergunta_ora:
                with st.spinner("O oráculo consulta as sombras..."):
                    st.session_state['chat_ora'] = consultar_ravengar(pergunta_ora, api_key=chave_api, setor=setor_atual)
        if 'chat_ora' in st.session_state:
            st.markdown(f"<div class='card-ravengar'><div style='color:#D4AF37;font-family:Cinzel,serif;margin-bottom:10px'>🔮 Ravengar fala:</div>{st.session_state['chat_ora']}</div>", unsafe_allow_html=True)

        # Numerologia
        st.markdown("---")
        st.markdown("<div class='titulo-secao' style='font-size:1.1em'>🔢 Numerologia do Nome</div>", unsafe_allow_html=True)
        nome_num = st.text_input("Digite seu nome completo:", key="nome_numerologia")
        data_num = st.date_input("Data de nascimento:", key="data_numerologia")
        if st.button("✦ REVELAR MEU NÚMERO ✦"):
            if nome_num:
                with st.spinner("Calculando vibração numerológica..."):
                    prompt_num = f"Faça uma leitura numerológica completa de {nome_num}, nascido(a) em {data_num}. Calcule o número do caminho de vida, número da expressão, número da alma e número da personalidade. Seja mísrico e profundo."
                    st.session_state['num_result'] = consultar_ravengar(prompt_num, chave_api, "Numerologia")
        if 'num_result' in st.session_state:
            st.markdown(f"<div class='card-ouro'>{st.session_state['num_result']}</div>", unsafe_allow_html=True)

        # Horóscopo personalizado
        st.markdown("---")
        st.markdown("<div class='titulo-secao' style='font-size:1.1em'>⭐ Horóscopo Personalizado</div>", unsafe_allow_html=True)
        signos = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem", "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
        signo_sel = st.selectbox("Seu signo solar:", signos, key="signo_sel")
        area_horo = st.selectbox("Área de interesse:", ["Amor", "Trabalho", "Saúde", "Finanças", "Família", "Espiritualidade"], key="area_horo")
        if st.button("✦ CONSULTAR OS ASTROS ✦"):
            with st.spinner("Lendo os astros..."):
                prompt_horo = f"Faça um horóscopo profundo e personalizado para {signo_sel} com foco em {area_horo}. Tom místico e revelador. Dê conselhos práticos embrulhados em linguagem ancestral."
                st.session_state['horo_result'] = consultar_ravengar(prompt_horo, chave_api, "Horoscopo")
        if 'horo_result' in st.session_state:
            st.markdown(f"<div class='card-ravengar'>{st.session_state['horo_result']}</div>", unsafe_allow_html=True)

    # ============================================================
    # TAB 1: VIDAS PASSADAS
    # ============================================================
    with tabs[1]:
        if 'jogo_vp' not in st.session_state:
            st.session_state.jogo_vp = {"passo": 0, "pontos": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}}

        vp = st.session_state.jogo_vp

        if vp["passo"] == 0:
            st.markdown("<div class='card-resultado'><div style='font-size:3em'>📜</div><h2>Quem Você Foi na Vida Passada?</h2><p style='color:#C4B5D4'>As sombras guardam memórias que sua mente consciente esqueceu. Vamos buscá-las.</p></div>", unsafe_allow_html=True)
            if st.button("✦ INICIAR REVELAÇÃO ✦"):
                vp["passo"] = 1
                st.rerun()

        elif vp["passo"] <= 7:
            perguntas_vp = [
                {"p": "Qual destes cenários te traz uma sensação estranha de 'já estive aqui'?", "o": {"A": "Uma sala de guerra estratégica", "B": "Um palco sob aplausos", "C": "Uma caravana sem destino", "D": "Um observatório solitário"}},
                {"p": "O que você mais valoriza em uma jornada?", "o": {"A": "O plano bem executado", "B": "O impacto deixado nas pessoas", "C": "A liberdade de mudar a rota", "D": "A compreensão dos sinais ocultos"}},
                {"p": "Como você lida com um novo grupo de pessoas?", "o": {"E": "Busco unir todos e criar harmonia", "F": "Prefiro ouvir e aprender tudo primeiro", "A": "Analiso quem é quem e as intenções", "B": "Tomo a frente naturalmente"}},
                {"p": "Qual o seu maior medo?", "o": {"C": "Ficar preso a uma rotina eterna", "D": "Ignorar um detalhe crucial", "E": "Ver o conflito separar as pessoas", "F": "Ficar na superfície do conhecimento"}},
                {"p": "Ao se deparar com uma injustiça, qual sua reação ancestral?", "o": {"A": "Punição imediata e justa", "E": "Diplomacia para acalmar os ânimos", "B": "Denúncia pública fervorosa", "D": "Observação fria para entender o motivo"}},
                {"p": "Se pudesse escolher um artefato antigo para carregar hoje:", "o": {"F": "Um pergaminho de sabedoria esquecida", "C": "Um mapa de terras nunca visitadas", "A": "Uma adaga de proteção leal", "B": "Um amuleto que atrai multidões"}},
                {"p": "Como você prefere terminar o seu dia?", "o": {"D": "Em silêncio, refletindo sobre o que vi", "F": "Estudando algo que me instruia", "E": "Rodeado de quem traz paz", "C": "Planejando o próximo destino"}},
            ]
            total = 7
            pct = int((vp["passo"] - 1) / total * 100)
            st.markdown(f"<div class='progresso-bar-bg'><div style='width:{pct}%;height:6px;background:linear-gradient(90deg,#6B21A8,#D4AF37);border-radius:20px'></div></div>", unsafe_allow_html=True)

            q = perguntas_vp[vp["passo"] - 1]
            st.markdown(f"<div class='pergunta-quiz'>{q['p']}</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (key, val) in enumerate(q['o'].items()):
                with cols[i % 2]:
                    if st.button(val, key=f"vp_{vp['passo']}_{key}"):
                        vp["pontos"][key] += 1
                        vp["passo"] += 1
                        st.rerun()
        else:
            vencedor = max(vp["pontos"], key=vp["pontos"].get)
            perfis = {
                "A": ("🎯 O Estrategista", "Você foi alguém que pensava à frente. Tomava decisões calculadas e raramente agia por impulso."),
                "B": ("🔥 O Influente", "Você foi alguém que impactava pessoas. Sua presença chamava atenção naturalmente."),
                "C": ("🌍 O Livre", "Você foi alguém que não aceitava limites. Sempre buscava novos caminhos e experiências."),
                "D": ("🧠 O Observador", "Você foi alguém que enxergava além. Percebia detalhes e intenções que outros ignoravam."),
                "E": ("💬 O Conector", "Você foi alguém que unia pessoas. Criava laços e resolvia conflitos com facilidade."),
                "F": ("📚 O Buscador", "Você foi alguém que buscava entender tudo. O conhecimento era parte da sua essência."),
            }
            titulo_p, desc_p = perfis[vencedor]
            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>{titulo_p.split()[0]}</div><h2>{titulo_p}</h2><p style='color:#C4B5D4;font-size:1.1em'>{desc_p}</p></div>", unsafe_allow_html=True)

            if 'revelacao_vp' not in st.session_state:
                with st.spinner("Conectando com suas vidas passadas..."):
                    st.session_state.revelacao_vp = consultar_ravengar(
                        f"Perfil de vida passada: {titulo_p} — {desc_p}. Faça uma leitura mística curta sobre como essa essência ancestral influencia o presente.",
                        chave_api, "Revelacao"
                    )
            st.markdown(f"<div class='card-ravengar'><p style='font-style:italic;color:#C4B5D4'>{st.session_state.revelacao_vp}</p></div>", unsafe_allow_html=True)

            if st.button("🔄 REPETIR RITUAL"):
                del st.session_state.jogo_vp
                if 'revelacao_vp' in st.session_state: del st.session_state.revelacao_vp
                st.rerun()

    # ============================================================
    # TAB 2: QUIZ AMOR — PARCEIRO(A) IDEAL
    # ============================================================
    with tabs[2]:
        perguntas_amor = [
            {"p": "Numa relação, o que você mais precisa sentir?", "contexto": "Pense nos seus relacionamentos mais marcantes...",
             "o": {"seg": "Segurança e estabilidade", "int": "Intensidade e paixão", "lib": "Liberdade e parceria", "con": "Conexão emocional profunda"},
             "pontos": {"seg": {"seg": 3, "est": 1}, "int": {"int": 3, "aven": 1}, "lib": {"lib": 3, "int": 1}, "con": {"emo": 3, "seg": 1}}},
            {"p": "Como você age quando se apaixona?", "contexto": "Seja honesto(a)...",
             "o": {"rapido": "Me entrego rapidamente", "devagar": "Me aproximo devagar, com cautela", "acao": "Demonstro através de ações", "palavras": "Expresso com palavras e carinho"},
             "pontos": {"rapido": {"int": 2, "emo": 1}, "devagar": {"seg": 2, "est": 1}, "acao": {"prat": 2, "seg": 1}, "palavras": {"emo": 2, "con": 1}}},
            {"p": "O que mais te incomoda em um parceiro(a)?", "contexto": "Pense nos seus maiores desgastes...",
             "o": {"cime": "Ciúme excessivo", "frio": "Frieza emocional", "depend": "Dependência", "infid": "Falta de comprometimento"},
             "pontos": {"cime": {"lib": 2, "int": 1}, "frio": {"emo": 2, "con": 1}, "depend": {"lib": 2, "aven": 1}, "infid": {"seg": 2, "est": 1}}},
            {"p": "Um final de semana romântico ideal seria:", "contexto": "Deixe seu coração escolher...",
             "o": {"viagem": "Uma viagem surpresa para lugar desconhecido", "casa": "Em casa, confortáveis e conectados", "jantar": "Um jantar sofisticado e conversa profunda", "aventura": "Uma aventura ao ar livre"},
             "pontos": {"viagem": {"aven": 3, "int": 1}, "casa": {"seg": 2, "emo": 1}, "jantar": {"con": 2, "int": 1}, "aventura": {"lib": 2, "aven": 1}}},
            {"p": "Como você prefere resolver conflitos no amor?", "contexto": "Cada um tem seu padrão...",
             "o": {"conv": "Conversa aberta e imediata", "tempo": "Preciso de tempo para processar", "abrac": "Um abraço vale mais que palavras", "escr": "Prefiro escrever o que sinto"},
             "pontos": {"conv": {"prat": 2, "int": 1}, "tempo": {"seg": 1, "est": 1}, "abrac": {"emo": 2, "seg": 1}, "escr": {"con": 2, "emo": 1}}},
            {"p": "O que mais te atrai em outra pessoa?", "contexto": "A primeira coisa que vem à mente...",
             "o": {"intelig": "Inteligência e profundidade", "humor": "Bom humor e leveza", "ambic": "Ambição e determinação", "cuidado": "Gentileza e cuidado"},
             "pontos": {"intelig": {"con": 2, "int": 1}, "humor": {"lib": 2, "aven": 1}, "ambic": {"prat": 2, "est": 1}, "cuidado": {"emo": 2, "seg": 1}}},
            {"p": "No amor, você é mais:", "contexto": "Seja sincero(a)...",
             "o": {"corac": "Coração — sigo o que sinto", "razao": "Razão — analiso antes de agir", "eqlib": "Equilíbrio entre os dois", "inst": "Instinto — confio no meu pressentimento"},
             "pontos": {"corac": {"emo": 2, "int": 1}, "razao": {"est": 2, "prat": 1}, "eqlib": {"seg": 2, "con": 1}, "inst": {"int": 2, "lib": 1}}},
        ]

        def resultado_amor(estado, api_key):
            pontos = estado["pontos"]
            perfis_amor = {
                "emo": ("💜 O Alma Gêmea Emocional", "Você busca conexão profunda, cumplicidade e alguém que entenda seu mundo interior sem julgamentos."),
                "int": ("🔥 O Amor Intenso", "Você é movido por paixão, atração magnética e intensidade. Quer sentir o amor em cada célula do corpo."),
                "seg": ("🏡 O Amor Seguro", "Você valoriza estabilidade, confiança e um amor que seja seu porto seguro no caos do mundo."),
                "lib": ("🌊 O Amor Livre", "Você precisa de um parceiro(a) que seja seu igual, respeite sua independência e cresça ao seu lado."),
                "aven": ("⚡ O Amor Aventureiro", "Você quer um parceiro que topie tudo, surpreenda e mantenha a chama acesa com novidade."),
                "con": ("🌙 O Amor Contemplativo", "Você busca profundidade intelectual e emocional — conversas que durem a madrugada e olhares que dizem tudo."),
                "prat": ("💎 O Amor Concreto", "Você se mostra amando através de ações. Quer alguém que construa algo real ao seu lado."),
                "est": ("⚖️ O Amor Equilibrado", "Você quer harmonia, maturidade e uma relação sólida baseada em respeito mútuo."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "emo"
            titulo_r, desc_r = perfis_amor.get(vencedor, ("💜 Perfil Único", "Seu perfil amoroso é singular e especial."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>💘</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_amor' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar analisa seu coração..."):
                    st.session_state.ia_quiz_amor = consultar_ravengar(
                        f"Perfil amoroso: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Descreva em detalhes: como é o(a) parceiro(a) ideal desta pessoa (personalidade, características), "
                        f"como este amor vai se manifestar na vida dela, e 3 conselhos para encontrá-lo. Tom místico e preciso.",
                        api_key, "Quiz_Amor"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_amor}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_amor", perguntas_amor, "Quiz_Amor", "Qual é o Seu Perfil no Amor?", "Descubra como você ama, o que você precisa e quem é o(a) parceiro(a) ideal para a sua alma.", "💘", resultado_amor)

    # ============================================================
    # TAB 3: QUIZ TRABALHO — AMBIENTE IDEAL
    # ============================================================
    with tabs[3]:
        perguntas_trabalho = [
            {"p": "Como você prefere trabalhar?", "contexto": "Pense em quando você rende mais...",
             "o": {"sozinho": "Sozinho, com foco total", "equipe": "Em equipe, colaborativamente", "lider": "Liderando e tomando decisões", "apoio": "Apoiando e executando com precisão"},
             "pontos": {"sozinho": {"ind": 3}, "equipe": {"col": 3}, "lider": {"lid": 3}, "apoio": {"exe": 3}}},
            {"p": "O que te dá mais satisfação no trabalho?", "contexto": "Seja honesto(a)...",
             "o": {"result": "Ver resultados concretos", "impac": "Impactar pessoas positivamente", "apren": "Aprender coisas novas sempre", "criat": "Criar e inovar livremente"},
             "pontos": {"result": {"prag": 2, "exe": 1}, "impac": {"hum": 3}, "apren": {"intel": 3}, "criat": {"cri": 3}}},
            {"p": "Qual ambiente de trabalho te energiza?", "contexto": "Onde você se sente no seu melhor...",
             "o": {"agito": "Dinâmico e acelerado", "silenc": "Calmo e organizado", "criativo": "Criativo e colorido", "natural": "Ao ar livre ou presença na natureza"},
             "pontos": {"agito": {"lid": 2, "cri": 1}, "silenc": {"ind": 2, "exe": 1}, "criativo": {"cri": 3}, "natural": {"lib": 3}}},
            {"p": "Diante de um problema no trabalho, você:", "contexto": "Sua reação natural...",
             "o": {"analisa": "Analisa dados antes de agir", "intuit": "Age por intuição e experiência", "consul": "Consulta a equipe para decidir junto", "busca": "Busca referências e aprende novo"},
             "pontos": {"analisa": {"intel": 2, "prag": 1}, "intuit": {"lid": 2, "cri": 1}, "consul": {"col": 3}, "busca": {"intel": 2, "ind": 1}}},
            {"p": "O que você NÃO suporta no ambiente de trabalho?", "contexto": "Seus maiores gatilhos profissionais...",
             "o": {"microg": "Microgerenciamento", "desor": "Desorganização e caos", "monot": "Monotonia e repetição", "conflit": "Conflitos e política interna"},
             "pontos": {"microg": {"ind": 2, "lib": 1}, "desor": {"exe": 2, "prag": 1}, "monot": {"cri": 2, "lib": 1}, "conflit": {"ind": 2, "intel": 1}}},
            {"p": "Qual seria seu maior legado profissional?", "contexto": "Pense no longo prazo...",
             "o": {"empresa": "Construir uma empresa de sucesso", "ajudar": "Ter ajudado muitas pessoas", "criar": "Ter criado algo que durou", "ensinar": "Ter ensinado e formado outros"},
             "pontos": {"empresa": {"lid": 2, "prag": 1}, "ajudar": {"hum": 3}, "criar": {"cri": 3}, "ensinar": {"hum": 2, "intel": 1}}},
        ]

        def resultado_trabalho(estado, api_key):
            pontos = estado["pontos"]
            perfis_trab = {
                "lid": ("👑 O Líder Natural", "Você nasceu para guiar. Seu melhor ambiente é onde tem autonomia para decidir e pessoas para inspirar."),
                "col": ("🤝 O Colaborador Mestre", "Você brilha em equipe. Sua força está em conectar pessoas e fazer o grupo funcionar em harmonia."),
                "ind": ("🎯 O Especialista Independente", "Você performa melhor com autonomia e foco. Seu talento floresce em profundidade, não em quantidade."),
                "cri": ("✨ O Criativo Inovador", "Você precisa de liberdade para criar. Ambientes rígidos sufocam seu maior talento."),
                "exe": ("⚙️ O Executor de Excelência", "Você tem o dom raro da execução precisa. Onde outros veem caos, você encontra a ordem."),
                "hum": ("💙 O Propósito Humano", "Você trabalha para impactar vidas. Qualquer trabalho sem propósito humano drena sua energia."),
                "intel": ("🧠 O Estrategista Intelectual", "Você precisa de desafios mentais constantes. Seu cérebro é sua maior ferramenta."),
                "prag": ("💡 O Pragmático de Resultados", "Você foca no que funciona. Seu ambiente ideal é orientado a metas claras e resultados mensuráveis."),
                "lib": ("🌿 O Trabalho com Propósito Livre", "Você precisa de liberdade e sentido. O melhor trabalho para você é aquele que parece missão."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "lid"
            titulo_r, desc_r = perfis_trab.get(vencedor, ("💼 Perfil Único", "Seu perfil profissional é singular."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>💼</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_trabalho' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar desvenda seu perfil profissional..."):
                    st.session_state.ia_quiz_trabalho = consultar_ravengar(
                        f"Perfil profissional: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Descreva: o ambiente de trabalho ideal, o tipo de liderança que esta pessoa precisa, "
                        f"seus superpoderes profissionais e o que deve evitar. Tom místico mas praticamente útil.",
                        api_key, "Quiz_Trabalho"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_trabalho}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_trabalho", perguntas_trabalho, "Quiz_Trabalho", "Qual é o Seu Perfil Profissional?", "Descubra como você trabalha melhor, o ambiente ideal e seus superpoderes profissionais.", "💼", resultado_trabalho)

    # ============================================================
    # TAB 4: QUIZ CARREIRA — EMPREGO/CARREIRA IDEAL
    # ============================================================
    with tabs[4]:
        perguntas_carreira = [
            {"p": "Se você pudesse trabalhar com qualquer coisa sem pensar em dinheiro, o que escolheria?", "contexto": "Deixe a lógica de lado por um momento...",
             "o": {"arte": "Arte, música ou expressão criativa", "cienc": "Ciência, tecnologia ou inovação", "pessoas": "Ajudar e cuidar de pessoas", "negocios": "Empreender e construir negócios"},
             "pontos": {"arte": {"arte": 3}, "cienc": {"tec": 3}, "pessoas": {"social": 3}, "negocios": {"empr": 3}}},
            {"p": "Qual destas habilidades é a sua mais natural?", "contexto": "Não o que você aprendeu, mas o que já nasceu em você...",
             "o": {"convenc": "Convencer e influenciar pessoas", "analisa": "Analisar e resolver problemas complexos", "cria": "Criar e imaginar coisas novas", "organiz": "Organizar e estruturar processos"},
             "pontos": {"convenc": {"comun": 3}, "analisa": {"anali": 3}, "cria": {"arte": 2, "tec": 1}, "organiz": {"gest": 3}}},
            {"p": "Quanto tempo você está disposto(a) a investir estudando para sua carreira?", "contexto": "Seja realista...",
             "o": {"muito": "Vou dedicar anos — quero ser especialista", "medio": "Estudo contínuo, mas já quero começar", "rapido": "Quero algo prático e rápido", "apren": "Prefiro aprender fazendo"},
             "pontos": {"muito": {"tec": 1, "saude": 1, "jur": 1}, "medio": {"empr": 1, "comun": 1}, "rapido": {"arte": 1, "comun": 1}, "apren": {"empr": 2}}},
            {"p": "Qual destes cenários te empolga mais?", "contexto": "Imagine vividamente...",
             "o": {"palco": "Estar num palco falando para uma multidão", "lab": "Resolver um problema técnico complexo sozinho", "impac": "Saber que seu trabalho ajudou centenas de pessoas", "liber": "Acordar sem horário fixo e trabalhar do jeito que quer"},
             "pontos": {"palco": {"comun": 3}, "lab": {"anali": 2, "tec": 1}, "impac": {"social": 3}, "liber": {"empr": 3, "arte": 1}}},
            {"p": "Qual seria o maior sinal de sucesso na sua carreira?", "contexto": "Como você saberá que chegou lá?...",
             "o": {"dinheiro": "Renda muito acima da média", "reconhec": "Reconhecimento e prestígio no campo", "impac2": "Ter mudado a vida de muitas pessoas", "liber2": "Trabalhar onde e quando quiser"},
             "pontos": {"dinheiro": {"empr": 2, "tec": 1}, "reconhec": {"comun": 2, "arte": 1}, "impac2": {"social": 3}, "liber2": {"empr": 2, "arte": 1}}},
            {"p": "Qual destas áreas do conhecimento te fascina mais?", "contexto": "O que você leria por pura curiosidade?...",
             "o": {"psico": "Psicologia e comportamento humano", "tecno": "Tecnologia, dados e sistemas", "negs": "Negócios, estratégia e mercados", "design": "Design, comunicação e estética"},
             "pontos": {"psico": {"social": 2, "comun": 1}, "tecno": {"tec": 3, "anali": 1}, "negs": {"empr": 2, "gest": 1}, "design": {"arte": 2, "comun": 1}}},
        ]

        def resultado_carreira(estado, api_key):
            pontos = estado["pontos"]
            carreiras = {
                "arte": ("🎨 Economia Criativa", "Designer, ilustrador, músico, produtor de conteúdo, fotógrafo, roteirista, arquiteto criativo.", "Sua alma é criativa. Qualquer carreira que suprima isso vai te sugar por dentro."),
                "tec": ("💻 Tecnologia & Inovação", "Desenvolvedor, cientista de dados, engenheiro, UX designer, especialista em IA, analista de sistemas.", "Sua mente analítica e interesse em sistemas te coloca no centro da revolução tecnológica."),
                "social": ("🌍 Impacto Social & Cuidado", "Psicólogo, assistente social, educador, profissional de saúde, ONG, RH, coaching.", "Sua maior realização vem quando vê o impacto direto na vida das pessoas."),
                "empr": ("🚀 Empreendedorismo", "Fundador de startup, consultor independente, vendedor, gestor comercial, investidor, freelancer.", "Você não foi feito para trabalhar para outros por muito tempo. Seu lugar é no comando."),
                "comun": ("🎤 Comunicação & Influência", "Marketing, jornalismo, publicidade, relações públicas, palestrante, criador de conteúdo, vendas.", "Você tem o dom de mover pessoas com palavras. Esse é um talento raro e valioso."),
                "anali": ("🔬 Análise & Estratégia", "Analista financeiro, consultor estratégico, cientista, pesquisador, auditor, economista.", "Sua mente vê padrões onde outros veem caos. Isso é ouro no mundo dos negócios."),
                "gest": ("⚙️ Gestão & Operações", "Gerente de projetos, administrador, supply chain, controller, gestor de operações.", "Você tem o talento de fazer as coisas funcionarem. Organizações precisam desesperadamente de pessoas como você."),
                "saude": ("💊 Saúde & Bem-estar", "Médico, enfermeiro, nutricionista, fisioterapeuta, terapeuta, personal trainer.", "Cuidar de corpos e mentes é sua vocação. É uma das carreiras mais humanas e necessárias."),
                "jur": ("⚖️ Direito & Justiça", "Advogado, juiz, promotor, defensor público, analista jurídico.", "Você tem senso de justiça apurado e capacidade analítica para navegar sistemas complexos."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "empr"
            area, exemplos, motivo = carreiras.get(vencedor, ("🌟 Carreira Única", "Múltiplas possibilidades", "Seu perfil é singular."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>🚀</div><h2>{area}</h2><p style='color:#C4B5D4;font-size:1.05em'>{motivo}</p><div class='badge-perfil'>{exemplos}</div></div>", unsafe_allow_html=True)

            if 'ia_quiz_carreira' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar revela sua vocação..."):
                    st.session_state.ia_quiz_carreira = consultar_ravengar(
                        f"Vocação revelada: {area}. Exemplos: {exemplos}. Motivo: {motivo}. Respostas: {respostas_txt}. "
                        f"Crie um plano de carreira místico e prático: por onde começar, quais habilidades desenvolver, "
                        f"qual carreira específica dentro da área tem mais potencial para esta pessoa, e um insight profundo sobre o propósito por trás desta vocação.",
                        api_key, "Quiz_Carreira"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_carreira}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_carreira", perguntas_carreira, "Quiz_Carreira", "Qual é a Sua Carreira Ideal?", "As estrelas já sabem para onde sua vida profissional deve ir. Vamos revelar.", "🚀", resultado_carreira)

    # ============================================================
    # TAB 5: QUIZ PERSONALIDADE PROFUNDA
    # ============================================================
    with tabs[5]:
        perguntas_pers = [
            {"p": "Numa festa, você normalmente:", "contexto": "Seja honesto(a)...",
             "o": {"energia": "Energiza o ambiente e conhece todos", "observa": "Observa antes de interagir", "grupos": "Fica com grupos pequenos que já conhece", "sai": "Fica pouco tempo e prefere sair cedo"},
             "pontos": {"energia": {"ext": 3}, "observa": {"int": 2, "obs": 1}, "grupos": {"sel": 2}, "sai": {"int": 3}}},
            {"p": "Quando precisa tomar uma decisão importante:", "contexto": "Como seu processo interno funciona?...",
             "o": {"dados": "Pesquiso dados e analiso tudo antes", "instinto": "Confio no instinto e no que sinto", "consult": "Consulto pessoas de confiança", "espero": "Espero a situação se resolver"},
             "pontos": {"dados": {"racion": 3}, "instinto": {"intuit": 3}, "consult": {"ext": 1, "sel": 1}, "espero": {"adapt": 2}}},
            {"p": "Qual das características abaixo mais te define?", "contexto": "A primeira que vier à mente...",
             "o": {"curio": "Curioso e sempre buscando aprender", "leal": "Leal e confiável acima de tudo", "direto": "Direto e focado em resultados", "empath": "Empático e sensível ao outro"},
             "pontos": {"curio": {"intel": 3}, "leal": {"leal": 3}, "direto": {"racion": 2, "lidp": 1}, "empath": {"emo": 3}}},
            {"p": "O que você faz quando está sob pressão extrema?", "contexto": "Naqueles momentos difíceis...",
             "o": {"foco": "Foco ainda mais e entrego o melhor", "retiro": "Me retiro e processo internamente", "busca": "Busco apoio de pessoas próximas", "explode": "Libero a tensão e depois me recomponho"},
             "pontos": {"foco": {"racion": 2, "lidp": 1}, "retiro": {"int": 2, "intel": 1}, "busca": {"emo": 2, "sel": 1}, "explode": {"intuit": 1, "ext": 1}}},
            {"p": "O que as pessoas mais te pedem?", "contexto": "Pense nos seus relacionamentos...",
             "o": {"conselho": "Conselhos e orientação", "anima": "Ânimo e energia positiva", "solucao": "Ajuda para resolver problemas práticos", "ouvido": "Um ouvido para desabafar"},
             "pontos": {"conselho": {"intel": 2, "leal": 1}, "anima": {"ext": 2, "intuit": 1}, "solucao": {"racion": 3}, "ouvido": {"emo": 3}}},
            {"p": "Qual é o seu maior ponto cego (o que você evita enxergar)?", "contexto": "Aqui mora a sua sombra...",
             "o": {"vuln": "Minha vulnerabilidade", "limit": "Meus limites", "senti": "Meus sentimentos", "depend": "Minha dependência dos outros"},
             "pontos": {"vuln": {"racion": 2, "lidp": 1}, "limit": {"ext": 2, "intuit": 1}, "senti": {"racion": 2, "intel": 1}, "depend": {"int": 2, "leal": 1}}},
        ]

        def resultado_personalidade(estado, api_key):
            pontos = estado["pontos"]
            perfis_pers = {
                "ext": ("🌟 O Extrovertido Magnético", "Você ganha energia das pessoas. Sua presença ilumina ambientes e você tem facilidade natural de criar conexões."),
                "int": ("🌙 O Introvertido Profundo", "Você ganha energia na solidão. Sua profundidade interior é sua maior riqueza — você pensa diferente de 90% das pessoas."),
                "racion": ("⚖️ O Racional Estratégico", "Sua mente é sua arma. Você analisa, planeja e executa com precisão que poucos alcançam."),
                "intuit": ("🔮 O Intuitivo Criativo", "Você sente as coisas antes de entendê-las. Sua intuição é um superpoder que o mundo ainda não aprendeu a valorizar."),
                "emo": ("💜 O Empático Profundo", "Você sente o mundo com intensidade. Sua capacidade de compreender o outro é rara e transforma relacionamentos."),
                "intel": ("🧠 O Intelectual Curioso", "Sua sede de conhecimento é insaciável. Você aprende rápido e consegue conectar ideias de formas que outros não veem."),
                "leal": ("🛡️ O Guardião Leal", "Sua lealdade e confiabilidade são pilares. Pessoas ao seu redor sabem que podem contar com você sempre."),
                "lidp": ("👑 O Líder Nato", "Você assume o comando naturalmente. Sua segurança e direcionamento atraem pessoas que precisam de orientação."),
                "adapt": ("🌊 O Adaptável", "Você flui com as mudanças. Sua flexibilidade é uma riqueza em um mundo em constante transformação."),
                "obs": ("👁️ O Observador Perspicaz", "Você vê o que os outros não veem. Sua análise silenciosa revela verdades que ficam ocultas para a maioria."),
                "sel": ("💎 O Seletivo Profundo", "Você preza por qualidade em tudo — especialmente em pessoas. Seus relacionamentos são poucos, mas são ouro."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "intel"
            titulo_r, desc_r = perfis_pers.get(vencedor, ("✨ Perfil Único", "Sua personalidade é singular e multidimensional."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>🧠</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_pers' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar desvenda sua alma..."):
                    st.session_state.ia_quiz_pers = consultar_ravengar(
                        f"Personalidade: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Faça uma análise profunda de: seus pontos fortes ocultos, seus padrões autossabotadores, "
                        f"como seus relacionamentos são afetados por essa personalidade, e o que ela precisa desenvolver para alcançar seu potencial máximo. "
                        f"Tom místico, psicologicamente preciso e revelador.",
                        api_key, "Quiz_Personalidade"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_pers}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_pers", perguntas_pers, "Quiz_Personalidade", "Sua Personalidade Revelada", "Descubra as camadas mais profundas de quem você realmente é — além da máscara social.", "🧠", resultado_personalidade)

    # ============================================================
    # TAB 6: QUIZ DINHEIRO
    # ============================================================
    with tabs[6]:
        perguntas_din = [
            {"p": "Quando você recebe dinheiro extra, o que faz primeiro?", "contexto": "Seja completamente honesto(a)...",
             "o": {"gasta": "Gasto logo — eu mereço", "guarda": "Guardo imediatamente na poupança", "investe": "Penso em como fazer esse dinheiro crescer", "decide": "Fico em dúvida e acabo gastando aos poucos"},
             "pontos": {"gasta": {"hedoni": 3}, "guarda": {"conser": 3}, "investe": {"invest": 3}, "decide": {"inseg": 3}}},
            {"p": "Como você se sente ao pedir desconto ou negociar?", "contexto": "Pense na última vez que aconteceu...",
             "o": {"faz": "Faço naturalmente, sem constrangimento", "incom": "Me sinto desconfortável mas faço", "evito": "Evito sempre, prefiro pagar o preço", "gosto": "Gosto — é um jogo que eu ganho"},
             "pontos": {"faz": {"negoc": 2}, "incom": {"conser": 1}, "evito": {"inseg": 2}, "gosto": {"empr_d": 3}}},
            {"p": "O que você acredita profundamente sobre dinheiro?", "contexto": "Sua crença mais honesta...",
             "o": {"dificil": "É difícil de ganhar e fácil de perder", "ferram": "É uma ferramenta — nem bem nem mal", "poder": "Dinheiro é poder e liberdade", "raiz": "Pode corromper quem não tem valores"},
             "pontos": {"dificil": {"inseg": 2, "conser": 1}, "ferram": {"invest": 2, "empr_d": 1}, "poder": {"empr_d": 2, "invest": 1}, "raiz": {"conser": 2}}},
            {"p": "Qual é a sua maior dificuldade com dinheiro?", "contexto": "Aqui está a raiz do padrão...",
             "o": {"gastar": "Gasto mais do que deveria", "economiz": "Tenho dificuldade de economizar", "investir": "Não sei como investir ou tenho medo", "ganhar": "Sinto que nunca ganho o suficiente"},
             "pontos": {"gastar": {"hedoni": 2}, "economiz": {"hedoni": 1, "inseg": 1}, "investir": {"inseg": 2, "conser": 1}, "ganhar": {"inseg": 2, "conser": 1}}},
            {"p": "Com qual afirmação você mais se identifica?", "contexto": "A que faz mais sentido para você...",
             "o": {"viver": "Prefiro viver o hoje do que economizar para o amanhã", "segur": "Segurança financeira é minha prioridade", "crescer": "Quero ver meu dinheiro crescer e trabalhar por mim", "merit": "Dinheiro vem para quem trabalha duro"},
             "pontos": {"viver": {"hedoni": 3}, "segur": {"conser": 3}, "crescer": {"invest": 3}, "merit": {"empr_d": 2, "conser": 1}}},
        ]

        def resultado_dinheiro(estado, api_key):
            pontos = estado["pontos"]
            perfis_din = {
                "hedoni": ("🎉 O Hedonista Financeiro", "Você vive o presente com intensidade. Dinheiro para você é sinônimo de prazer e experiências. O risco: o futuro pode te surpreender."),
                "conser": ("🏦 O Conservador Cauteloso", "Você valoriza segurança acima de tudo. Isso te protege — mas pode te impedir de crescer financeiramente."),
                "invest": ("📈 O Investidor Estratégico", "Você entende que dinheiro deve trabalhar por você. Sua mentalidade já está à frente da maioria."),
                "inseg": ("😰 O Ansioso Financeiro", "Dinheiro te gera mais ansiedade do que tranquilidade. Há crenças limitantes que precisam ser revisadas."),
                "empr_d": ("🚀 O Empreendedor Financeiro", "Você vê oportunidade onde outros veem risco. Seu perfil é de quem gera riqueza, não só acumula."),
                "negoc": ("🤝 O Negociador Nato", "Você tem facilidade natural com dinheiro na prática. Sua habilidade de negociar é um ativo financeiro real."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "conser"
            titulo_r, desc_r = perfis_din.get(vencedor, ("💰 Perfil Único", "Sua relação com dinheiro é singular."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>💰</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_din' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar revela sua relação com a prosperidade..."):
                    st.session_state.ia_quiz_din = consultar_ravengar(
                        f"Perfil financeiro: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Revele: as crenças ocultas que moldam a relação desta pessoa com dinheiro, "
                        f"o padrão financeiro que ela repete inconscientemente, "
                        f"3 ações concretas para transformar sua vida financeira, "
                        f"e o potencial de prosperidade que ela ainda não acessou. Tom místico mas financeiramente preciso.",
                        api_key, "Quiz_Dinheiro"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_din}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_din", perguntas_din, "Quiz_Dinheiro", "Qual é a Sua Relação com o Dinheiro?", "Descubra as crenças ocultas que definem sua prosperidade — e como transformá-las.", "💰", resultado_dinheiro)

    # ============================================================
    # TAB 7: QUIZ PROPÓSITO
    # ============================================================
    with tabs[7]:
        perguntas_prop = [
            {"p": "O que te tira do sono (no bom sentido)?", "contexto": "Aquilo que te mantém acordado(a) pensando...",
             "o": {"ideias": "Ideias e projetos que ainda não existem", "injust": "Injustiças que precisam ser resolvidas", "pessoas": "O bem-estar de quem você ama", "aprend": "Algo novo que está aprendendo"},
             "pontos": {"ideias": {"cria_p": 3}, "injust": {"missao": 3}, "pessoas": {"conec": 3}, "aprend": {"saber": 3}}},
            {"p": "Quando você perde a noção do tempo, geralmente está:", "contexto": "O estado de flow revela o propósito...",
             "o": {"criando": "Criando ou construindo algo", "ajudando": "Ajudando alguém a resolver um problema", "aprendendo": "Aprendendo ou pesquisando", "conectando": "Conectando pessoas ou ideias"},
             "pontos": {"criando": {"cria_p": 3}, "ajudando": {"missao": 2, "conec": 1}, "aprendendo": {"saber": 3}, "conectando": {"conec": 2, "cria_p": 1}}},
            {"p": "Se você soubesse que ia morrer em 5 anos, o que faria?", "contexto": "A resposta mais honesta que você puder dar...",
             "o": {"legado": "Criaria algo que durasse depois de mim", "viagens": "Viveria intensamente cada experiência", "familia": "Me dedicaria completamente a quem amo", "causa": "Lutaria por uma causa que acredito"},
             "pontos": {"legado": {"cria_p": 2, "missao": 1}, "viagens": {"saber": 2, "conec": 1}, "familia": {"conec": 3}, "causa": {"missao": 3}}},
            {"p": "Qual dor do mundo mais te incomoda?", "contexto": "Aquilo que você não consegue ignorar...",
             "o": {"solidao": "A solidão e desconexão entre as pessoas", "injust2": "A injustiça e desigualdade", "ignor": "A ignorância e falta de acesso ao conhecimento", "beleza": "A falta de beleza e expressão no mundo"},
             "pontos": {"solidao": {"conec": 3}, "injust2": {"missao": 3}, "ignor": {"saber": 3}, "beleza": {"cria_p": 3}}},
            {"p": "Como você quer ser lembrado(a)?", "contexto": "Sua definição de uma vida bem vivida...",
             "o": {"criou": "Criou algo que mudou a forma como vemos o mundo", "ajudou": "Ajudou e transformou muitas vidas", "ensinou": "Ensinou e iluminou o caminho de outros", "amou": "Amou profundamente e foi amado(a)"},
             "pontos": {"criou": {"cria_p": 3}, "ajudou": {"missao": 2, "conec": 1}, "ensinou": {"saber": 3}, "amou": {"conec": 3}}},
        ]

        def resultado_proposito(estado, api_key):
            pontos = estado["pontos"]
            perfis_prop = {
                "cria_p": ("✨ O Criador de Mundos", "Seu propósito é criar. Trazer à existência o que ainda não existe. Você está aqui para deixar uma marca através da sua expressão única."),
                "missao": ("🌍 O Agente de Mudança", "Você está aqui para transformar algo que está errado no mundo. Seu propósito tem dimensão social e política — e isso não é escolha, é chamado."),
                "conec": ("💙 O Construtor de Pontes", "Seu propósito é conectar — pessoas, ideias, mundos. Você é o elo que faz a corrente funcionar."),
                "saber": ("🔮 O Guardião do Conhecimento", "Você está aqui para aprender e transmitir sabedoria. Seu propósito é ser um farol de entendimento em um mundo de ruído."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "missao"
            titulo_r, desc_r = perfis_prop.get(vencedor, ("🌟 Propósito Singular", "Seu propósito é único e está se revelando."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>🌟</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_prop' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar revela sua missão de vida..."):
                    st.session_state.ia_quiz_prop = consultar_ravengar(
                        f"Propósito revelado: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Faça uma revelação profunda sobre: a missão específica desta alma nesta vida, "
                        f"por que ela ainda não está vivendo seu propósito pleno, "
                        f"o primeiro passo concreto para se alinhar com esse propósito, "
                        f"e uma visão inspiradora de como sua vida ficará quando estiver no caminho certo. "
                        f"Tom filosófico, místico e emocionalmente tocante.",
                        api_key, "Quiz_Proposito"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_prop}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_prop", perguntas_prop, "Quiz_Proposito", "Qual é o Seu Propósito de Vida?", "A missão que sua alma escolheu antes de chegar aqui. Está na hora de lembrar.", "🌟", resultado_proposito)

    # ============================================================
    # TAB 8: QUIZ ENERGIA
    # ============================================================
    with tabs[8]:
        perguntas_en = [
            {"p": "Quando você entra numa sala, o que geralmente acontece?", "contexto": "Observe o padrão...",
             "o": {"anima": "O ambiente fica mais animado", "calma": "As pessoas se acalmam", "foco": "As pessoas ficam mais focadas", "curio": "As pessoas ficam curiosas"},
             "pontos": {"anima": {"solar": 3}, "calma": {"terra": 3}, "foco": {"fogo": 2, "terra": 1}, "curio": {"ar": 3}}},
            {"p": "Como você recarrega suas energias?", "contexto": "O que realmente te restaura...",
             "o": {"sozinho": "Silêncio e solidão completa", "natureza": "Contato com a natureza", "pessoas": "Estar com pessoas que amo", "criando": "Criando ou me expressando"},
             "pontos": {"sozinho": {"agua": 3}, "natureza": {"terra": 3}, "pessoas": {"solar": 2, "ar": 1}, "criando": {"fogo": 3}}},
            {"p": "Qual elemento da natureza mais te representa?", "contexto": "Confie no primeiro instinto...",
             "o": {"fogo_e": "🔥 Fogo — intenso e transformador", "agua_e": "🌊 Água — profundo e adaptável", "terra_e": "🌍 Terra — estável e nutrido", "ar_e": "💨 Ar — livre e expansivo"},
             "pontos": {"fogo_e": {"fogo": 3}, "agua_e": {"agua": 3}, "terra_e": {"terra": 3}, "ar_e": {"ar": 3}}},
            {"p": "Como as pessoas descrevem sua presença?", "contexto": "O que costumam te falar...",
             "o": {"intensa": "Intensa e marcante", "aconc": "Acolhedora e reconfortante", "inspir": "Inspiradora e motivadora", "misteriosa": "Misteriosa e intrigante"},
             "pontos": {"intensa": {"fogo": 2, "agua": 1}, "aconc": {"terra": 2, "solar": 1}, "inspir": {"solar": 2, "ar": 1}, "misteriosa": {"agua": 3}}},
            {"p": "Em momentos de crise, você é:", "contexto": "Sua natureza emerge no limite...",
             "o": {"acao": "Ação imediata e decisão rápida", "apoio": "O porto seguro que todos buscam", "analis": "Analisa friamente e encontra a saída", "adapta": "Se adapta e flui com a situação"},
             "pontos": {"acao": {"fogo": 3}, "apoio": {"terra": 2, "solar": 1}, "analis": {"ar": 2, "agua": 1}, "adapta": {"agua": 3}}},
        ]

        def resultado_energia(estado, api_key):
            pontos = estado["pontos"]
            perfis_en = {
                "fogo": ("🔥 Energia de Fogo", "Você é transformação em movimento. Onde você chega, algo muda. Sua intensidade é seu maior dom e seu maior desafio."),
                "agua": ("🌊 Energia de Água", "Você é profundidade e mistério. Você sente tudo intensamente e tem uma capacidade única de compreender o que está além das palavras."),
                "terra": ("🌍 Energia de Terra", "Você é fundação e sustento. As pessoas ao seu redor se sentem mais seguras, mais inteiras, mais enraizadas na sua presença."),
                "ar": ("💨 Energia de Ar", "Você é movimento e ideia. Sua mente conecta pontos que outros não veem e sua energia expande tudo ao redor."),
                "solar": ("☀️ Energia Solar", "Você é luz e vitalidade. Sua presença aquece, anima e dá esperança. Você é o tipo de pessoa que as pessoas buscam quando precisam de força."),
            }
            vencedor = max(pontos, key=pontos.get) if pontos else "solar"
            titulo_r, desc_r = perfis_en.get(vencedor, ("⚡ Energia Única", "Sua energia é singular e multidimensional."))

            st.markdown(f"<div class='card-resultado'><div style='font-size:2em'>⚡</div><h2>{titulo_r}</h2><p style='color:#C4B5D4;font-size:1.05em'>{desc_r}</p></div>", unsafe_allow_html=True)

            if 'ia_quiz_en' not in st.session_state:
                respostas_txt = " | ".join([f"{r['pergunta']}: {r['resposta']}" for r in estado["respostas"]])
                with st.spinner("O Ravengar lê sua energia vital..."):
                    st.session_state.ia_quiz_en = consultar_ravengar(
                        f"Energia vital: {titulo_r} — {desc_r}. Respostas: {respostas_txt}. "
                        f"Revele: como essa energia se manifesta nos relacionamentos desta pessoa, "
                        f"ambientes que potencializam vs drenam essa energia, "
                        f"como usar essa energia conscientemente para atrair o que deseja, "
                        f"e um ritual ou prática para amplificar esse tipo de energia. Tom espiritual e prático.",
                        api_key, "Quiz_Energia"
                    )
            st.markdown(f"<div class='card-ravengar'>{st.session_state.ia_quiz_en}</div>", unsafe_allow_html=True)

        renderizar_quiz("quiz_en", perguntas_en, "Quiz_Energia", "Qual é o Seu Tipo de Energia?", "Descubra a energia que você irradia e como ela molda sua realidade.", "⚡", resultado_energia)

    # ============================================================
    # TAB 9: DECIFRADOR
    # ============================================================
    with tabs[9]:
        st.markdown("<div class='titulo-secao'>👁️ O Decifrador de Símbolos</div>", unsafe_allow_html=True)
        texto_dec = st.text_area("Descreva o símbolo, sonho ou signo que quer decifrar:", placeholder="Ex: Sonhei que estava voando sobre uma cidade em chamas e havia um espelho quebrado no chão...")
        if st.button("✦ DECIFRAR MISTÉRIO ✦"):
            if chave_api and texto_dec:
                with st.spinner("O oráculo decifra os símbolos..."):
                    st.session_state['chat_dec'] = consultar_ravengar(texto_dec, api_key=chave_api, setor="Decifrador")
        if 'chat_dec' in st.session_state:
            st.markdown(f"<div class='card-ravengar'>👁️<br>{st.session_state['chat_dec']}</div>", unsafe_allow_html=True)

        # Meditação guiada
        st.markdown("---")
        st.markdown("<div class='titulo-secao' style='font-size:1.1em'>🧘 Meditação Guiada Personalizada</div>", unsafe_allow_html=True)
        intencao_med = st.selectbox("Intenção da meditação:", ["Clareza mental", "Cura emocional", "Prosperidade", "Amor próprio", "Proteção energética", "Conexão espiritual", "Foco e produtividade"])
        tempo_med = st.selectbox("Duração:", ["5 minutos", "10 minutos", "20 minutos"])
        if st.button("✦ CRIAR MINHA MEDITAÇÃO ✦"):
            with st.spinner("Criando sua meditação personalizada..."):
                prompt_med = f"Crie uma meditação guiada de {tempo_med} com intenção de {intencao_med} para {nome}. Inclua respiração, visualizações e afirmações. Tom sereno, profundo e transformador."
                st.session_state['med_result'] = consultar_ravengar(prompt_med, chave_api, "Meditacao")
        if 'med_result' in st.session_state:
            st.markdown(f"<div class='card-ouro'>{st.session_state['med_result']}</div>", unsafe_allow_html=True)

    # ============================================================
    # TAB 10: DETETIVE VIRTUAL
    # ============================================================
    with tabs[10]:
        st.markdown("<div class='titulo-secao'>🕵️ O Detetive das Almas</div>", unsafe_allow_html=True)
        if 'historico_detetive' not in st.session_state:
            st.session_state.historico_detetive = []

        nome_alvo = st.text_input("Quem vamos investigar?", placeholder="Ex: A pessoa misteriosa que apareceu na minha vida...")

        for msg in st.session_state.historico_detetive:
            icon = "👤" if msg["role"] == "user" else "🕵️"
            st.markdown(f"<div class='{'msg-balao' if msg['role']=='user' else 'card-ravengar'}'><b>{icon}</b> {msg['content']}</div>", unsafe_allow_html=True)

        if prompt_det := st.chat_input("Descreva um comportamento ou situação para análise..."):
            st.session_state.historico_detetive.append({"role": "user", "content": f"Sobre {nome_alvo}: {prompt_det}"})
            resposta = consultar_ravengar("", api_key=chave_api, setor="Detetive", historico=st.session_state.historico_detetive)
            st.session_state.historico_detetive.append({"role": "assistant", "content": resposta})
            st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.historico_detetive:
                conteudo = f"INVESTIGAÇÃO: {nome_alvo}\n" + "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.historico_detetive])
                st.download_button("💾 SALVAR INVESTIGAÇÃO", data=conteudo, file_name=f"investigacao_{nome_alvo}.txt", mime="text/plain")
        with col2:
            if st.session_state.historico_detetive:
                if st.button("🗑️ RESETAR CONVERSA"):
                    st.session_state.historico_detetive = []
                    st.rerun()

    # ============================================================
    # TAB 11: SEU ESPAÇO
    # ============================================================
    with tabs[11]:
        st.markdown("<div class='titulo-secao'>🧘 Seu Espaço Sagrado</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 📰 Radar do Ravengar")
            tema = st.selectbox("Escolha um assunto:", ["Ciência", "Astronomia", "Saúde & Bem-estar", "Relacionamentos", "Tecnologia", "Games", "Esportes", "Cinema & TV", "Espiritualidade", "Filosofia"])
            if st.button("✦ BUSCAR NO ÉTER ✦"):
                if chave_api:
                    with st.spinner("Buscando no éter..."):
                        st.session_state['noticias_dia'] = consultar_ravengar(f"Resuma 3 tendências ou reflexões sobre {tema} com tom místico e perspicaz.", api_key=chave_api, setor="Noticias")
            if 'noticias_dia' in st.session_state:
                st.markdown(f"<div class='card-ravengar'>{st.session_state['noticias_dia']}</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown("### 🃏 Tarot do Dia")
            if st.button("✦ PUXAR CARTA DO DIA ✦"):
                if chave_api:
                    cartas = ["O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador", "O Hierofante", "Os Enamorados", "O Carro", "A Justiça", "O Eremita", "A Roda da Fortuna", "A Força", "O Pendurado", "A Morte", "A Temperança", "O Diabo", "A Torre", "A Estrela", "A Lua", "O Sol", "O Julgamento", "O Mundo", "O Louco"]
                    carta = random.choice(cartas)
                    with st.spinner("Puxando a carta..."):
                        st.session_state['carta_dia'] = (carta, consultar_ravengar(f"Carta do Tarot '{carta}' para {nome} hoje. Veredito profundo e personalizaado.", api_key=chave_api, setor="Tarot"))
            if 'carta_dia' in st.session_state:
                st.markdown(f"<div class='card-resultado'><h2 style='color:#D4AF37'>{st.session_state['carta_dia'][0]}</h2><p>{st.session_state['carta_dia'][1]}</p></div>", unsafe_allow_html=True)

        # Afirmações diárias
        st.markdown("---")
        st.markdown("### 🌟 Afirmações Personalizadas")
        area_afirm = st.selectbox("Área de foco:", ["Autoestima", "Prosperidade", "Amor", "Saúde", "Coragem", "Paz interior"], key="area_afirm")
        if st.button("✦ GERAR MINHAS AFIRMAÇÕES ✦"):
            with st.spinner("Canalizando suas afirmações..."):
                prompt_af = f"Crie 7 afirmações poderosas e personalizadas para {nome} com foco em {area_afirm}. Cada uma deve ser no presente, na primeira pessoa, poderosa e emocionalmente impactante. Adicione uma explicação mística de cada uma."
                st.session_state['afirm_result'] = consultar_ravengar(prompt_af, chave_api, "Meditacao")
        if 'afirm_result' in st.session_state:
            st.markdown(f"<div class='card-ouro'>{st.session_state['afirm_result']}</div>", unsafe_allow_html=True)

    # ============================================================
    # TAB 12: BIBLIOTECA
    # ============================================================
    with tabs[12]:
        st.markdown("<div class='titulo-secao'>📚 Biblioteca Secreta</div>", unsafe_allow_html=True)
        cursos = [
            {"titulo": "🔮 Leitura Fria: Como Entender Qualquer Pessoa em Segundos", "desc": "Aprenda a interpretar comportamentos, identificar padrões ocultos e compreender o que as pessoas realmente pensam.", "url": "https://drive.google.com/file/d/1Yn7BkHCKjJPEXb3Rtip11ZxO0R11a1bd/view?usp=sharing"},
            {"titulo": "✋ Leitura de Mãos: Descubra o Que Suas Mãos Revelam Sobre Você", "desc": "Aprenda a identificar as principais linhas da mão e interpretar seus significados de forma simples e prática.", "url": "https://drive.google.com/file/d/1jDHSLRzxB2jQbTnpsdegLvMITqLKhHN5/view?usp=sharing"},
            {"titulo": "🔢 Numerologia do Nome: Descubra Seu Código Oculto", "desc": "Aprenda a transformar letras em números e interpretar o significado oculto por trás do seu nome.", "url": "https://drive.google.com/file/d/1t0x1eEvlXQbEOO24OZghlAC4x8yLbvzh/view?usp=sharing"},
            {"titulo": "🧠 Leitura Psicológica: Descubra Padrões Ocultos da Sua Mente", "desc": "Aprenda a identificar comportamentos inconscientes e reconhecer padrões que influenciam suas decisões.", "url": "https://drive.google.com/file/d/1xcQdzSXBfXIUht2hjGlty0Ikw4nYz4og/view?usp=sharing"},
            {"titulo": "❤️ Leitura de Intenção: Descubra o Que as Pessoas Realmente Sentem", "desc": "Aprenda a interpretar sinais sutis, atitudes e comportamentos que revelam o verdadeiro interesse.", "url": "https://drive.google.com/file/d/1XnnG0yXlzPa7f7TVrC8oK5kJZr5_gItJ/view?usp=sharing"},
            {"titulo": "🎯 Simulador de Futuro: Veja Para Onde Suas Decisões Estão Te Levando", "desc": "Aprenda a identificar padrões de comportamento e entender como suas escolhas impactam seu futuro.", "url": "https://drive.google.com/file/d/1i8CGaZ0aYba7aykQ8n4nIj52HmS8uqOB/view?usp=sharing"},
            {"titulo": "🎁 Desbloqueio da Sorte: Ative Seu Potencial de Oportunidades", "desc": "Aprenda a desenvolver uma mentalidade estratégica para reconhecer e aproveitar oportunidades.", "url": "https://drive.google.com/file/d/1jBUp4W1K-PYCkSeAJuRzm6xaDB8C8Ly1/view?usp=sharing"},
        ]
        cols = st.columns(2)
        for i, item in enumerate(cursos):
            with cols[i % 2]:
                st.markdown(f"<div class='biblioteca-card'><h4 style='color:#D4AF37;font-family:Cinzel,serif'>{item['titulo']}</h4><p style='color:#C4B5D4;font-size:0.9em'>{item['desc']}</p></div>", unsafe_allow_html=True)
                st.link_button("📥 Baixar PDF Grátis", item["url"])
                st.markdown("<br>", unsafe_allow_html=True)

    # ============================================================
    # TAB 13: ENCONTROS
    # ============================================================
    with tabs[13]:
        st.markdown("<div class='titulo-secao'>🤝 Encontros de Almas</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 💬 Mural das Sombras")
            if not mural_global:
                st.markdown("<div class='card-ravengar'><p style='text-align:center;color:#64748B;font-style:italic'>O silêncio ecoa... As sombras aguardam o primeiro registro.</p></div>", unsafe_allow_html=True)
            else:
                for m in reversed(mural_global[-15:]):
                    st.markdown(f"<div class='msg-balao'><small style='color:#D4AF37'><b>{m['usuario']}</b> · {m['hora']}</small><br>{m['texto']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("### ✍️ Manifestar no Mural")
            msg_input = st.text_area("O que desejas dizer às sombras?", placeholder="Sua mensagem para o universo...")
            if st.button("✦ LANÇAR AO MURAL ✦"):
                if msg_input:
                    mural_global.append({"usuario": nome, "texto": msg_input, "hora": datetime.datetime.now().strftime("%H:%M")})
                    st.rerun()

    st.markdown("---")
    if st.button("🔄 ENCERRAR SESSÃO"):
        st.session_state.clear()
        st.rerun()

    st.markdown("<div style='text-align:center;color:#4B3A6B;padding:20px;font-family:Cinzel,serif;font-size:0.8em;letter-spacing:2px'>✦ EXPLORANDO OS MISTÉRIOS DA MENTE E DO DESTINO ✦<br>© 2026 TENDA DO RAVENGAR</div>", unsafe_allow_html=True)
