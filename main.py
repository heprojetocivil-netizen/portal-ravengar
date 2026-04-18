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
def consultar_ravengar(pergunta, api_key, setor="Destino"):
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
        pergunta_ora = st.text_area(f"O que desejas saber sobre o teu {setor}?")
        if st.button("PROFERIR VEREDITO"):
            if chave_api and pergunta_ora:
                st.session_state['chat_ora'] = [{"content": consultar_ravengar(pergunta_ora, chave_api, setor)}]
        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 2: DECIFRADOR ---
    with tabs[1]:
        texto_dec = st.text_area("Descreve o símbolo ou sonho:")
        if st.button("DECIFRAR MISTÉRIO"):
            if chave_api and texto_dec:
                st.session_state['chat_dec'] = [{"content": consultar_ravengar(texto_dec, chave_api, "Decifrador")}]
        if 'chat_dec' in st.session_state:
            for msg in st.session_state['chat_dec']:
                st.markdown(f"<div class='ravengar-card'>👁️ {msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 3: DETETIVE VIRTUAL ---
    with tabs[2]:
        nome_alvo = st.text_input("Quem vamos investigar?")
        comp = st.text_area("Descreve o comportamento:")
        if st.button("INICIAR INVESTIGAÇÃO"):
            if chave_api and comp:
                st.session_state['chat_det'] = [{"content": consultar_ravengar(f"Investigar {nome_alvo}: {comp}", chave_api, "Detetive")}]
        if 'chat_det' in st.session_state:
            for msg in st.session_state['chat_det']:
                st.markdown(f"<div class='ravengar-card'>🕵️ **Relatório:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 4: QUIZ PSICOLÓGICO ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
            st.markdown("## Você acha que se conhece bem? 🤔")
            st.markdown("#### Faça o nosso teste e descubra camadas da sua personalidade que você nunca percebeu.")
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado = True
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
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
                st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
                st.markdown(f"<h3>O Veredito Psicológico de {st.session_state.nome_user}</h3>", unsafe_allow_html=True)
                st.write(" ".join(st.session_state.analise))
                if st.button("REINICIAR JORNADA"): 
                    st.session_state.quiz_iniciado = False
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # --- ABA 5: BIBLIOTECA SECRETA ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>🔮 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Amor Oculto", "desc": "Sinais silenciosos de sentimentos.", "botao": "🔓 Aceder", "link": "#"},
            {"id": "f2", "titulo": "🔥 Ritual II — Desapego", "desc": "Libertar a mente do passado.", "botao": "🔓 Abrir", "link": "#"}
        ]
        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(item["botao"], key=item["id"]):
                st.warning(f"**Revelado:** [BAIXAR AQUI]({item['link']})")

    # --- 6. RODAPÉ ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Venha se divertir e concorrer a muitos prêmios com a gente.<br>"
        "<a href='http://www.quizmaispremios.com.br' target='_blank' style='color: #FF69B4; font-weight: bold; text-decoration: none;'>"
        "www.quizmaispremios.com.br</a>"
        "</div>", 
        unsafe_allow_html=True
    )
