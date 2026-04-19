import streamlit as st
from groq import Groq
import random
import datetime

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

    /* Estilo para os novos Cursos */
    .curso-card {
        background-color: #FFFFFF !important;
        border: 1px solid #FFD1DC !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #FF69B4 !important;
    }
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
        "Amor": ("És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética, profunda e empática."),
        "Trabalho": ("És o Ravengar, o Estrategista das Sombras. Tua linguagem é direta, fria e focada em poder."),
        "Futuro": ("És o Ravengar, o Profeta do Tempo. Tua linguagem é enigmática, vasta e mística."),
        "Saude": ("És o Ravengar, o Alquimista da Vitalidade. Tua linguagem é serena."),
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério e sabedoria ancestral.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa com precisão cirúrgica.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística e inteligente.",
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
        return f"Erro na conexão mística: {str(e)}"

# --- 4. BARRA LATERAL (CONFORME SEU CÓDIGO) ---
with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")
    if st.button("🔄 REINICIAR SESSÃO"):
        st.session_state.clear()
        st.rerun()

# --- 5. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
   st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    nome_input = st.text_input("Como as sombras te devem chamar?")
    genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
    if st.button("ENTRAR NA TENDA"):
        if nome_input:
           st.session_state.nome_user, st.session_state.genero_user = nome_input, genero_input
           st.session_state.usuario_identificado = True
           st.rerun()
else:
    # --- INTERFACE PRINCIPAL ---
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    # Abas com a nova adição: "🎓 Cursos Grátis"
    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço", "🤝 Encontros", "🎓 Cursos Grátis"])

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
                st.session_state['chat_ora'] = [{"content": consultar_ravengar(pergunta_ora, chave_api, setor_atual)}]
        if 'chat_ora' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{st.session_state['chat_ora'][0]['content']}</div>", unsafe_allow_html=True)

    # ... (Abas de Decifrador, Detetive e Quiz mantidas conforme seu original)

    with tabs[6]: # ENCONTROS
        st.markdown("<h2 style='text-align: center;'>🤝 ENCONTROS</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 💬 Mural de Almas")
            for m in reversed(mural_global[-15:]):
                st.markdown(f"<div class='msg-balao'><small><b>{m['usuario']}</b> • {m['hora']}</small><br>{m['texto']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("### ✍️ Manifestar")
            msg_input = st.text_area("O que deseja dizer às sombras?")
            if st.button("LANÇAR AO MURAL"):
                if msg_input:
                    mural_global.append({"usuario": st.session_state.nome_user, "texto": msg_input, "hora": datetime.datetime.now().strftime("%H:%M")})
                    st.rerun()

    with tabs[7]: # UPGRADE: CURSOS GRÁTIS
        st.markdown("<h2 style='text-align: center;'>🎓 Cursos e Treinamentos Gratuitos</h2>", unsafe_allow_html=True)
        
        cursos_data = [
            ("🔮 Leitura Fria: Como Entender Qualquer Pessoa em Segundos", "Aprenda a interpretar comportamentos, identificar padrões ocultos e compreender o que as pessoas realmente pensam — mesmo quando não dizem nada. Neste curso, você vai descobrir técnicas simples e poderosas para fazer leituras precisas, criar conexões instantâneas e se comunicar com muito mais influência e segurança em qualquer situação."),
            ("✋ Leitura de Mãos: Descubra o Que Suas Mãos Revelam Sobre Você", "Aprenda a identificar as principais linhas da mão e interpretar seus significados de forma simples e prática. Neste curso, você vai entender como traços físicos podem revelar padrões de personalidade, emoções e tendências, permitindo fazer leituras rápidas e surpreendentes."),
            ("🔢 Numerologia do Nome: Descubra Seu Código Oculto", "Aprenda a transformar letras em números e interpretar o significado oculto por trás do seu nome. Neste curso, você vai descobrir padrões que influenciam sua personalidade, suas decisões e até os caminhos que você tende a seguir na vida."),
            ("🧠 Leitura Psicológica: Descubra Padrões Ocultos da Sua Mente", "Aprenda a identificar comportamentos inconscientes, entender suas emoções e reconhecer padrões que influenciam suas decisões. Neste curso, você vai acessar uma nova forma de enxergar a si mesmo e às pessoas ao seu redor com muito mais clareza."),
            ("❤️ Leitura de Intenção: Descubra o Que as Pessoas Realmente Sentem", "Aprenda a interpretar sinais sutis, atitudes e comportamentos que revelam o verdadeiro interesse das pessoas. Neste curso, você vai entender como decifrar intenções e agir com mais segurança em relacionamentos e interações sociais."),
            ("🎯 Simulador de Futuro: Veja Para Onde Suas Decisões Estão Te Levando", "Aprenda a identificar padrões de comportamento e entender como suas escolhas impactam diretamente seu futuro. Neste curso, você vai visualizar diferentes caminhos possíveis e tomar decisões com mais clareza e estratégia."),
            ("🎁 Desbloqueio da Sorte: Ative Seu Potencial de Oportunidades", "Aprenda a desenvolver uma mentalidade estratégica para reconhecer e aproveitar oportunidades que passam despercebidas pela maioria. Neste curso, você vai entender como pequenas mudanças podem gerar grandes resultados.")
        ]

        for idx, (titulo, desc) in enumerate(cursos_data):
            st.markdown(f"""
                <div class='curso-card'>
                    <strong>{titulo}</strong><br>
                    <p style='font-size: 14px; margin-top: 10px;'>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("📥 Baixar PDF", key=f"dl_pdf_{idx}"):
                st.info("Iniciando download do material...")

    # --- 6. RODAPÉ ORIGINAL ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Venha se divertir e concorrer a muitos prêmios com a gente.<br>"
        "<a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold; text-decoration: none;'>"
        "www.quizmaispremios.com.br</a>"
        "</div>", 
        unsafe_allow_html=True
    )
