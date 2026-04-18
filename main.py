import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    
    /* Estilo dos Cards e Balões */
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    .stButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 50px;
        width: 100%;
    }

    .biblioteca-card {
        background-color: #FFFFFF !important;
        border: 1px solid #FFD1DC !important;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE IA COM MEMÓRIA ---
def consultar_ravengar(pergunta, api_key, setor, historico):
    prompt_sistema = f"És o Ravengar, especialista em {setor}. Nome do consulente: {st.session_state.get('nome_user', 'Desconhecido')}."
    
    mensagens = [{"role": "system", "content": prompt_sistema}]
    for msg in historico:
        role = "assistant" if msg["role"] == "assistant" else "user"
        mensagens.append({"role": role, "content": msg["content"]})
    mensagens.append({"role": "user", "content": pergunta})

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(messages=mensagens, model="llama-3.3-70b-versatile")
        return completion.choices[0].message.content
    except Exception as e:
        return f"A conexão mística falhou: {str(e)}"

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")
    if st.button("🔄 REINICIAR TUDO"):
        st.session_state.clear()
        st.rerun()

# --- 4. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    nome = st.text_input("Como as sombras te devem chamar?")
    genero = st.radio("Teu género:", ["Masculino", "Feminino"])
    if st.button("ENTRAR NA TENDA"):
        if nome:
            st.session_state.nome_user, st.session_state.genero_user = nome, genero
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    st.markdown(f"<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz", "👉 Biblioteca"])

    # --- ABA 1: ORÁCULO ---
    with tabs[0]:
        if 'chat_ora' not in st.session_state: st.session_state.chat_ora = []
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR"): st.session_state.setor = "Amor"
        with c2: 
            if st.button("💼 TRABALHO"): st.session_state.setor = "Trabalho"
        with c3: 
            if st.button("✨ FUTURO"): st.session_state.setor = "Futuro"
        with c4: 
            if st.button("🌿 SAÚDE"): st.session_state.setor = "Saúde"
        
        setor_atual = st.session_state.get('setor', 'Destino')
        if prompt_ora := st.chat_input(f"Pergunta ao Oráculo sobre {setor_atual}..."):
            if chave_api:
                st.session_state.chat_ora.append({"role": "user", "content": prompt_ora})
                res = consultar_ravengar(prompt_ora, chave_api, setor_atual, st.session_state.chat_ora)
                st.session_state.chat_ora.append({"role": "assistant", "content": res})
        
        for msg in reversed(st.session_state.chat_ora):
            st.markdown(f"<div class='ravengar-card'><b>{'👤 Você' if msg['role']=='user' else '🔮 Ravengar'}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 2: DECIFRADOR ---
    with tabs[1]:
        if 'chat_dec' not in st.session_state: st.session_state.chat_dec = []
        if prompt_dec := st.chat_input("Descreve o teu sonho ou símbolo..."):
            if chave_api:
                st.session_state.chat_dec.append({"role": "user", "content": prompt_dec})
                res = consultar_ravengar(prompt_dec, chave_api, "Decifrador", st.session_state.chat_dec)
                st.session_state.chat_dec.append({"role": "assistant", "content": res})
        
        for msg in reversed(st.session_state.chat_dec):
            st.markdown(f"<div class='ravengar-card'><b>{'👤 Você' if msg['role']=='user' else '👁️ Ravengar'}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 3: DETETIVE VIRTUAL (CHAT CONTÍNUO) ---
    with tabs[2]:
        if 'chat_det' not in st.session_state: st.session_state.chat_det = []
        
        # O Chat Input fica fixo no rodapé da aba
        if prompt_det := st.chat_input("Relata o comportamento suspeito ao Detetive..."):
            if chave_api:
                st.session_state.chat_det.append({"role": "user", "content": prompt_det})
                resposta = consultar_ravengar(prompt_det, chave_api, "Detetive Virtual", st.session_state.chat_det)
                st.session_state.chat_det.append({"role": "assistant", "content": resposta})
                st.rerun()

        for msg in reversed(st.session_state.chat_det):
            st.markdown(f"<div class='ravengar-card'><b>{'👤 Você' if msg['role']=='user' else '🕵️ Detetive'}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # --- ABA 4: QUIZ PSICOLÓGICO ---
    with tabs[3]:
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 20px;'><h2>Descobre a tua verdadeira essência 🧠</h2></div>", unsafe_allow_html=True)
            if st.button("INICIAR TESTE"):
                st.session_state.quiz_iniciado, st.session_state.passo, st.session_state.analise = True, 0, []
                st.rerun()
        else:
            # Lógica simplificada das perguntas para manter o código limpo
            st.write(f"Pergunta {st.session_state.passo + 1} de 10")
            if st.button("Próxima Pergunta (Simulação)"):
                st.session_state.passo += 1
                if st.session_state.passo >= 10:
                    st.success("Teste concluído! Veredito: Tens uma mente estratégica e resiliente.")
                    if st.button("Reiniciar"): st.session_state.quiz_iniciado = False; st.rerun()

    # --- ABA 5: BIBLIOTECA (5 EBOOKS) ---
    with tabs[4]:
        st.markdown("<h2 style='text-align: center;'>📚 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        ebooks = [
            ("❤️ Fragmento I — Amor Oculto", "Sinais silenciosos de sentimentos."),
            ("🔥 Ritual II — Desapego", "Libertar a mente de conexões passadas."),
            ("🌙 Fragmento III — Leis do Destino", "O que as coincidências dizem."),
            ("🧠 Código IV — A Mente Alheia", "Ler intenções e comportamentos."),
            ("🕯️ Fragmento V — Proteção Energética", "Blindagem espiritual diária.")
        ]
        for titulo, desc in ebooks:
            st.markdown(f"<div class='biblioteca-card'><h4>{titulo}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
            st.button(f"Desbloquear {titulo.split('—')[0]}", key=titulo)

    # --- RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>Acompanha os prémios em <a href='http://www.quizmaispremios.com.br'>www.quizmaispremios.com.br</a></div>", unsafe_allow_html=True)
