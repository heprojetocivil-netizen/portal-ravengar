import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }

    .quiz-pergunta {
        font-size: 28px !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-bottom: 35px !important;
        line-height: 1.4;
    }
    
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #FFD1DC !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #FFB7C5 !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
        font-size: 18px !important;
    }
    
    .ravengar-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        line-height: 1.6;
        font-size: 17px !important;
    }

    .veredito-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-size: 22px !important;
        font-weight: 500 !important;
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

# ... (Abas 1 e 2)
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
    pergunta_ora = st.text_area("O que as sombras devem revelar?", key="ora_input")
    if st.button("PROFERIR VEREDITO"):
        if chave_api:
            res = consultar_ravengar(f"Você é o Ravengar. Responda sobre {setor}.", pergunta_ora, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 👁️ O Decifrador")
    texto_dec = st.text_area("Insira o enigma, sonho ou mensagem:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            res = consultar_ravengar("Você é o Ravengar, decifrador de símbolos.", texto_dec, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔥 Teste de Intenção Real")
    col_a, col_b = st.columns(2)
    with col_a: nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo_int")
    with col_b: genero_int = st.radio("Essa pessoa é:", ["Homem", "Mulher"], key="gen_int")
    comportamento = st.text_area("Descreva o comportamento suspeito:", key="comp_input")
    if st.button("DEVASSAR INTENÇÃO"):
        if chave_api and comportamento:
            prompt_init = f"Você é o Ravengar. Analise as intenções de {nome_alvo}. Termine com uma pergunta provocativa."
            res_inicial = consultar_ravengar(prompt_init, comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]
    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            div_class = "ravengar-card" if msg['role'] == "ravengar" else ""
            prefixo = "🔮 **Ravengar:**" if msg['role'] == "ravengar" else "👤 **Você:**"
            st.markdown(f"<div class='{div_class}'>{prefixo}<br>{msg['content']}</div>", unsafe_allow_html=True)
        with st.form(key="chat_intencao_rev", clear_on_submit=True):
            resp_usuario = st.text_input("Sua resposta para o Ravengar:")
            if st.form_submit_button("ENVIAR RESPOSTA") and resp_usuario:
                st.session_state['historico'].append({"role": "user", "content": resp_usuario})
                hist_texto = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state['historico']])
                nova_res = consultar_ravengar(f"Ravengar, histórico: {hist_texto}", "Continue o diálogo de forma mística.", chave_api)
                st.session_state['historico'].append({"role": "ravengar", "content": nova_res})
                st.rerun()

# --- ABA 4: QUIZ PSICOLÓGICO (REVISADO) ---
with tab4:
    if 'quiz_iniciado' not in st.session_state:
        st.session_state.quiz_iniciado = False

    if not st.session_state.quiz_iniciado:
        st.markdown("### 🧠 Identifique-se")
        nome_user = st.text_input("Qual é o seu nome?")
        genero_user = st.radio("Como você se identifica?", ["Masculino", "Feminino"])
        if st.button("INICIAR JORNADA"):
            if nome_user:
                st.session_state.nome_user, st.session_state.genero_user = nome_user, genero_user
                st.session_state.quiz_iniciado, st.session_state.passo, st.session_state.analise = True, 0, []
                st.rerun()
    else:
        g = st.session_state.genero_user
        art, um, guerr, prep, reser, leg = ("o", "um", "guerreiro", "preparado", "reservado", "legítimo") if g == "Masculino" else ("a", "uma", "guerreira", "preparada", "reservada", "legítima")
        
        perguntas = [
            {"p": f"{st.session_state.nome_user}, você caminha pela floresta... você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Você possui uma essência de independência, alguém que encontra força no próprio silêncio para cruzar qualquer destino.", "Com alguém": "Você valoriza a presença das pessoas, entendendo que a vida ganha mais sentido através do compartilhamento."}},
            {"p": "Você vê um animal na sua frente, qual é esse animal?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Sua mente vê desafios como batalhas a serem vencidas, agindo com a postura de quem domina o espaço como {um} {leg} {guerr}.", "Coelho": "Sua natureza busca refúgio na calma e na diplomacia, preferindo rotas onde a paz seja a prioridade.", "Pássaro": "Você detém uma agilidade mental rara, capaz de superar obstáculos com uma leveza que os outros não compreendem."}},
            {"p": "A sua reação ao ver o animal é:", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "Sua inteligência é movida pela cautela estratégica; você sabe que recuar muitas vezes é o segredo da sobrevivência.", "Permanecer": "Você não teme o desconhecido."}},
            {"p": "Você chega em uma estrada. Como ela é:", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você opera com planejamento, preferindo saber exatamente para onde o caminho leva.", "Terra": "Seu espírito vibra no imprevisível; você encontra beleza na incerteza e na liberdade de criar seu próprio rastro."}},
            {"p": "Você avista uma casa. Ela é:", "o": ["Grande", "Pequena"], "s": {"Grande": f"Suas ambições são vastas e seu potencial de conquista é imenso; você tem grandes aspirações.", "Pequena": "Sua alma entende que a verdadeira plenitude reside no essencial e na tranquilidade de um refúgio acolhedor."}},
            {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": "Você é reservado, mantendo um escudo necessário para proteger o que há de mais valioso em seu interior.", "Não": "Você é uma pessoa aberta às trocas e ao fluxo da vida, acreditando na transparência como forma de conexão."}},
            {"p": "A mesa dentro da casa está:", "o": ["Farta", "Vazia"], "s": {"Farta": "Seu momento atual é de preenchimento e conexão, sentindo que suas necessidades emocionais estão sendo supridas.", "Vazia": "Você atravessa uma fase de busca e introspecção, talvez sentindo que ainda falta algo para completar seu cenário atual."}},
            {"p": "Você vê uma xícara no chão. O que faz?", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Você é uma pessoa saudosista, e entende que cada fragmento do passado ajudou a moldar quem você é hoje.", "Ignora": f"Seu foco é o horizonte à frente; você não se permite ser detid{art} por fardos que já não fazem parte do seu agora."}},
            {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Sua visão sobre o afeto é refinada e cuidadosa, tratando os laços como algo precioso que não pode ser negligenciado.", "Metal": "Para você, a lealdade é inquebrável; seus vínculos são forjados para resistir a qualquer tempestade."}},
            {"p": "Atrás da casa existe um lago, você:", "o": ["Mergulha", "Toca a água", "Contempla a margem"], "s": {"Mergulha": f"Sua entrega é visceral; você mergulha de cabeça nas emoções e vive as experiências com máxima intensidade.", "Toca a água": "Você domina o equilíbrio entre sentir e agir, mantendo o controle emocional enquanto desbrava o mundo.", "Contempla a margem": f"Sua essência é de um observador silencioso; você é {reser} e prefere entender o terreno e proteger sua energia antes de se envolver."}}
        ]

        if st.session_state.passo < len(perguntas):
            q = perguntas[st.session_state.passo]
            st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
            cols = st.columns(len(q['o']))
            for i, opt in enumerate(q['o']):
                if cols[i].button(opt, key=f"q_fin_rev_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='veredito-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; margin-bottom:20px;'>O Veredito para {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            st.write(" ".join(st.session_state.analise))
            if st.button("REINICIAR JORNADA"):
                st.session_state.quiz_iniciado = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
