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

    /* Botões das Esferas com Destaque */
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
        font-size: 17px !important;
    }}

    .veredito-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-size: 20px !important;
    }}

    .saudacao-texto {{
        text-align: center;
        font-size: 20px !important;
        color: #555555 !important;
        margin-bottom: 30px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DE CONEXÃO REFINADA ---
def consultar_ravengar(pergunta, api_key, setor="Destino"):
    prompts = {
        "Amor": "Você é o Ravengar, um oráculo místico. No Amor, você fala sobre conexões de alma, feridas emocionais e o fluxo dos afetos. Seja profundo e empático.",
        "Trabalho": "Você é o Ravengar. Na esfera do Trabalho, você é pragmático e estratégico. Fala sobre colheita, poder, autoridade e disciplina.",
        "Futuro": "Você é o Ravengar. No Futuro, você é enigmático e visionário. Foque no destino e em eventos forjados nas sombras.",
        "Saude": "Você é o Ravengar. Na Saúde, você foca no equilíbrio das energias, vitalidade e preservação do templo que é o corpo.",
        "Decifrador": "Você é o Ravengar, o mestre dos símbolos. Sua missão é decifrar sonhos e enigmas revelando significados ocultos.",
        "Intencao": "Você é o Ravengar. Sua visão atravessa máscaras sociais para revelar a real intenção por trás das ações."
    }
    sistema = prompts.get(setor, "Você é o Ravengar, um oráculo místico.")
    sistema += f" O usuário se chama {st.session_state.nome_user} e se identifica no gênero {st.session_state.genero_user}."

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

# --- 4. FLUXO DE ENTRADA ---
if 'usuario_identificado' not in st.session_state:
    st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h3>Bem-vindo à Tenda.</h3><p>Identifique-se para que as sombras saibam quem você é.</p></div>", unsafe_allow_html=True)
    nome_input = st.text_input("Seu nome:")
    genero_input = st.radio("Seu gênero:", ["Masculino", "Feminino"])
    if st.button("ENTRAR NA TENDA"):
        if nome_input:
            st.session_state.nome_user = nome_input
            st.session_state.genero_user = genero_input
            st.session_state.usuario_identificado = True
            st.rerun()
else:
    # --- 5. INTERFACE PRINCIPAL ---
    st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    saudacao = "Seja muito bem-vindo" if st.session_state.genero_user == "Masculino" else "Seja muito bem-vinda"
    st.markdown(f"<p class='saudacao-texto'>{saudacao}, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção", "🧠 Quiz Psicológico"])

    with tab1:
        st.markdown("### Escolha sua Esfera")
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
        pergunta_ora = st.text_area(f"O que deseja saber sobre o seu {setor}?", key="ora_input")
        if st.button("PROFERIR VEREDITO", key="btn_main_ora"):
            if chave_api and pergunta_ora:
                res = consultar_ravengar(pergunta_ora, chave_api, setor)
                st.session_state['chat_ora'] = [{"role": "ravengar", "content": res}]

        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                st.markdown(f"<div class='ravengar-card' style='margin-bottom:10px;'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            with st.form(key="form_ora", clear_on_submit=True):
                resp = st.text_input("Continue sua dúvida:")
                if st.form_submit_button("ENVIAR") and resp:
                    st.session_state['chat_ora'].append({"role": "user", "content": resp})
                    res = consultar_ravengar(f"Contexto: {resp}", chave_api, setor)
                    st.session_state['chat_ora'].append({"role": "ravengar", "content": res})
                    st.rerun()

    with tab2:
        st.markdown("### 👁️ O Decifrador")
        texto_dec = st.text_area("Descreva o mistério:", key="dec_input")
        if st.button("DECIFRAR AGORA"):
            if chave_api and texto_dec:
                res = consultar_ravengar(texto_dec, chave_api, "Decifrador")
                st.session_state['chat_dec'] = [{"role": "ravengar", "content": res}]
        if 'chat_dec' in st.session_state:
            for msg in st.session_state['chat_dec']:
                st.markdown(f"<div class='ravengar-card' style='margin-bottom:10px;'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            with st.form(key="form_dec", clear_on_submit=True):
                resp = st.text_input("Pergunte mais:")
                if st.form_submit_button("ENVIAR") and resp:
                    st.session_state['chat_dec'].append({"role": "user", "content": resp})
                    res = consultar_ravengar(f"Siga decifrando: {resp}", chave_api, "Decifrador")
                    st.session_state['chat_dec'].append({"role": "ravengar", "content": res})
                    st.rerun()

    with tab3:
        st.markdown("### 🔥 Teste de Intenção Real")
        nome_alvo = st.text_input("Pessoa alvo:", key="nome_alvo_int")
        comportamento = st.text_area("Comportamento suspeito:", key="comp_input")
        if st.button("DESVENDAR INTENÇÃO"):
            if chave_api and comportamento:
                res = consultar_ravengar(f"Analise {nome_alvo}: {comportamento}", chave_api, "Intencao")
                st.session_state['historico'] = [{"role": "ravengar", "content": res}]
        if 'historico' in st.session_state:
            for msg in st.session_state['historico']:
                st.markdown(f"<div class='ravengar-card' style='margin-bottom:10px;'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            with st.form(key="chat_int", clear_on_submit=True):
                resp_usuario = st.text_input("Fale com o Ravengar:")
                if st.form_submit_button("ENVIAR"):
                    st.session_state['historico'].append({"role": "user", "content": resp_usuario})
                    res = consultar_ravengar(f"Diálogo sobre intenção: {resp_usuario}", chave_api, "Intencao")
                    st.session_state['historico'].append({"role": "ravengar", "content": res})
                    st.rerun()

    with tab4:
        if 'passo' not in st.session_state:
            st.session_state.passo, st.session_state.analise = 0, []

        g = st.session_state.genero_user
        art, um, guerr, prep, reser, leg = ("o", "um", "guerreiro", "preparado", "reservado", "legítimo") if g == "Masculino" else ("a", "uma", "guerreira", "preparada", "reservada", "legítima")
        
        perguntas = [
            {"p": f"{st.session_state.nome_user}, você caminha pela floresta... você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Você possui uma essência de independência, alguém que encontra força no próprio silêncio.", "Com alguém": "Você valoriza a presença das pessoas, entendendo que a vida ganha sentido através do compartilhamento."}},
            {"p": "Você vê um animal na sua frente, qual é?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Sua mente vê desafios como batalhas a serem vencidas, agindo como {um} {leg} {guerr}.", "Coelho": "Sua natureza busca refúgio na calma e na diplomacia.", "Pássaro": "Você detém uma agilidade mental rara, capaz de superar obstáculos com leveza."}},
            {"p": "A sua reação ao ver o animal é:", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "Sua inteligência é movida pela cautela estratégica.", "Permanecer": "Você não teme o desconhecido."}},
            {"p": "Você chega em uma estrada. Como ela é:", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você opera com planejamento e ordem.", "Terra": "Seu espírito vibra no imprevisível e na liberdade."}},
            {"p": "Você avista uma casa. Ela é:", "o": ["Grande", "Pequena"], "s": {"Grande": "Suas ambições são vastas e seu potencial de conquista é imenso.", "Pequena": "Sua alma entende que a verdadeira plenitude reside no essencial."}},
            {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": f"Você é {reser}, mantendo um escudo necessário para proteger o seu interior.", "Não": "Você é uma pessoa aberta às trocas e acredita na transparência."}},
            {"p": "A mesa dentro da casa está:", "o": ["Farta", "Vazia"], "s": {"Farta": "Seu momento atual é de preenchimento e conexão emocional.", "Vazia": "Você atravessa uma fase de busca e introspecção profunda."}},
            {"p": "Você vê uma xícara no chão. O que faz?", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Você é uma pessoa saudosista e valoriza o que moldou seu passado.", "Ignora": "Seu foco é o horizonte à frente, sem carregar fardos antigos."}},
            {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Sua visão sobre o afeto é refinada e preciosa.", "Metal": "Sua lealdade é inquebrável, forjada para resistir a tempestades."}},
            {"p": "Atrás da casa existe um lago, você:", "o": ["Mergulha", "Toca a água", "Contempla"], "s": {"Mergulha": "Sua entrega é visceral e intensa.", "Toca a água": "Você domina o equilíbrio entre sentir e agir.", "Contempla": f"Sua essência é de um observador {reser} que protege sua energia."}}
        ]

        if st.session_state.passo < len(perguntas):
            q = perguntas[st.session_state.passo]
            st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
            cols = st.columns(len(q['o']))
            for i, opt in enumerate(q['o']):
                if cols[i].button(opt, key=f"q_final_rev_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='veredito-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>O Veredito para {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            st.write(" ".join(st.session_state.analise))
            if st.button("REINICIAR JORNADA"):
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
