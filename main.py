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

# --- ABAS 1, 2 e 3 (Mantidas) ---
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
    st.write(f"Energia atual: **{setor}**")
    pergunta_ora = st.text_area("O que as sombras devem revelar?", key="ora_input")
    if st.button("PROFERIR VEREDITO"):
        if chave_api:
            res = consultar_ravengar(f"Você é o Ravengar. Responda sobre {setor}.", pergunta_ora, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 👁️ O Decifrador")
    texto_dec = st.text_area("Insira o enigma ou mensagem:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            res = consultar_ravengar("Você é o Ravengar, decifrador de símbolos.", texto_dec, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 🔥 Teste de Intenção Real")
    nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo_intent")
    comportamento = st.text_area("Comportamento suspeito:", key="comp_input")
    if st.button("DEVASSAR INTENÇÃO"):
        if chave_api and comportamento:
            res_inicial = consultar_ravengar(f"Analise a intenção de {nome_alvo}.", comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]
    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            if msg['role'] == "ravengar":
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"👤 **Você:** {msg['content']}")

# --- ABA 4: QUIZ PSICOLÓGICO (COM ADAPTAÇÃO DE GÊNERO) ---
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
        # Ajustes de gênero automáticos
        art = "o" if g == "Masculino" else "a"
        um = "um" if g == "Masculino" else "uma"
        guerr = "guerreiro" if g == "Masculino" else "guerreira"
        sozinho = "sozinho" if g == "Masculino" else "sozinha"
        acompanhado = "acompanhado" if g == "Masculino" else "acompanhada"
        reservado = "reservado" if g == "Masculino" else "reservada"
        equilibrado = "equilibrado" if g == "Masculino" else "equilibrada"
        focado = "focado" if g == "Masculino" else "focada"

        perguntas = [
            {"p": f"{st.session_state.nome_user}, você caminha pela floresta... você está:", "o": [f"{sozinho.capitalize()}", f"{acompanhado.capitalize()}"], "s": {f"{sozinho.capitalize()}": f"Você carrega uma alma independente, alguém que confia na própria força para cruzar qualquer caminho {sozinho}.", f"{acompanhado.capitalize()}": f"Você valoriza a conexão e sente que a jornada da vida é mais plena quando compartilhada com quem você ama, sentindo-se melhor {acompanhado}."}},
            {"p": "Vê um animal na sua frente:", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Você encara os desafios como {um} {guerr}, vendo neles uma oportunidade de mostrar sua força bruta.", "Coelho": "Você busca a paz e prefere trilhas serenas, evitando o desgaste de conflitos desnecessários.", "Pássaro": "Você possui um espírito livre, capaz de sobrevoar os problemas com leveza e desapego."}},
            {"p": "Sua reação ao ver o animal:", "o": ["Fujo", "Encaro"], "s": {"Fujo": "Diante do desconhecido, seu instinto busca a proteção e a cautela.", "Encaro": f"Você possui a coragem de quem não baixa o olhar para as dificuldades, encarando-as de frente como {um} verdadeiro {guerr}."}},
            {"p": "A estrada que você encontra é de:", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você preza pela segurança e pelo planejamento, gostando de saber exatamente onde pisa.", "Terra": f"Você é atraíd{art} pelo selvagem, pelo incerto e pela liberdade de criar seu próprio rastro."}},
            {"p": "A casa que você vê é:", "o": ["Grande", "Pequena"], "s": {"Grande": "Suas ambições são vastas e você nasceu para ocupar grandes espaços e ser reconhecid{art}.", "Pequena": "Você entende que a verdadeira felicidade mora na simplicidade e no aconchego de um lar calmo."}},
            {"p": "A casa tem cerca?", "o": ["Sim", "Não"], "s": {"Sim": f"Você é uma pessoa {reservado}, que protege seu mundo interior e só deixa entrar quem realmente merece.", "Não": "Você possui um coração aberto e receptivo, permitindo que a vida e as pessoas fluam livremente através de você."}},
            {"p": "A mesa da casa está:", "o": ["Cheia", "Vazia"], "s": {"Cheia": "Neste momento, sua vida transborda conexões e você se sente alimentad{art} pelo afeto ao seu redor.", "Vazia": "Talvez você sinta um vazio que precisa ser preenchido, buscando uma conexão que ainda não encontrou."}},
            {"p": "Vê uma xícara no chão. O que faz?", "o": ["Pego", "Deixo"], "s": {"Pego": f"Você guarda as memórias com carinho e valoriza as raízes que te trouxeram até aqui, sendo {um} amant{art} do passado.", "Deixo": f"Você é alguém do 'agora', focad{art} no futuro e capaz de desapegar do que já passou."}},
            {"p": "A xícara é de:", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Para você, o amor é algo sagrado e delicado, que deve ser cuidado com mãos de seda.", "Metal": "Você vê o amor como uma armadura: algo forte, resistente e feito para durar uma eternidade."}},
            {"p": "No lago final, você:", "o": ["Mergulho", "Molho apenas as mãos", "Sigo direto"], "s": {"Mergulho": f"Você se entrega por inteiro, mergulhando de cabeça nas emoções. É {um} ser de intensidades.", "Molho apenas as mãos": f"Você é {equilibrado} e prudente, mantendo o controle das suas emoções para não se perder.", "Sigo direto": f"Você é {focado} e racional, não permitindo que as águas da emoção te desviem do seu objetivo principal."}}
        ]

        if st.session_state.passo < len(perguntas):
            q = perguntas[st.session_state.passo]
            st.write(f"### {q['p']}")
            cols = st.columns(len(q['o']))
            for i, opt in enumerate(q['o']):
                if cols[i].button(opt, key=f"quiz_opt_{st.session_state.passo}_{i}"):
                    st.session_state.analise.append(q['s'][opt])
                    st.session_state.passo += 1
                    st.rerun()
        else:
            st.markdown("<div class='ravengar-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>🔮 O Veredito para {st.session_state.nome_user}</h2>", unsafe_allow_html=True)
            perfil_texto = " ".join(st.session_state.analise)
            st.write(f"Ravengar sussurra para você: *\"{perfil_texto}\"*")
            
            if st.button("RECOMEÇAR JORNADA"):
                st.session_state.quiz_iniciado = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
