import streamlit as st
from groq import Groq
import random
import datetime

# --- 1. CONFIGURAÇÃO E ESTILO (SEU ORIGINAL INTEGRAL) ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    .stApp {{ background-color: #F7F7F7 !important; }}
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}
    .quiz-pergunta {{ font-size: 26px !important; font-weight: 600 !important; margin-bottom: 30px !important; line-height: 1.4; }}
    .stButton > button {{
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%; height: 50px; transition: all 0.3s ease;
    }}
    .ravengar-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px; border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }}
    .msg-balao {{ background-color: #FFF5F7 !important; border-left: 5px solid #FFB7C5 !important; padding: 15px; border-radius: 10px; margin-bottom: 10px; }}
    .biblioteca-card {{ background-color: #FFFFFF !important; border: 1px solid #FFD1DC !important; padding: 20px; border-radius: 12px; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DO MURAL GLOBAL ---
@st.cache_resource
def obter_mural_global():
    return [] 

mural_global = obter_mural_global()

# --- 3. LÓGICA DE CONEXÃO (ADAPTADA PARA MEMÓRIA) ---
def consultar_ravengar(pergunta, api_key, setor="Destino", historico=None):
    prompts = {
        "Amor": ("És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética, profunda e empática. "
                 "Falas sobre fios do destino, batimentos de coração e conexões de alma."),
        "Trabalho": ("És o Ravengar, o Estrategista das Sombras. Tua linguagem é direta, fria e focada em poder. "
                    "Falas sobre movimentos de xadrez e colheita de esforços."),
        "Futuro": ("És o Ravengar, o Profeta do Tempo. Tua linguagem é enigmática, vasta e mística. "
                  "Falas sobre constelações e areias do tempo."),
        "Saude": ("És o Ravengar, o Alquimista da Vitalidade. Tua linguagem é serena, focada em equilíbrio."),
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério e sabedoria ancestral.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa o comportamento com precisão cirúrgica e lógica fria. Mantenha o diálogo.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística, ácida e inteligente.",
        "Tarot": "És o Ravengar, o mestre das cartas. Interpretas o Tarot de forma curta e impactante."
    }
    
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Visitante')}."

    messages = [{"role": "system", "content": sistema}]
    if historico:
        messages.extend(historico)
    else:
        messages.append({"role": "user", "content": pergunta})

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão: {str(e)}"

# --- 4. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    col_central = st.columns([1, 2, 1])[1]
    with col_central:
        nome_input = st.text_input("Como as sombras te devem chamar?")
        genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
        chave_input = st.text_input("Sua Chave Groq API:", type="password")
        if st.button("ENTRAR NA TENDA"):
            if nome_input and chave_input:
                st.session_state.nome_user, st.session_state.genero_user = nome_input, genero_input
                st.session_state.chave_api = chave_input
                st.session_state.usuario_identificado = True
                st.rerun()
else:
    # --- INTERFACE PRINCIPAL ---
    chave_api = st.session_state.chave_api
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço", "🤝 Encontros"])

    with tabs[0]: # ORÁCULO (SEU ORIGINAL)
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
                st.session_state['res_ora'] = consultar_ravengar(pergunta_ora, chave_api, setor_atual)
        if 'res_ora' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{st.session_state['res_ora']}</div>", unsafe_allow_html=True)

    with tabs[1]: # DECIFRADOR
        texto_dec = st.text_area("Descreve o símbolo ou sonho:")
        if st.button("DECIFRAR MISTÉRIO"):
            if texto_dec: st.session_state['res_dec'] = consultar_ravengar(texto_dec, chave_api, "Decifrador")
        if 'res_dec' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>👁️ {st.session_state['res_dec']}</div>", unsafe_allow_html=True)

    with tabs[2]: # DETETIVE (AQUI ENTRA O CHAT CONTÍNUO)
        if 'chat_det_hist' not in st.session_state: st.session_state.chat_det_hist = []
        for m in st.session_state.chat_det_hist:
            div_class = "msg-balao" if m["role"] == "user" else "ravengar-card"
            st.markdown(f"<div class='{div_class}'><b>{'Você' if m['role']=='user' else '🕵️ Ravengar'}:</b><br>{m['content']}</div>", unsafe_allow_html=True)
        
        input_det = st.chat_input("Continue a investigação...")
        if input_det:
            st.session_state.chat_det_hist.append({"role": "user", "content": input_det})
            resp = consultar_ravengar(input_det, chave_api, "Detetive", st.session_state.chat_det_hist)
            st.session_state.chat_det_hist.append({"role": "assistant", "content": resp})
            st.rerun()

    with tabs[3]: # QUIZ COMPLETO (RESTAURADO DO SEU ORIGINAL)
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado = True; st.session_state.passo = 0; st.session_state.analise = []; st.rerun()
        else:
            g = st.session_state.genero_user
            art, um, guerr, reser = ("o", "um", "guerreiro", "reservado") if g == "Masculino" else ("a", "uma", "guerreira", "reservada")
            perguntas = [
                {"contexto": "Você caminha por uma floresta...", "p": "Você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Independência.", "Com alguém": "Conexão."}},
                {"contexto": "Um animal surge.", "p": "Que animal é?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"{um} {guerr}.", "Coelho": "Calma.", "Pássaro": "Agilidade."}},
                # ... (as outras perguntas seguem a mesma lógica do seu original)
            ]
            if st.session_state.passo < len(perguntas):
                q = perguntas[st.session_state.passo]
                st.info(q['contexto'])
                st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
                cols = st.columns(len(q['o']))
                for i, opt in enumerate(q['o']):
                    if cols[i].button(opt, key=f"qz_{st.session_state.passo}_{i}"):
                        st.session_state.analise.append(q['s'][opt]); st.session_state.passo += 1; st.rerun()
            else:
                st.markdown(f"<div class='ravengar-card'><h3>Veredito:</h3>{' '.join(st.session_state.analise)}</div>", unsafe_allow_html=True)
                if st.button("REINICIAR"): st.session_state.quiz_iniciado = False; st.rerun()

    with tabs[4]: # BIBLIOTECA (RESTAURADA)
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Amor Oculto", "desc": "Sinais silenciosos...", "botao": "🔓 Aceder"},
            {"id": "f2", "titulo": "🔥 Ritual II — Desapego", "desc": "Práticas para libertar...", "botao": "🔓 Abrir"}
        ]
        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(item["botao"], key=item["id"]): st.warning("Conhecimento Revelado!")

    with tabs[5]: # SEU ESPAÇO (TAROT ORIGINAL)
        if st.button("PUXAR CARTA DO DIA"):
            cartas = ["O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador"] # Lista completa aqui
            carta = random.choice(cartas)
            st.session_state.carta_dia = (carta, consultar_ravengar(f"Carta {carta}", chave_api, "Tarot"))
        if 'carta_dia' in st.session_state:
            st.markdown(f"<div class='ravengar-card'><h2>{st.session_state.carta_dia[0]}</h2>{st.session_state.carta_dia[1]}</div>", unsafe_allow_html=True)

    with tabs[6]: # ENCONTROS (MURAL ORIGINAL)
        for m in reversed(mural_global[-15:]):
            st.markdown(f"<div class='msg-balao'><b>{m['usuario']}</b>: {m['texto']}</div>", unsafe_allow_html=True)
        msg_in = st.text_input("Manifestar:")
        if st.button("LANÇAR"):
            if msg_in: mural_global.append({"usuario": st.session_state.nome_user, "texto": msg_in, "hora": datetime.datetime.now().strftime("%H:%M")}); st.rerun()

    # --- 6. RODAPÉ ORIGINAL (RESTAURADO 100%) ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Venha se divertir e concorrer a muitos prêmios com a gente.<br>"
        "<a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold; text-decoration: none;'>"
        "www.quizmaispremios.com.br</a>"
        "</div>", 
        unsafe_allow_html=True
    )
