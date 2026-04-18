import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    [data-testid="stChatMessage"] { background-color: #FFFFFF !important; border-radius: 15px; border: 1px solid #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNÇÃO DE IA ---
def consultar_ravengar(api_key, setor, historico_mensagens):
    prompts = {
        "Detetive": "Você é o Ravengar, o Detetive Virtual. Analise friamente o comportamento suspeito relatado. Seja místico, direto e use deduções lógicas.",
        "Oráculo": "Você é o Ravengar, um oráculo místico que vê o destino.",
        "Decifrador": "Você é o Ravengar, especialista em traduzir sonhos e símbolos."
    }
    
    contexto = prompts.get(setor, "Você é o Ravengar.")
    
    # Preparamos o pacote de mensagens para a API (Sistema + Histórico)
    mensagens_api = [{"role": "system", "content": contexto}]
    for m in historico_mensagens:
        mensagens_api.append({"role": m["role"], "content": m["content"]})

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=mensagens_api,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

# --- 3. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    nome = st.text_input("Como as sombras te devem chamar?")
    if st.button("ENTRAR NA TENDA"):
        if nome:
            st.session_state.nome_user = nome
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)
    
    aba1, aba2, aba3 = st.tabs(["🕵️ Detetive Virtual", "🧠 Quiz", "📚 Biblioteca"])

    # --- ABA DETETIVE (ESTILO WHATSAPP) ---
    with aba1:
        if 'mensagens_detetive' not in st.session_state:
            st.session_state.mensagens_detetive = []

        # Exibe o histórico estilo chat
        for msg in st.session_state.mensagens_detetive:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Campo de entrada (igual ao rodapé do WhatsApp)
        if prompt := st.chat_input("Diga ao Detetive o que aconteceu..."):
            # Guarda e mostra a pergunta do usuário
            st.session_state.mensagens_detetive.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Busca resposta da IA
            with st.chat_message("assistant", avatar="🕵️"):
                with st.spinner("Analisando evidências..."):
                    resposta = consultar_ravengar(st.secrets.get("GROQ_API_KEY", ""), "Detetive", st.session_state.mensagens_detetive)
                    st.write(resposta)
                    st.session_state.mensagens_detetive.append({"role": "assistant", "content": resposta})

    # --- ABA QUIZ E BIBLIOTECA (Skeletal) ---
    with aba2: st.write("O Quiz está pronto para ser lapidado.")
    with aba3: st.write("Os 5 Ebooks estão seguros aqui.")

    # --- RODAPÉ ---
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>Venha se divertir no <a href='http://www.quizmaispremios.com.br'>www.quizmaispremios.com.br</a></div>", unsafe_allow_html=True)
