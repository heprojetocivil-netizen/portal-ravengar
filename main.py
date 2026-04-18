import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    .stApp p, .stApp span, .stApp label, h1, h2, h3 { color: #000000 !important; }
    div.stButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        transition: 0.3s;
    }
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        color: #000000 !important;
        margin-bottom: 20px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
        line-height: 1.6;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CONEXÃO ---
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

with st.sidebar:
    st.markdown("### 🍷 Conexão")
    chave_api = st.text_input("Chave Groq API", type="password")

st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção", "🧠 Quiz Psicológico"])

# --- ABA 4: QUIZ PSICOLÓGICO (SEQUÊNCIA LOGICA) ---
with tab4:
    if 'quiz_iniciado' not in st.session_state:
        st.session_state.quiz_iniciado = False

    if not st.session_state.quiz_iniciado:
        st.markdown("### 🧠 Identifique-se para o Ravengar")
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
            else:
                st.error("Diga seu nome para as sombras.")
    else:
        g = st.session_state.genero_user
        art = "o" if g == "Masculino" else "a"
        um = "um" if g == "Masculino" else "uma"
        guerr = "guerreiro" if g == "Masculino" else "guerreira"
        preparado = "preparado" if g == "Masculino" else "preparada"

        # SEQUÊNCIA LOGICA DAS PERGUNTAS
        perguntas = [
            {
                "p": f"{st.session_state.nome_user}, você caminha pela floresta... você está:",
                "o": ["Só", "Com alguém"],
                "s": {"Só": "Você possui uma essência de independência, alguém que encontra força no próprio silêncio para cruzar qualquer destino.", 
                      "Com alguém": "Você valoriza a presença e o suporte, entendendo que a vida ganha mais sentido através do compartilhamento."}
            },
            {
                "p": "Você vê um animal na sua frente:",
                "o": ["Lobo", "Coelho", "Pássaro"],
                "s": {"Lobo": f"Sua mente vê desafios como batalhas a serem vencidas, agindo com a postura de quem domina o espaço como {um} legítimo {guerr}.", 
                      "Coelho": "Sua natureza busca refúgio na calma e na diplomacia, preferindo rotas onde a paz seja a prioridade.", 
                      "Pássaro": "Você detém uma agilidade mental rara, capaz de superar obstáculos com uma leveza que os outros não compreendem."}
            },
            {
                "p": "A sua reação ao ver o animal é:",
                "o": ["Recuar", "Permanecer"],
                "s": {"Recuar": "Sua inteligência é movida pela cautela estratégica; você sabe que recuar muitas vezes é o segredo da sobrevivência.", 
                      "Permanecer": f"Você carrega a firmeza de quem não se deixa abalar, mantendo-se {preparado} para encarar o desconhecido."}
            },
            {
                "p": "Você chega em uma estrada. Como ela é:",
                "o": ["Asfalto", "Terra"],
                "s": {"Asfalto": "Você opera sob a lógica da segurança e do planejamento, preferindo saber exatamente para onde o caminho leva.", 
                      "Terra": "Seu espírito vibra no imprevisível; você encontra beleza na incerteza e na liberdade de criar seu próprio rastro."}
            },
            {
                "p": "Você segue caminhando e avista uma casa. Ela é:",
                "o": ["Grande", "Pequena"],
                "s": {"Grande": f"Suas ambições são vastas e seu potencial de conquista é imenso; você foi feit{art} para ocupar grandes lugares.", 
                      "Pequena": "Sua alma entende que a verdadeira plenitude reside no essencial e na tranquilidade de um refúgio acolhedor."}
            },
            {
                "p": "A casa tem cerca?",
                "o": ["Sim", "Não"],
                "s": {"Sim": "Você é seletivo com sua privacidade, mantendo um escudo necessário para proteger o que há de mais valioso em seu interior.", 
                      "Não": "Você é uma pessoa aberta às trocas e ao fluxo da vida, acreditando na transparência como forma de conexão."}
            },
            {
                "p": "Você entra na casa e avista uma mesa. Ela está:",
                "o": ["Farta", "Vazia"],
                "s": {"Farta": "Seu momento atual é de preenchimento e conexão, sentindo que suas necessidades emocionais estão sendo supridas.", 
                      "Vazia": "Você atravessa uma fase de busca e introspecção, talvez sentindo que ainda falta algo para completar seu cenário atual."}
            },
            {
                "p": "Você vê uma xícara no chão. O que faz?",
                "o": ["Recolhe", "Ignora"],
                "s": {"Recolhe": "Você respeita o passado e os legados, entendendo que cada fragmento do que passou ajuda a construir quem você é.", 
                      "Ignora": f"Seu foco é o horizonte à frente; você não se permite ser detid{art} por fardos que já não fazem parte do seu agora."}
            },
            {
                "p": "A xícara é de:",
                "o": ["Porcelana", "Metal"],
                "s": {"Porcelana": "Sua visão sobre o afeto é refinada e cuidadosa, tratando os laços como algo precioso que não pode ser negligenciado.", 
                      "Metal": "Para você, a lealdade é inquebrável; seus vínculos são forjados para resistir a qualquer tempestade."}
            },
            {
                "p": "Atrás da casa existe um lago, você:",
                "o": ["Mergulha", "Toca a água", "Apenas olha"],
                "s": {"Mergulha": f"Sua entrega é visceral; você mergulha de cabeça nas emoções e vive as experiências com máxima intensidade.", 
                      "Toca a água": "Você domina o equilíbrio entre sentir e agir, mantendo o controle emocional enquanto experimenta o mundo.", 
                      "Apenas olha": "Sua racionalidade é seu guia; você prefere observar e analisar o cenário antes de se envolver emocionalmente."}
            }
        ]

        if st.session_state.passo < len(perguntas):
            q = perguntas[st.session_state.passo]
            st.write(f"### {q['p']}")
            cols = st.columns(len(q['o']))
            for i, opt in enumerate(q['o']):
                if cols[i].button(opt, key=f"q_seq_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>🔮 O Veredito para {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            perfil_texto = " ".join(st.session_state.analise)
            st.write(f"Ravengar sussurra: *\"{perfil_texto}\"*")
            
            if st.button("REINICIAR JORNADA"):
                st.session_state.quiz_iniciado = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
