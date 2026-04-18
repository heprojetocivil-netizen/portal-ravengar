import streamlit as st
from groq import Groq
import random
from datetime import date

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar",
page_icon="🔮",
layout="wide")

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
    """,
unsafe_allow_html=True)

# --- 2. LÓGICA DE CONEXÃO ---
def consultar_ravengar(pergunta, api_key, setor="Destino"):
    prompts = {
        "Amor": "És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética e profunda.",
        "Trabalho": "És o Ravengar, o Estrategista das Sombras. Tua linguagem é direta e assertiva.",
        "Futuro": "És o Ravengar, o Profeta do Tempo. Tua linguagem é enigmática e mística.",
        "Saude": "És o Ravengar, o Alquimista da Vitalidade. Tua linguagem é serena e equilibrada.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com sabedoria ancestral.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa com precisão cirúrgica.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística e ácida.",
        "Tarot": "És o Ravengar. Interpretas a carta de Tarot com mistério e impacto."
    }
    
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Viajante')}."

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
            st.session_state.nome_user = nome_input
            st.session_state.genero_user = genero_input
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    # --- 5. INTERFACE PRINCIPAL ---
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço"])

    # --- ABA 1: ORÁCULO ---
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR", key="btn_Amor"): st.session_state.setor = "Amor"
        with c2: 
            if st.button("💼 TRABALHO", key="btn_Trabalho"): st.session_state.setor = "Trabalho"
        with c3: 
            if st.button("✨ FUTURO", key="btn_Futuro"): st.session_state.setor = "Futuro"
        with c4: 
            if st.button("🌿 SAÚDE", key="btn_Saude"): st.session_state.setor = "Saude"
        
        setor_atual = st.session_state.get('setor', 'Destino')
        pergunta_ora = st.text_area(f"O que desejas saber sobre o teu {setor_atual}?")
        if st.button("PROFERIR VEREDITO"):
            if chave_api and pergunta_ora:
                st.session_state['chat_ora'] = consultar_ravengar(pergunta_ora, chave_api, setor_atual)
        if 'chat_ora' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{st.session_state['chat_ora']}</div>", unsafe_allow_html=True)

    # --- ABA 2: DECIFRADOR ---
    with tabs[1]:
        texto_dec = st.text_area("Descreve o símbolo ou sonho:")
        if st.button("DECIFRAR MISTÉRIO"):
            if chave_api and texto_dec:
                st.session_state['chat_dec'] = consultar_ravengar(texto_dec, chave_api, "Decifrador")
        if 'chat_dec' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>👁️ {st.session_state['chat_dec']}</div>", unsafe_allow_html=True)

    # --- ABA 3: DETETIVE VIRTUAL ---
    with tabs[2]:
        nome_alvo = st.text_input("Quem vamos investigar?")
        comp = st.text_area("Descreve o comportamento:")
        if st.button("INICIAR INVESTIGAÇÃO"):
            if chave_api and comp:
                st.session_state['chat_det'] = consultar_ravengar(f"Investigar {nome_alvo}: {comp}", chave_api, "Detetive")
        if 'chat_det' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>🕵️ **Relatório:**<br>{st.session_state['chat_det']}</div>", unsafe_allow_html=True)

    # --- ABA 4: QUIZ PSICOLÓGICO ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2>"
                        "<h4>Faça o teste e descubra camadas da sua personalidade.</h4></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado = True
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
        else:
            g = st.session_state.genero_user
            um, guerr = ("um", "guerreiro") if g == "Masculino" else ("uma", "guerreira")
            
            perguntas = [
                {"contexto": "Você caminha por uma floresta densa...", "p": "Nesta caminhada, você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Independente.", "Com alguém": "Sociável."}},
                {"contexto": "Um animal surge.", "p": "Qual é?", "o": ["Lobo", "Coelho"], "s": {"Lobo": f"Age como {um} {guerr}.", "Coelho": "Busca calma."}}
            ]

            if st.session_state.passo < len(perguntas):
                q = perguntas[st.session_state.passo]
                st.info(q['contexto'])
                st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
                cols = st.columns(len(q['o']))
                for i, opt in enumerate(q['o']):
                    if cols[i].button(opt, key=f"qz_{st.session_state.passo}_{i}"):
                        st.session_state.analise.append(q['s'][opt])
                        st.session_state.passo += 1
                        st.rerun()
            else:
                st.markdown(f"<div class='ravengar-card'><h3>Veredito de {st.session_state.nome_user}</h3><p>{' '.join(st.session_state.analise)}</p></div>", unsafe_allow_html=True)
                if st.button("REINICIAR JORNADA"): 
                    st.session_state.quiz_iniciado = False
                    st.rerun()

    # --- ABA 5: BIBLIOTECA SECRETA ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>🔮 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Amor Oculto", "desc": "Sinais silenciosos de sentimentos."},
            {"id": "f2", "titulo": "🔥 Ritual II — Desapego", "desc": "Práticas para libertar a mente."}
        ]
        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button("🔓 Aceder", key=item["id"]):
                st.warning("Conhecimento Revelado!")

    # --- ABA 6: SEU ESPAÇO ---
    with tabs[5]:
        st.markdown("<h2 style='text-align: center;'>🧘 SEU ESPAÇO</h2>", unsafe_allow_html=True)
        
        st.markdown("### 📰 Radar do Ravengar")
        tema_escolhido = st.selectbox("Assunto:", ["Trabalho", "Amor", "Mistérios"])
        if st.button("BUSCAR NO ÉTER"):
            if chave_api:
                st.session_state['noticias_dia'] = consultar_ravengar(f"3 notícias sobre {tema_escolhido}.", chave_api, "Noticias")
        if 'noticias_dia' in st.session_state:
            st.markdown(f"<div class='ravengar-card'>{st.session_state['noticias_dia']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🃏 Tarot do Dia")
        hoje = str(date.today())
        
        # Se for um novo dia ou nunca clicou, mostra o botão
        if st.session_state.get('data_clique_tarot') != hoje:
            if st.button("PUXAR CARTA DO DIA"):
                if chave_api:
                    cartas = ["O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador", "O Hierofante", "Os Enamorados", "O Carro", "A Justiça", "O Eremita", "A Roda da Fortuna", "A Força", "O Pendurado", "A Morte", "A Temperança", "O Diabo", "A Torre", "A Estrela", "A Lua", "O Sol", "O Julgamento", "O Mundo", "O Louco"]
                    carta_sorteada = random.choice(cartas)
                    res = consultar_ravengar(f"Carta '{carta_sorteada}'. Veredito curto.", chave_api, "Tarot")
                    st.session_state['carta_dia'] = (carta_sorteada, res)
                    st.session_state['data_clique_tarot'] = hoje
                    st.rerun()
        else:
            st.info("🔮 A carta de hoje já cumpriu seu papel… mas o destino nunca repete mensagens. Volte amanhã e veja o que ele decide te mostrar.")

        # Exibe a carta salva para o dia atual
        if 'carta_dia' in st.session_state and st.session_state.get('data_clique_tarot') == hoje:
            c, t = st.session_state['carta_dia']
            st.markdown(f"<div class='ravengar-card' style='text-align: center;'><h2>{c}</h2><p>{t}</p></div>", unsafe_allow_html=True)

    # --- 6. RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666; padding: 20px;'>www.quizmaispremios.com.br</div>", unsafe_allow_html=True)
