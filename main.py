import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    
    /* Fonte reta e limpa para todo o app */
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }

    /* Pergunta do Quiz: Centralizada, Grande e Reta */
    .quiz-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 0;
    }
    .quiz-pergunta {
        font-size: 28px !important;
        font-weight: 600 !important;
        color: #000000 !important;
        text-align: center !important;
        margin-bottom: 40px !important;
        line-height: 1.5;
    }
    
    div.stButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
        transition: 0.3s;
        font-size: 18px !important;
    }
    
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 30px;
        border-radius: 15px;
        color: #000000 !important;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-size: 19px;
    }
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

# --- ABAS 1, 2 E 3 (Omitidas aqui para brevidade, mas devem ser mantidas no seu arquivo) ---
# ... (Mantenha o código das outras abas igual ao anterior)

# --- ABA 4: QUIZ PSICOLÓGICO ---
with tab4:
    if 'quiz_iniciado' not in st.session_state:
        st.session_state.quiz_iniciado = False

    if not st.session_state.quiz_iniciado:
        st.markdown("<div style='max-width: 500px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown("### 🧠 Identifique-se")
        nome_user = st.text_input("Qual é o seu nome?")
        genero_user = st.radio("Como você se identifica?", ["Masculino", "Feminino"])
        if st.button("INICIAR JORNADA"):
            if nome_user:
                st.session_state.nome_user = nome_user
                st.session_state.genero_user = genero_user
                st.session_state.quiz_iniciado = True
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        g = st.session_state.genero_user
        art = "o" if g == "Masculino" else "a"
        um = "um" if g == "Masculino" else "uma"
        guerr = "guerreiro" if g == "Masculino" else "guerreira"
        preparado = "preparado" if g == "Masculino" else "preparada"
        reservado = "reservado" if g == "Masculino" else "reservada"

        perguntas = [
            {"p": f"{st.session_state.nome_user}, você caminha pela floresta... você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Você possui uma essência de independência, alguém que encontra força no próprio silêncio.", "Com alguém": "Você valoriza a presença e o suporte, entendendo que a vida ganha sentido no compartilhamento."}},
            {"p": "Você vê um animal na sua frente, qual é esse animal?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Sua mente vê desafios como batalhas, agindo como {um} legítimo {guerr}.", "Coelho": "Sua natureza busca refúgio na calma, preferindo rotas onde a paz seja prioridade.", "Pássaro": "Você detém uma agilidade mental rara, capaz de superar obstáculos com leveza."}},
            {"p": "A sua reação ao ver o animal é:", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "Sua inteligência é movida pela cautela; você sabe que recuar é estratégia.", "Permanecer": f"Você carrega a firmeza de quem não se abala, mantendo-se {preparado}."}},
            {"p": "Você chega em uma estrada. Como ela é:", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você opera sob a lógica da segurança, preferindo saber onde pisa.", "Terra": "Seu espírito vibra no imprevisível; você encontra beleza na incerteza."}},
            {"p": "Você avista uma casa. Ela é:", "o": ["Grande", "Pequena"], "s": {"Grande": f"Suas ambições são vastas; você foi feit{art} para ocupar grandes lugares.", "Pequena": "Sua alma entende que a plenitude reside no essencial e no aconchego."}},
            {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": "Você é seletivo com sua privacidade, protegendo seu valioso interior.", "Não": "Você é uma pessoa aberta ao fluxo da vida e à transparência."}},
            {"p": "A mesa dentro da casa está:", "o": ["Farta", "Vazia"], "s": {"Farta": "Seu momento atual é de preenchimento, com necessidades emocionais supridas.", "Vazia": "Você atravessa uma fase de busca, sentindo que algo ainda falta."}},
            {"p": "Você vê uma xícara no chão. O que faz?", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Você respeita o passado, entendendo que cada fragmento construiu quem você é.", "Ignora": f"Seu foco é o horizonte; você não se permite ser detid{art} por fardos antigos."}},
            {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Sua visão sobre o afeto é refinada, tratando laços como algo precioso.", "Metal": "Sua lealdade é inquebrável; vínculos forjados para resistir a tempestades."}},
            {"p": "Atrás da casa existe um lago, você:", "o": ["Mergulha", "Toca a água", "Contempla a margem"], "s": {"Mergulha": f"Sua entrega é visceral; você mergulha de cabeça nas emoções.", "Toca a água": "Você domina o equilíbrio entre sentir e agir no mundo.", "Contempla a margem": f"Você é {reservado} e prefere entender o terreno antes de se envolver."}}
        ]

        if st.session_state.passo < len(perguntas):
            q = perguntas[st.session_state.passo]
            
            # Pergunta centralizada no meio
            st.markdown(f"<div class='quiz-container'><div class='quiz-pergunta'>{q['p']}</div></div>", unsafe_allow_html=True)
            
            cols = st.columns(len(q['o']))
            for i, opt in enumerate(q['o']):
                if cols[i].button(opt, key=f"q_center_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>🔮 Veredito de {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            st.write(f"Ravengar sussurra: *\"{' '.join(st.session_state.analise)}\"*")
            if st.button("REINICIAR"):
                st.session_state.quiz_iniciado = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
