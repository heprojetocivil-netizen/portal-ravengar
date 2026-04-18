import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

setor_ativo = st.session_state.get('setor', '')

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}

    .quiz-pergunta {{
        font-size: 28px !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-bottom: 35px !important;
        line-height: 1.4;
    }}

    .stButton > button, div.stFormSubmitButton > button {{
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
        transition: all 0.3s ease;
    }}

    /* Estilo das Esferas */
    button[key*="Amor"] {{ background-color: { "#FFB2C1" if setor_ativo == "Amor" else "#FFD1DC" } !important; border: { "2px solid #FF69B4" if setor_ativo == "Amor" else "1px solid #FFB7C5" } !important; }}
    button[key*="Trabalho"] {{ background-color: { "#FFB2C1" if setor_ativo == "Trabalho" else "#FFD1DC" } !important; border: { "2px solid #FF69B4" if setor_ativo == "Trabalho" else "1px solid #FFB7C5" } !important; }}
    button[key*="Futuro"] {{ background-color: { "#FFB2C1" if setor_ativo == "Futuro" else "#FFD1DC" } !important; border: { "2px solid #FF69B4" if setor_ativo == "Futuro" else "1px solid #FFB7C5" } !important; }}
    button[key*="Saude"] {{ background-color: { "#FFB2C1" if setor_ativo == "Saude" else "#FFD1DC" } !important; border: { "2px solid #FF69B4" if setor_ativo == "Saude" else "1px solid #FFB7C5" } !important; }}

    .ravengar-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        line-height: 1.6;
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

# --- 2. LÓGICA DE CONEXÃO BLINDADA ---
def consultar_ravengar(pergunta, api_key, setor="Destino"):
    prompts = {
        "Amor": "És o Ravengar. Analisa conexões de alma e sentimentos. És um observador frio e místico.",
        "Trabalho": "És o Ravengar. Analisa estratégia e poder. Revela verdades de mercado.",
        "Futuro": "És o Ravengar. Vês o que o tempo esconde.",
        "Saude": "És o Ravengar. Analisa o templo carnal e a energia vital.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos.",
        "Intencao": "ÉS O RAVENGAR. Analisa a pessoa mencionada. NUNCA fales de ti mesmo."
    }
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome: {st.session_state.nome_user}. Género: {st.session_state.genero_user}."

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão: {str(e)}"

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")
    if st.button("🔄 REINICIAR SESSÃO"):
        for key in list(st.session_state.keys()): del st.session_state[key]
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
    saudacao = "Seja muito bem-vindo" if st.session_state.genero_user == "Masculino" else "Seja muito bem-vinda"
    st.markdown(f"<p style='text-align: center;'>{saudacao}, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Intenção", "🧠 Quiz", "👉 Biblioteca Secreta"])

    # --- ABA 1, 2, 3 (Mantidas) ---
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
                st.session_state['chat_ora'] = [{"role": "ravengar", "content": consultar_ravengar(pergunta_ora, chave_api, setor)}]
        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    with tabs[1]:
        texto_dec = st.text_area("Descreve o símbolo ou sonho:")
        if st.button("DECIFRAR"):
            if chave_api and texto_dec:
                st.session_state['chat_dec'] = [{"role": "ravengar", "content": consultar_ravengar(texto_dec, chave_api, "Decifrador")}]
        if 'chat_dec' in st.session_state:
            for msg in st.session_state['chat_dec']:
                st.markdown(f"<div class='ravengar-card'>🔮 {msg['content']}</div>", unsafe_allow_html=True)

    with tabs[2]:
        nome_alvo = st.text_input("Alvo:")
        comp = st.text_area("Comportamento:")
        if st.button("DESVENDAR"):
            if chave_api and comp:
                st.session_state['chat_int'] = [{"role": "ravengar", "content": consultar_ravengar(f"Analise {nome_alvo}: {comp}", chave_api, "Intencao")}]
        if 'chat_int' in st.session_state:
            for msg in st.session_state['chat_int']:
                st.markdown(f"<div class='ravengar-card'>🔮 {msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 4: QUIZ PSICOLÓGICO RESTAURADO ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
            st.markdown("## Você acha que se conhece bem? 🤔")
            st.markdown("#### Faça o nosso teste e descubra camadas da sua personalidade que você nunca percebeu.")
            if st.button("CLIQUE PARA INICIAR", key="btn_start_quiz"):
                st.session_state.quiz_iniciado = True
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            g = st.session_state.genero_user
            art, um, guerr, reser = ("o", "um", "guerreiro", "reservado") if g == "Masculino" else ("a", "uma", "guerreira", "reservada")
            
            perguntas = [
                {"p": "Caminhas pela floresta... estás:", "o": ["Só", "Com alguém"], "s": {"Só": "Tens uma essência independente.", "Com alguém": "Valorizas a presença alheia."}},
                {"p": "Vês um animal, qual é?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"A tua mente age como {um} {guerr}.", "Coelho": "Buscas refúgio na calma.", "Pássaro": "Tens agilidade mental rara."}},
                {"p": "A tua reação é:", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "És movido pela cautela.", "Permanecer": "Não temes o desconhecido."}},
                {"p": "Como é a estrada?", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Operas com planeamento.", "Terra": "Vibras na liberdade."}},
                {"p": "Como é a casa?", "o": ["Grande", "Pequena"], "s": {"Grande": "Tens ambições vastas.", "Pequena": "Entendes o essencial."}},
                {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": f"És {reser}.", "Não": "Crês na transparência."}},
                {"p": "A mesa está:", "o": ["Farta", "Vazia"], "s": {"Farta": "Estás em conexão emocional.", "Vazia": "Estás em busca profunda."}},
                {"p": "Vês uma xícara no chão:", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Valorizas o passado.", "Ignora": "Focas no horizonte."}},
                {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "O teu afeto é refinado.", "Metal": "A tua lealdade é inquebrável."}},
                {"p": "No lago, tu:", "o": ["Mergulha", "Toca a água", "Contempla"], "s": {"Mergulha": "Entregas-te de corpo e alma.", "Toca a água": "Dominas o equilíbrio.", "Contempla": f"És {um} observador {reser}."}}
            ]

            if st.session_state.passo < len(perguntas):
                q = perguntas[st.session_state.passo]
                st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
                cols = st.columns(len(q['o']))
                for i, opt in enumerate(q['o']):
                    if cols[i].button(opt, key=f"qz_{st.session_state.passo}_{i}"):
                        st.session_state.analise.append(q['s'][opt]); st.session_state.passo += 1; st.rerun()
            else:
                st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
                st.markdown("<h3>O Veredito Psicológico</h3>", unsafe_allow_html=True)
                st.write(" ".join(st.session_state.analise))
                if st.button("REINICIAR JORNADA"): 
                    st.session_state.quiz_iniciado = False
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # --- ABA 5: BIBLIOTECA SECRETA (CORRIGIDA) ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>🔮 BIBLIOTECA SECRETA DE RAVENGAR</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic;'>Nem todo conhecimento deve ser revelado… mas alguns fragmentos encontram-te por um motivo.</p>", unsafe_allow_html=True)
        
        biblioteca = [
            {"id": "f1", "titulo": "❤️ Fragmento I — Os Sinais do Amor Oculto", "desc": "Nem todo sentimento é dito… mas sempre deixa rastros.", "botao": "🔓 Desbloquear agora", "link": "LINK_AQUI"},
            {"id": "f2", "titulo": "🔥 Ritual II — O Desapego", "desc": "Liberta-te de quem ainda prende a tua mente… e recupera o teu poder.", "botao": "🔓 Acessar conhecimento", "link": "LINK_AQUI"},
            {"id": "f3", "titulo": "🌙 Fragmento III — Leis do Destino", "desc": "O que parece acaso… pode ser direção disfarçada.", "botao": "🔓 Ver o que está reservado", "link": "LINK_AQUI"},
            {"id": "f4", "titulo": "🧠 Código IV — A Mente de Quem Deseja", "desc": "Entende o que não é dito… mas pode ser sentido.", "botao": "🔓 Decifrar agora", "link": "LINK_AQUI"},
            {"id": "f5", "titulo": "🕯️ Fragmento V — Energia que Atrai e Afasta", "desc": "Algumas presenças aproximam… outras desaparecem sem explicação.", "botao": "🔓 Desbloquear leitura", "link": "LINK_AQUI"}
        ]

        for item in biblioteca:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p style='color: #666;'>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button(item["botao"], key=item["id"]):
                st.warning(f"""
                    **🔮 Estás prestes a aceder a um conhecimento restrito** Nem todos estão preparados para isto.  
                    
                    [CLICA AQUI PARA CONFIRMAR O ACESSO E DESCARREGAR]({item['link']})
                """)
            st.markdown("<br>", unsafe_allow_html=True)
