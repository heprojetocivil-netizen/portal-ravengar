import streamlit as st
from groq import Groq

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

# Lógica de CSS Dinâmico para destacar a esfera selecionada
setor_ativo = st.session_state.get('setor', '')

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}

    /* Estilo padrão dos botões de esfera */
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

    /* Destaque para a esfera selecionada */
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
        font-size: 22px !important;
    }}

    .saudacao-texto {{
        text-align: center;
        font-size: 20px !important;
        color: #555555 !important;
        margin-bottom: 30px !important;
    }}
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
            st.error("O Oráculo precisa de um nome para abrir os portões.")

# --- 5. INTERFACE PRINCIPAL ---
else:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    saudacao = "Seja muito bem-vindo" if st.session_state.genero_user == "Masculino" else "Seja muito bem-vinda"
    st.markdown(f"<p class='saudacao-texto'>{saudacao}, <b>{st.session_state.nome_user}</b>.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção", "🧠 Quiz Psicológico"])

    # --- ABA 1: ORÁCULO COM BOTÕES PERSISTENTES ---
    with tab1:
        st.markdown("### Escolha sua Esfera")
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR", key="btn_Amor"): 
                st.session_state.setor = "Amor"
                st.rerun()
        with c2: 
            if st.button("💼 TRABALHO", key="btn_Trabalho"): 
                st.session_state.setor = "Trabalho"
                st.rerun()
        with c3: 
            if st.button("✨ FUTURO", key="btn_Futuro"): 
                st.session_state.setor = "Futuro"
                st.rerun()
        with c4: 
            if st.button("🌿 SAÚDE", key="btn_Saude"): 
                st.session_state.setor = "Saude"
                st.rerun()
        
        setor = st.session_state.get('setor', 'Destino')
        st.info(f"Esfera ativa: **{setor.upper()}**")
        
        pergunta_ora = st.text_area(f"O que deseja saber sobre o seu {setor}?", key="ora_input")
        
        if st.button("PROFERIR VEREDITO", key="btn_main_ora"):
            if chave_api and pergunta_ora:
                res = consultar_ravengar(f"Você é o Ravengar. Responda a {st.session_state.nome_user} sobre {setor}.", pergunta_ora, chave_api)
                st.session_state['chat_ora'] = [{"role": "ravengar", "content": res}]

        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                div_class = "ravengar-card" if msg['role'] == "ravengar" else ""
                st.markdown(f"<div class='{div_class}'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            
            with st.form(key="form_ora", clear_on_submit=True):
                resp = st.text_input("Continue o diálogo:")
                if st.form_submit_button("ENVIAR") and resp:
                    st.session_state['chat_ora'].append({"role": "user", "content": resp})
                    res = consultar_ravengar(f"Ravengar, em diálogo com {st.session_state.nome_user} sobre {setor}: {resp}", "Responda de forma mística.", chave_api)
                    st.session_state['chat_ora'].append({"role": "ravengar", "content": res})
                    st.rerun()

    # --- ABA 2: DECIFRADOR ---
    with tab2:
        st.markdown("### 👁️ O Decifrador")
        texto_dec = st.text_area("Descreva o sonho ou sinal para decifrar:", key="dec_input")
        if st.button("DECIFRAR MISTÉRIO", key="btn_dec"):
            if chave_api and texto_dec:
                res = consultar_ravengar(f"Você é o Ravengar decifrador. Falando com {st.session_state.nome_user}.", texto_dec, chave_api)
                st.session_state['chat_dec'] = [{"role": "ravengar", "content": res}]

        if 'chat_dec' in st.session_state:
            for msg in st.session_state['chat_dec']:
                div_class = "ravengar-card" if msg['role'] == "ravengar" else ""
                st.markdown(f"<div class='{div_class}'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            
            with st.form(key="form_dec", clear_on_submit=True):
                resp = st.text_input("Busque mais profundidade:")
                if st.form_submit_button("ENVIAR") and resp:
                    st.session_state['chat_dec'].append({"role": "user", "content": resp})
                    res = consultar_ravengar(f"Ravengar decifrando para {st.session_state.nome_user}: {resp}", "Continue a explicação.", chave_api)
                    st.session_state['chat_dec'].append({"role": "ravengar", "content": res})
                    st.rerun()

    # --- ABA 3: TESTE DE INTENÇÃO ---
    with tab3:
        st.markdown("### 🔥 Teste de Intenção Real")
        col_a, col_b = st.columns(2)
        with col_a: nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo_int")
        with col_b: genero_int = st.radio("Essa pessoa é:", ["Homem", "Mulher"], key="gen_int")
        comportamento = st.text_area("Descreva o comportamento suspeito:", key="comp_input")
        
        if st.button("DESVENDAR INTENÇÃO"):
            if chave_api and comportamento:
                prompt_init = f"Você é o Ravengar. Analise as intenções de {nome_alvo} para {st.session_state.nome_user}."
                res_inicial = consultar_ravengar(prompt_init, comportamento, chave_api)
                st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]
        
        if 'historico' in st.session_state:
            for msg in st.session_state['historico']:
                div_class = "ravengar-card" if msg['role'] == "ravengar" else ""
                st.markdown(f"<div class='{div_class}'>{'🔮 **Ravengar:**' if msg['role'] == 'ravengar' else '👤 **Você:**'}<br>{msg['content']}</div>", unsafe_allow_html=True)
            with st.form(key="chat_intencao_rev", clear_on_submit=True):
                resp_usuario = st.text_input("Sua resposta ao Ravengar:")
                if st.form_submit_button("ENVIAR") and resp_usuario:
                    st.session_state['historico'].append({"role": "user", "content": resp_usuario})
                    nova_res = consultar_ravengar(f"Ravengar, conversando com {st.session_state.nome_user}: {resp_usuario}", "Continue a análise.", chave_api)
                    st.session_state['historico'].append({"role": "ravengar", "content": nova_res})
                    st.rerun()

    # --- ABA 4: QUIZ PSICOLÓGICO ---
    with tab4:
        if 'passo' not in st.session_state:
            st.session_state.passo = 0
            st.session_state.analise = []

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
                if cols[i].button(opt, key=f"q_final_rev_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='veredito-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; margin-bottom:20px;'>O Veredito para {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            st.write(" ".join(st.session_state.analise))
            if st.button("REINICIAR JORNADA"):
                st.session_state.passo = 0
                st.session_state.analise = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
