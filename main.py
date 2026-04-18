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

    .biblioteca-card {{
        background-color: #FFFFFF !important;
        border: 1px solid #FFD1DC !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE CONEXÃO ---
def consultar_ravengar(pergunta, api_key, setor="Destino", historico=[]):
    prompts = {
        "Amor": "És o Ravengar. Analisa conexões de alma e sentimentos.",
        "Trabalho": "És o Ravengar. Analisa estratégia e poder.",
        "Futuro": "És o Ravengar. Vês o que o tempo esconde.",
        "Saude": "És o Ravengar. Analisa a energia vital.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa o comportamento da pessoa mencionada com precisão. Foca no alvo da investigação."
    }
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome: {st.session_state.nome_user}."

    mensagens = [{"role": "system", "content": sistema}]
    for msg in historico:
        role = "assistant" if msg["role"] == "ravengar" else "user"
        mensagens.append({"role": role, "content": msg["content"]})
    mensagens.append({"role": "user", "content": pergunta})

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=mensagens,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

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
            st.session_state.nome_user, st.session_state.genero_user = nome_input, genero_input
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    # --- 5. INTERFACE PRINCIPAL ---
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta"])

    # --- ABA 1: ORÁCULO ---
    with tabs[0]:
        if 'chat_ora' not in st.session_state: st.session_state.chat_ora = []
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR", key="btn_Amor"): st.session_state.setor = "Amor"; st.rerun()
        with c2: 
            if st.button("💼 TRABALHO", key="btn_Trabalho"): st.session_state.setor = "Trabalho"; st.rerun()
        with c3: 
            if st.button("✨ FUTURO", key="btn_Futuro"): st.session_state.setor = "Futuro"; st.rerun()
        with c4: 
            if st.button("🌿 SAÚDE", key="btn_Saude"): st.session_state.setor = "Saude"; st.rerun()
        
        setor = st.session_state.get('setor', 'Destino')
        pergunta_ora = st.text_input(f"O que desejas saber sobre o teu {setor}?", key="in_ora")
        if st.button("PROFERIR VEREDITO", key="bt_ora"):
            if chave_api and pergunta_ora:
                res = consultar_ravengar(pergunta_ora, chave_api, setor, st.session_state.chat_ora)
                st.session_state.chat_ora.append({"role": "user", "content": pergunta_ora})
                st.session_state.chat_ora.append({"role": "ravengar", "content": res})
        
        for msg in reversed(st.session_state.chat_ora):
            label = "👤 Você" if msg["role"] == "user" else "🔮 Ravengar"
            st.markdown(f"<div class='ravengar-card'>**{label}:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 2: DECIFRADOR ---
    with tabs[1]:
        if 'chat_dec' not in st.session_state: st.session_state.chat_dec = []
        texto_dec = st.text_input("Descreve o símbolo ou sonho:", key="in_dec")
        if st.button("DECIFRAR MISTÉRIO", key="bt_dec"):
            if chave_api and texto_dec:
                res = consultar_ravengar(texto_dec, chave_api, "Decifrador", st.session_state.chat_dec)
                st.session_state.chat_dec.append({"role": "user", "content": texto_dec})
                st.session_state.chat_dec.append({"role": "ravengar", "content": res})
        
        for msg in reversed(st.session_state.chat_dec):
            label = "👤 Você" if msg["role"] == "user" else "👁️ Ravengar"
            st.markdown(f"<div class='ravengar-card'>**{label}:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 3: DETETIVE VIRTUAL (RESTAURADA) ---
    with tabs[2]:
        if 'chat_det' not in st.session_state: st.session_state.chat_det = []
        pergunta_det = st.text_input("Descreve o comportamento suspeito:", key="in_det")
        if st.button("INICIAR/CONTINUAR INVESTIGAÇÃO", key="bt_det"):
            if chave_api and pergunta_det:
                res = consultar_ravengar(pergunta_det, chave_api, "Detetive", st.session_state.chat_det)
                st.session_state.chat_det.append({"role": "user", "content": pergunta_det})
                st.session_state.chat_det.append({"role": "ravengar", "content": res})
        
        for msg in reversed(st.session_state.chat_det):
            label = "👤 Você" if msg["role"] == "user" else "🕵️ Detetive Ravengar"
            st.markdown(f"<div class='ravengar-card'>**{label}:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 4: QUIZ PSICOLÓGICO ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2><h4>Faça o nosso teste e descubra camadas da sua personalidade.</h4></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado, st.session_state.passo, st.session_state.analise = True, 0, []
                st.rerun()
        else:
            g = st.session_state.genero_user
            art, um, guerr, reser = ("o", "um", "guerreiro", "reservado") if g == "Masculino" else ("a", "uma", "guerreira", "reservada")
            perguntas = [
                {"contexto": "Você caminha por uma floresta densa...", "p": "Nesta caminhada, você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Sua essência é de independência.", "Com alguém": "Você valoriza conexões próximas."}},
                {"contexto": "De repente, um animal surge à sua frente.", "p": "Que animal é este?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Sua mente age como {um} {guerr}.", "Coelho": "Sua natureza busca calma.", "Pássaro": "Sua agilidade mental é rara."}},
                {"contexto": "O animal encara você fixamente.", "p": "Qual é a sua reação imediata?", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "Sua inteligência é movida pela cautela.", "Permanecer": "Você não teme o desconhecido."}},
                {"contexto": "A floresta abre-se, revelando uma estrada.", "p": "Como é esta estrada?", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você opera com planejamento.", "Terra": "Seu espírito vibra na liberdade."}},
                {"contexto": "Você avista uma casa solitária.", "p": "Como descreveria esta casa?", "o": ["Grande", "Pequena"], "s": {"Grande": "Suas ambições são vastas.", "Pequena": "Sua alma entende o essencial."}},
                {"contexto": "Você aproxima-se da entrada.", "p": "A casa possui uma cerca ao redor?", "o": ["Sim", "Não"], "s": {"Sim": f"Você é {reser}, protegendo seu interior.", "Não": "Você acredita na transparência."}},
                {"contexto": "Você entra. Há uma mesa de jantar na sala.", "p": "Como está esta mesa?", "o": ["Farta", "Vazia"], "s": {"Farta": "Você vive um momento de conexão emocional.", "Vazia": "Você busca algo profundo que ainda não encontrou."}},
                {"contexto": "Você nota uma xícara caída no chão.", "p": "O que você faz ao vê-la?", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Você valoriza o que moldou seu passado.", "Ignora": "Seu foco está no horizonte à frente."}},
                {"contexto": "Você observa o material da xícara.", "p": "De que material ela é?", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Sua visão sobre o afeto é refinada.", "Metal": "Sua lealdade é inquebrável."}},
                {"contexto": "Ao sair, encontra um lago sereno.", "p": "Diante da água, qual sua atitude?", "o": ["Mergulha", "Toca a água", "Contempla"], "s": {"Mergulha": "Você se entrega de corpo e alma nos relacionamentos.", "Toca a água": "Você domina o equilíbrio.", "Contempla": f"Você é {um} observador {reser}."}}
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
                st.markdown(f"<div class='ravengar-card'><h3>O Veredito Psicológico de {st.session_state.nome_user}</h3><p>{' '.join(st.session_state.analise)}</p></div>", unsafe_allow_html=True)
                if st.button("REINICIAR JORNADA"): st.session_state.quiz_iniciado = False; st.rerun()

    # --- ABA 5: BIBLIOTECA SECRETA (5 EBOOKS) ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>🔮 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Amor Oculto", "desc": "Sinais silenciosos de sentimentos.", "botao": "🔓 Aceder", "link": "#"},
            {"id": "f2", "titulo": "🔥 Ritual II — Desapego", "desc": "Libertar a mente do passado.", "botao": "🔓 Abrir", "link": "#"},
            {"id": "f3", "titulo": "🌙 Fragmento III — Leis do Destino", "desc": "O que as coincidências dizem.", "botao": "🔓 Ver Destino", "link": "#"},
            {"id": "f4", "titulo": "🧠 Código IV — A Mente Alheia", "desc": "Ler intenções e comportamentos.", "botao": "🔓 Decifrar", "link": "#"},
            {"id": "f5", "titulo": "🕯️ Fragmento V — Proteção", "desc": "Blindagem espiritual diária.", "botao": "🔓 Fortalecer", "link": "#"}
        ]
        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(item["botao"], key=item["id"]): st.warning(f"**Revelado:** [BAIXAR AQUI]({item['link']})")

    # --- 6. RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>Venha se divertir e concorrer a muitos prêmios com a gente.<br><a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold;'>www.quizmaispremios.com.br</a></div>", unsafe_allow_html=True)
