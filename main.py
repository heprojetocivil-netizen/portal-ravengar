import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    .stApp p, .stApp span, .stApp label, h1, h2, h3 { color: #000000 !important; }
    
    /* Botões Rosa Ravengar */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        transition: 0.3s;
    }
    
    /* Cartões de Resposta */
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        color: #000000 !important;
        margin-bottom: 20px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab-active"] { border-bottom: 3px solid #FFD1DC !important; }
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
st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção", "🧠 Quiz Psicológico"])

# --- ABA 1: ORÁCULO ---
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

# --- ABA 2: DECIFRADOR ---
with tab2:
    st.markdown("### 👁️ O Decifrador")
    texto_dec = st.text_area("Insira o enigma, sonho ou mensagem:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            res = consultar_ravengar("Você é o Ravengar, decifrador de símbolos.", texto_dec, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

# --- ABA 3: TESTE DE INTENÇÃO ---
with tab3:
    st.markdown("### 🔥 Teste de Intenção Real")
    col_a, col_b = st.columns(2)
    with col_a: nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo")
    with col_b: genero = st.radio("Essa pessoa é:", ["Homem", "Mulher"])
    comportamento = st.text_area("Descreva o comportamento suspeito:", key="comp_input")

    if st.button("DEVASSAR INTENÇÃO"):
        if not chave_api or not comportamento:
            st.error("Preencha a chave e o comportamento.")
        else:
            prompt_init = f"Você é o Ravengar. Analise as intenções de {nome_alvo}. Termine com uma pergunta provocativa."
            res_inicial = consultar_ravengar(prompt_init, comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]

    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            if msg['role'] == "ravengar":
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"👤 **Você:** {msg['content']}")

        with st.form(key="form_conversa", clear_on_submit=True):
            resp_usuario = st.text_input("Sua resposta para o Ravengar:")
            c1, c2 = st.columns(2)
            if c1.form_submit_button("ENVIAR RESPOSTA") and resp_usuario:
                st.session_state['historico'].append({"role": "user", "content": resp_usuario})
                hist_full = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state['historico']])
                nova_res = consultar_ravengar(f"Ravengar, histórico: {hist_full}", "Continue o diálogo.", chave_api)
                st.session_state['historico'].append({"role": "ravengar", "content": nova_res})
                st.rerun()
            if c2.form_submit_button("🔄 RESETAR"):
                del st.session_state['historico']
                st.rerun()

# --- ABA 4: QUIZ PSICOLÓGICO (A FLORESTA) ---
with tab4:
    st.markdown("### 🧠 Jornada na Floresta")
    perguntas = [
        {"p": "Você caminha pela floresta... está:", "o": ["Sozinha(o)", "Acompanhada(o)"], "s": {"Sozinha(o)": "Independência emocional.", "Acompanhada(o)": "Valoriza conexão e apoio."}},
        {"p": "Vê um animal na sua frente:", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": "Vê problemas como grandes desafios.", "Coelho": "Evita conflitos e busca paz.", "Pássaro": "Lida com a vida com leveza."}},
        {"p": "Sua reação ao ver o animal:", "o": ["Fujo", "Encaro"], "s": {"Fujo": "Evita situações difíceis.", "Encaro": "Enfrenta os problemas de frente."}},
        {"p": "A estrada que você encontra é de:", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Busca segurança e planejamento.", "Terra": "Gosta de liberdade e do incerto."}},
        {"p": "A casa que você vê é:", "o": ["Grande", "Pequena"], "s": {"Grande": "Ambição e desejo de crescimento.", "Pequena": "Valoriza paz e simplicidade."}},
        {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": "Pessoa reservada e protegida.", "Não": "Pessoa aberta e receptiva."}},
        {"p": "A mesa da casa está:", "o": ["Cheia", "Vazia"], "s": {"Cheia": "Sente-se conectado socialmente.", "Vazia": "Sente falta de conexão no momento."}},
        {"p": "Vê uma xícara no chão. O que faz?", "o": ["Pego", "Deixo"], "s": {"Pego": "Valoriza memórias e o passado.", "Deixo": "Vive o presente e o desapego."}},
        {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Amor é delicado e precioso.", "Metal": "Amor é forte e duradouro."}},
        {"p": "No lago final, você:", "o": ["Mergulho", "Molho apenas as mãos", "Sigo direto"], "s": {"Mergulho": "Entrega total nas emoções.", "Molho apenas as mãos": "Equilíbrio e controle.", "Sigo direto": "Foco total em objetivos."}}
    ]

    if 'passo' not in st.session_state: st.session_state.passo = 0
    if 'analise' not in st.session_state: st.session_state.analise = []

    if st.session_state.passo < len(perguntas):
        q = perguntas[st.session_state.passo]
        st.write(f"**{q['p']}**")
        cols = st.columns(len(q['o']))
        for i, opt in enumerate(q['o']):
            if cols[i].button(opt, key=f"q_{st.session_state.passo}_{i}"):
                st.session_state.analise.append(q['s'][opt])
                st.session_state.passo += 1
                st.rerun()
    else:
        st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
        st.markdown("### 🔮 Perfil da sua Alma")
        for item in st.session_state.analise:
            st.write(f"• {item}")
        if st.button("RECOMEÇAR JORNADA"):
            st.session_state.passo = 0
            st.session_state.analise = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
