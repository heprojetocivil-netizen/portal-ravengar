import streamlit as st
from groq import Groq
import random
from datetime import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F7F7F7 !important; }
    .stApp p, .stApp span, .stApp label, h1, h2, h3 { color: #000000 !important; }

    div.stButton > button, div.stFormSubmitButton > button {
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
    }

    .tarot-card {
        background: linear-gradient(135deg, #2D0036, #6B006B);
        border: 3px solid #FFD1DC;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px auto;
        max-width: 420px;
        box-shadow: 0 8px 32px rgba(180,0,180,0.25);
    }
    .tarot-card * { color: #FFD1DC !important; }
    .tarot-titulo { font-size: 1.6em; font-weight: bold; margin-bottom: 6px; }
    .tarot-simbolo { font-size: 3.5em; margin: 10px 0; }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab-active"] { border-bottom: 3px solid #FFD1DC !important; }

    .rodape-ravengar {
        text-align: center;
        padding: 24px 0 8px 0;
        font-size: 0.88em;
        color: #888 !important;
        border-top: 1px solid #FFD1DC;
        margin-top: 40px;
    }

    .boas-vindas-box {
        background: linear-gradient(135deg, #1a001a, #2D0036);
        border: 2px solid #FFD1DC;
        border-radius: 16px;
        padding: 22px 28px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 24px rgba(180,0,180,0.2);
    }
    .boas-vindas-box * { color: #FFD1DC !important; }
    .boas-vindas-hora { font-size: 0.82em; opacity: 0.65; margin-bottom: 8px; letter-spacing: 1px; }
    .boas-vindas-frase { font-size: 1.05em; font-style: italic; line-height: 1.7; }

    .runa-card {
        background: linear-gradient(135deg, #0D0D1A, #1A0026);
        border: 2px solid #9B59B6;
        border-radius: 16px;
        padding: 26px;
        text-align: center;
        margin: 16px auto;
        max-width: 380px;
        box-shadow: 0 6px 28px rgba(155,89,182,0.3);
    }
    .runa-card * { color: #DDA0DD !important; }
    .runa-simbolo { font-size: 4em; margin: 8px 0; }
    .runa-nome { font-size: 1.4em; font-weight: bold; }

    .astral-box {
        background: linear-gradient(135deg, #0A0A1F, #0D001A);
        border: 2px solid #6666FF;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
    }
    .astral-box * { color: #CCCCFF !important; }

    .numero-box {
        background: linear-gradient(135deg, #1A0A00, #2D1500);
        border: 2px solid #FFD700;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    .numero-box * { color: #FFD700 !important; }
    .numero-grande { font-size: 3.5em; font-weight: bold; }
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

# --- 3. TELA DE ENTRADA ---
if 'chave_api' not in st.session_state or not st.session_state.chave_api:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#888;'>Mistérios da Mente e do Destino</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#FFF0F5;border:1px solid #FFB7C5;border-radius:12px;
        padding:14px 18px;margin-bottom:20px;font-size:0.9em;color:#000;line-height:1.8;text-align:center;'>
        🔒 <strong>Exclusivo para Associados Quiz Com Prêmios</strong><br>
        🔗 <a href='https://quizcompremios.com.br/' target='_blank'
        style='color:#C2185B;font-weight:600;text-decoration:none;'>quizcompremios.com.br</a>
        </div>
        """, unsafe_allow_html=True)
        chave_digitada = st.text_input("🔑 Digite sua Chave Groq API para entrar:", type="password", key="input_chave_entrada")
        if st.button("✨ ENTRAR NA TENDA"):
            if chave_digitada.strip():
                st.session_state.chave_api = chave_digitada.strip()
                st.session_state['hora_entrada'] = datetime.now()
                st.rerun()
            else:
                st.error("Por favor, insira sua chave API antes de entrar.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:0.8em;color:#aaa;'>Não tem uma chave? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#C2185B;'>console.groq.com/keys</a></p>", unsafe_allow_html=True)
    st.stop()

# Chave disponível para todo o app
chave_api = st.session_state.chave_api

# --- 4. INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)

# Botão de sair
col_sair1, col_sair2 = st.columns([5, 1])
with col_sair2:
    if st.button("🚪 Sair", key="btn_sair"):
        del st.session_state['chave_api']
        st.rerun()

# --- MENSAGEM SOMBRIA DE BOAS-VINDAS ---
hora_entrada = st.session_state.get('hora_entrada', datetime.now())
dias_semana = ["segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado","domingo"]
dia_semana = dias_semana[hora_entrada.weekday()]
hora_fmt = hora_entrada.strftime("%Hh%M")

FRASES_RAVENGAR = [
    "As sombras sussurraram seu nome antes mesmo de você tocar a porta. Seja bem-vindo.",
    "Você não encontrou esta tenda por acaso. Nada aqui é acidente.",
    "Os espíritos já me avisaram que você viria. Estávamos esperando.",
    "Algo dentro de você sabia que precisava estar aqui. Esse algo tem razão.",
    "O véu entre os mundos é fino neste momento. Você chegou na hora certa.",
    "Não foi você que me escolheu. Foi o destino que te trouxe até mim.",
    "Há algo que você ainda não sabe sobre si mesmo. É para isso que você está aqui.",
    "Os astros registraram sua chegada. O que será revelado não pode ser desvelado.",
]
if 'frase_boas_vindas' not in st.session_state:
    st.session_state['frase_boas_vindas'] = random.choice(FRASES_RAVENGAR)

frase = st.session_state['frase_boas_vindas']
st.markdown(f"""
<div class='boas-vindas-box'>
    <div class='boas-vindas-hora'>🕯️ Você chegou às {hora_fmt} de uma {dia_semana}. Os espíritos já te aguardavam. 🕯️</div>
    <div class='boas-vindas-frase'>"{frase}"<br><br>— <strong>Ravengar</strong></div>
</div>
""", unsafe_allow_html=True)

# --- SOM AMBIENTE ---
with st.expander("🎵 Som Ambiente Místico (ativar/desativar)"):
    st.markdown("""
    <audio autoplay loop controls style="width:100%;margin-top:8px;">
      <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3" type="audio/mpeg">
    </audio>
    <p style="font-size:0.78em;color:#aaa;margin-top:6px;">🔇 Clique em pause para silenciar</p>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ABAS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
    "🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção",
    "🧠 Quiz Psicológico", "🌀 Vidas Passadas", "🃏 Carta do Tarot",
    "⭐ Mapa Astral", "💞 Compatibilidade", "🔢 Numerologia",
    "🖤 Espelho Negro", "🌙 Ritual de Intenção", "ᚠ Oráculo das Runas"
])

# --- ABA 1: ORÁCULO ---
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

# --- ABA 2: DECIFRADOR ---
with tab2:
    st.markdown("### 👁️ O Decifrador")
    texto_dec = st.text_area("Insira o enigma, sonho ou mensagem:", key="dec_input")
    if st.button("DECIFRAR MISTÉRIO"):
        if chave_api:
            res = consultar_ravengar("Você é o Ravengar, decifrador de símbolos.", texto_dec, chave_api)
            st.markdown(f"<div class='ravengar-card'>{res}</div>", unsafe_allow_html=True)

# --- ABA 3: TESTE DE INTENÇÃO ---
with tab3:
    st.markdown("### 🔥 Teste de Intenção Real")
    col_a, col_b = st.columns(2)
    with col_a: nome_alvo = st.text_input("Nome da pessoa:", key="nome_alvo")
    with col_b: genero = st.radio("Essa pessoa é:", ["Homem", "Mulher"])
    comportamento = st.text_area("Descreva o comportamento suspeito:", key="comp_input")
    if st.button("DEVASSAR INTENÇÃO"):
        if not chave_api or not comportamento:
            st.error("Preencha a chave e o comportamento.")
        else:
            prompt_init = f"Você é o Ravengar. Analise as intenções de {nome_alvo}. Termine com uma pergunta provocativa."
            res_inicial = consultar_ravengar(prompt_init, comportamento, chave_api)
            st.session_state['historico'] = [{"role": "ravengar", "content": res_inicial}]
    if 'historico' in st.session_state:
        for msg in st.session_state['historico']:
            if msg['role'] == "ravengar":
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"👤 **Você:** {msg['content']}")
        with st.form(key="form_conversa", clear_on_submit=True):
            resp_usuario = st.text_input("Sua resposta para o Ravengar:")
            c1, c2 = st.columns(2)
            if c1.form_submit_button("ENVIAR RESPOSTA") and resp_usuario:
                st.session_state['historico'].append({"role": "user", "content": resp_usuario})
                hist_full = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state['historico']])
                nova_res = consultar_ravengar(f"Ravengar, histórico: {hist_full}", "Continue o diálogo.", chave_api)
                st.session_state['historico'].append({"role": "ravengar", "content": nova_res})
                st.rerun()
            if c2.form_submit_button("🔄 RESETAR"):
                del st.session_state['historico']
                st.rerun()

# --- ABA 4: QUIZ PSICOLÓGICO ---
with tab4:
    st.markdown("### 🧠 Jornada pela Floresta")
    st.markdown("*Responda com calma, deixando a primeira imagem que vier à mente guiar você.*")

    perguntas_floresta = [
        {"p": "Imagine que você está caminhando em uma floresta. Você está:", "o": ["Sozinho", "Acompanhado"],
         "s": {"Sozinho": "Possui uma forte tendência à independência emocional. Consegue se bastar e encontrar seus próprios caminhos.", "Acompanhado": "Valoriza profundamente a conexão humana. Encontra força e segurança nas relações que constrói."}},
        {"p": "De repente, um animal aparece bem à sua frente no caminho. Qual é esse animal?", "o": ["Um lobo", "Um coelho", "Um pássaro"],
         "s": {"Um lobo": "Enxerga os desafios da vida como provações que exigem força e coragem. Não recua facilmente diante do que intimida.", "Um coelho": "Tem uma sensibilidade apurada e prefere a paz ao conflito. Evita situações de tensão e busca ambientes harmoniosos.", "Um pássaro": "Lida com a vida com uma leveza admirável. Tem a capacidade de ver as situações de um ponto de vista mais elevado."}},
        {"p": "Ao se deparar com esse animal, o que você faz instintivamente?", "o": ["Recuo e me afasto", "Fico parado e encaro"],
         "s": {"Recuo e me afasto": "Diante do desconhecido ou do desconforto, sua primeira reação é se proteger. Prefere analisar antes de agir.", "Fico parado e encaro": "Tem uma postura corajosa diante dos problemas. Não foge das situações difíceis — prefere encará-las de frente."}},
        {"p": "Você segue em frente e encontra uma estrada. Como ela é?", "o": ["Pavimentada e bem definida", "De terra, sem sinalização"],
         "s": {"Pavimentada e bem definida": "Valoriza a segurança, o planejamento e a previsibilidade. Sente-se mais confortável quando sabe para onde está indo.", "De terra, sem sinalização": "Tem uma veia aventureira e aprecia o imprevisível. A liberdade de descobrir o caminho por conta própria é algo que te move."}},
        {"p": "No final da estrada, você avista uma casa. Como ela é?", "o": ["Grande e imponente", "Pequena e aconchegante"],
         "s": {"Grande e imponente": "Carrega dentro de si uma ambição considerável e um desejo genuíno de crescer, expandir e conquistar.", "Pequena e aconchegante": "Preza pelo simples e pelo essencial. Encontra plenitude nas coisas menores, nos momentos íntimos e tranquilos."}},
        {"p": "Ao chegar mais perto, você percebe que essa casa tem ou não tem cerca?", "o": ["Tem cerca ao redor", "Não tem cerca"],
         "s": {"Tem cerca ao redor": "É uma pessoa que preserva seu espaço pessoal com cuidado. Tem limites bem definidos e não os abre para qualquer um.", "Não tem cerca": "É naturalmente aberto e receptivo. Tem facilidade em receber pessoas e raramente se fecha para o mundo."}},
        {"p": "Você entra na casa e vê uma mesa ao centro da sala. Como ela está?", "o": ["Cheia, com muitas coisas em cima", "Completamente vazia"],
         "s": {"Cheia, com muitas coisas em cima": "Sente-se cercado de pessoas e vivências. Há uma sensação de plenitude social na sua vida no momento.", "Completamente vazia": "Pode estar passando por um período de maior solidão ou distância das pessoas. Há algo que ainda não foi preenchido."}},
        {"p": "No chão da sala, há uma xícara. O que você faz com ela?", "o": ["Pego e guardo com cuidado", "Deixo onde está"],
         "s": {"Pego e guardo com cuidado": "Tem um apreço muito especial pelas memórias. O passado tem um peso significativo nas suas escolhas e na sua identidade.", "Deixo onde está": "Vive voltado para o presente. Tem facilidade com o desapego e não costuma se prender ao que já passou."}},
        {"p": "Olhando com mais atenção, você percebe que a xícara é feita de que material?", "o": ["Porcelana fina", "Metal resistente"],
         "s": {"Porcelana fina": "Para você, o amor é algo delicado, precioso e que precisa ser tratado com cuidado e atenção.", "Metal resistente": "Para você, o amor é sinônimo de resistência. Acredita em laços fortes, que suportam o tempo e as adversidades."}},
        {"p": "Ao sair da casa, você encontra um lago. O que você faz?", "o": ["Mergulho de cabeça", "Molho apenas as mãos", "Passo direto sem parar"],
         "s": {"Mergulho de cabeça": "Quando se entrega, é completamente. Mergulha de corpo e alma nas experiências e nas emoções.", "Molho apenas as mãos": "Tem um equilíbrio admirável entre razão e sentimento. Participa das emoções sem se perder nelas.", "Passo direto sem parar": "É alguém extremamente focado nos seus objetivos. Não se distrai facilmente e tem uma disciplina pouco comum."}},
    ]

    if 'passo_floresta' not in st.session_state: st.session_state.passo_floresta = 0
    if 'analise_floresta' not in st.session_state: st.session_state.analise_floresta = []

    if st.session_state.passo_floresta < len(perguntas_floresta):
        q = perguntas_floresta[st.session_state.passo_floresta]
        total = len(perguntas_floresta)
        atual = st.session_state.passo_floresta + 1
        st.progress(atual / total)
        st.markdown(f"**Pergunta {atual} de {total}**")
        st.markdown(f"### {q['p']}")
        cols = st.columns(len(q['o']))
        for i, opt in enumerate(q['o']):
            if cols[i].button(opt, key=f"floresta_{st.session_state.passo_floresta}_{i}"):
                st.session_state.analise_floresta.append(q['s'][opt])
                st.session_state.passo_floresta += 1
                st.rerun()
    else:
        if chave_api and st.session_state.analise_floresta:
            respostas_txt = " ".join(st.session_state.analise_floresta)
            sistema_psi = (
                "Você é um psicólogo experiente e empático, especializado em análise de personalidade. "
                "Com base nos traços que vou descrever, produza um veredito psicológico em formato de texto corrido, "
                "como se estivesse falando diretamente com o paciente numa sessão presencial. "
                "Não use tópicos, listas ou itens numerados. Escreva como um parágrafo fluido e orgânico, "
                "integrando todos os traços numa narrativa coerente que fala sobre quem é essa pessoa, "
                "como ela pensa, como se relaciona e o que isso revela sobre sua forma de estar no mundo. "
                "O tom deve ser acolhedor, profundo e revelador."
            )
            with st.spinner("O Ravengar está lendo sua alma..."):
                veredito = consultar_ravengar(sistema_psi, f"Traços identificados: {respostas_txt}", chave_api)
            st.markdown(f"<div class='ravengar-card'>🧠 <strong>Veredito Psicológico</strong><br><br>{veredito}</div>", unsafe_allow_html=True)
        elif not chave_api:
            st.warning("Insira sua chave Groq API para receber o veredito.")
        if st.button("RECOMEÇAR JORNADA", key="recomecar_floresta"):
            st.session_state.passo_floresta = 0
            st.session_state.analise_floresta = []
            st.rerun()

# --- ABA 5: VIDAS PASSADAS ---
with tab5:
    st.markdown("### 🌀 Quem Você Foi em Outra Vida?")
    st.markdown("*Responda com sinceridade — são suas escolhas de hoje que revelam quem você foi ontem.*")

    perguntas_vidas = [
        {"p": "Quando você entra num ambiente desconhecido cheio de pessoas, o que acontece com você?",
         "o": ["Sinto uma energia estranha, como se já conhecesse aquele lugar", "Me sinto totalmente fora do lugar, quero ir embora", "Fico observando tudo com curiosidade antes de interagir"],
         "s": {"Sinto uma energia estranha, como se já conhecesse aquele lugar": "memória de vidas anteriores fortemente ativa; alma antiga com muitas experiências acumuladas", "Me sinto totalmente fora do lugar, quero ir embora": "alma que ainda está se adaptando ao plano terrestre; possivelmente vinda de uma existência mais sutil ou espiritual", "Fico observando tudo com curiosidade antes de interagir": "estrategista nato; provavelmente exerceu papéis de liderança ou comando em outras vidas"}},
        {"p": "Existe algum período histórico que te fascina de forma quase inexplicável, como se você pertencesse àquele tempo?",
         "o": ["Egito Antigo ou civilizações místicas", "Guerras medievais e batalhas", "Renascimento, artes e ciência", "Não sinto conexão com nenhum período específico"],
         "s": {"Egito Antigo ou civilizações místicas": "forte ligação com conhecimentos esotéricos e sacerdócio; possível vida como guardião de saberes antigos", "Guerras medievais e batalhas": "alma de guerreiro; viveu sob códigos de honra, lealdade e conflito físico em vidas anteriores", "Renascimento, artes e ciência": "espírito criativo e intelectual; provavelmente foi artista, filósofo, inventor ou pensador em outra existência", "Não sinto conexão com nenhum período específico": "alma em transição; ainda processando as memórias de vidas passadas que não vieram à tona completamente"}},
        {"p": "Você tem algum medo profundo, aquele tipo de medo que não consegue explicar de onde vem?",
         "o": ["Medo de afogamento ou de profundezas", "Medo de altura ou de quedas", "Medo de ser traído ou abandonado", "Medo de perder o controle ou a liberdade"],
         "s": {"Medo de afogamento ou de profundezas": "possível morte por afogamento ou naufrágio em vida anterior; alma que carrega esse trauma na memória celular", "Medo de altura ou de quedas": "queda fatal ou batalha em terreno elevado pode ter marcado uma de suas existências passadas", "Medo de ser traído ou abandonado": "viveu uma traição devastadora em outra vida — amor, amizade ou aliança que foi rompida de forma brutal", "Medo de perder o controle ou a liberdade": "possivelmente viveu como escravo, prisioneiro ou sob um regime opressivo; a busca por liberdade é o fio condutor de suas vidas"}},
        {"p": "Como você se relaciona com o sofrimento alheio — quando vê alguém em dor, o que acontece dentro de você?",
         "o": ["Sinto a dor do outro como se fosse minha", "Quero agir imediatamente para resolver", "Observo com compaixão, mas mantenho distância emocional", "Me sinto impotente e prefiro me afastar"],
         "s": {"Sinto a dor do outro como se fosse minha": "alma altamente empática; provavelmente viveu como curandeiro, terapeuta ou figura espiritual de cura", "Quero agir imediatamente para resolver": "herói ou protetor em outras vidas; carrega a missão de intervir e transformar realidades", "Observo com compaixão, mas mantenho distância emocional": "sábio ou mentor; alguém que guiou outros pelo conhecimento, mas aprendeu a preservar sua própria energia", "Me sinto impotente e prefiro me afastar": "viveu perdas traumáticas que não pôde evitar; ainda carrega a culpa de não ter conseguido salvar alguém importante"}},
        {"p": "O que te move profundamente na vida — aquilo que, quando falta, você sente que algo essencial está ausente?",
         "o": ["Conhecimento e descoberta", "Amor e pertencimento", "Justiça e propósito", "Criação e expressão"],
         "s": {"Conhecimento e descoberta": "eterna busca por compreender o mundo; viveu como filósofo, alquimista, cientista ou explorador", "Amor e pertencimento": "o amor é o fio que conecta todas as suas existências; busca constantemente reconhecer almas com quem já se conectou antes", "Justiça e propósito": "alma que sofreu injustiças ou lutou por causas maiores; veio com uma missão clara de transformar algo no mundo", "Criação e expressão": "artista da alma em múltiplas formas; viveu para criar, expressar e deixar marcas que transcendem o tempo"}},
        {"p": "Quando você sonha, como costumam ser esses sonhos?",
         "o": ["Vividos em lugares e épocas que não reconheço", "Cheios de simbolismos e imagens que parecem mensagens", "Muito reais, com pessoas que nunca conheci mas sinto como familiares", "Raramente lembro dos meus sonhos"],
         "s": {"Vividos em lugares e épocas que não reconheço": "memória de vidas passadas aflorando durante o sono; o véu entre as existências é fino para você", "Cheios de simbolismos e imagens que parecem mensagens": "canal aberto com o inconsciente coletivo; provavelmente foi vidente, oráculo ou intérprete de sonhos", "Muito reais, com pessoas que nunca conheci mas sinto como familiares": "encontros com almas que já cruzaram sua jornada em outras dimensões do tempo; vínculos que transcendem esta vida", "Raramente lembro dos meus sonhos": "alma com proteção natural das memórias mais intensas; o esquecimento é um mecanismo de equilíbrio para sua jornada atual"}},
        {"p": "Como as pessoas ao seu redor costumam te ver — qual papel você naturalmente ocupa nos grupos?",
         "o": ["O que escuta e acolhe a todos", "O que lidera e organiza", "O que questiona e provoca reflexão", "O que prefere ficar à margem, observando"],
         "s": {"O que escuta e acolhe a todos": "sacerdote, monge ou figura de consolo; viveu para ser o porto seguro de almas perdidas", "O que lidera e organiza": "rei, rainha, general ou comandante; carrega a autoridade natural de quem já governou vidas e destinos", "O que questiona e provoca reflexão": "filósofo, herético ou reformador; aquele que sempre desafiou o pensamento da sua época", "O que prefere ficar à margem, observando": "espião, monge solitário ou eremita; encontrou nas sombras e no silêncio o seu maior poder"}},
        {"p": "Existe algo que você sente que veio a este mundo para fazer — uma missão que às vezes sente, mesmo que não consiga nomear?",
         "o": ["Curar ou ajudar pessoas a se transformar", "Criar algo que deixe uma marca duradoura", "Proteger ou lutar por algo importante", "Entender e decifrar os mistérios da existência"],
         "s": {"Curar ou ajudar pessoas a se transformar": "médico, xamã, terapeuta ou curandeiro em outras vidas; a missão de cura se repete em todas as suas existências", "Criar algo que deixe uma marca duradoura": "artista, construtor ou visionário; viveu para erguer — monumentos, obras, ideias — que sobrevivem ao corpo", "Proteger ou lutar por algo importante": "guerreiro, cavaleiro ou guardião; veio com a missão de defender o que considera sagrado", "Entender e decifrar os mistérios da existência": "alquimista, filósofo ou místico; sua alma é movida pela necessidade de compreender o que está além do visível"}},
    ]

    if 'passo_vidas' not in st.session_state: st.session_state.passo_vidas = 0
    if 'analise_vidas' not in st.session_state: st.session_state.analise_vidas = []

    if st.session_state.passo_vidas < len(perguntas_vidas):
        q = perguntas_vidas[st.session_state.passo_vidas]
        total_v = len(perguntas_vidas)
        atual_v = st.session_state.passo_vidas + 1
        st.progress(atual_v / total_v)
        st.markdown(f"**Pergunta {atual_v} de {total_v}**")
        st.markdown(f"### {q['p']}")
        for i, opt in enumerate(q['o']):
            if st.button(opt, key=f"vidas_{st.session_state.passo_vidas}_{i}"):
                st.session_state.analise_vidas.append(q['s'][opt])
                st.session_state.passo_vidas += 1
                st.rerun()
    else:
        if chave_api and st.session_state.analise_vidas:
            tracos_v = " ".join(st.session_state.analise_vidas)
            sistema_vidas = (
                "Você é o Ravengar, um oráculo ancestral com acesso aos registros akáshicos. "
                "Com base nos traços descritos, revele quem essa pessoa foi em suas vidas passadas. "
                "Escreva em formato de texto corrido e fluido, como uma revelação solene e envolvente — nunca em lista. "
                "Descreva a(s) vida(s) passada(s) com riqueza: época, papel, o que viveu, como morreu e que karma trouxe. "
                "Tom místico, profundo e revelador. Finalize com uma mensagem sobre o que essa alma veio completar nesta encarnação."
            )
            with st.spinner("O Ravengar consulta os Registros Akáshicos..."):
                veredito_v = consultar_ravengar(sistema_vidas, f"Traços da alma: {tracos_v}", chave_api)
            st.markdown(f"<div class='ravengar-card'>🌀 <strong>Revelação das Vidas Passadas</strong><br><br>{veredito_v}</div>", unsafe_allow_html=True)
        elif not chave_api:
            st.warning("Insira sua chave Groq API para receber a revelação.")
        if st.button("RECOMEÇAR JORNADA", key="recomecar_vidas"):
            st.session_state.passo_vidas = 0
            st.session_state.analise_vidas = []
            st.rerun()

# --- ABA 6: CARTA DO TAROT ---
with tab6:
    st.markdown("### 🃏 Tire Sua Carta do Tarot")
    st.markdown("*Respire fundo. Concentre-se no seu momento atual. Quando sentir que está pronto, clique.*")

    ARCANOS = [
        {"nome": "O Louco", "simbolo": "🌟", "numero": "0"},
        {"nome": "O Mago", "simbolo": "🪄", "numero": "I"},
        {"nome": "A Sacerdotisa", "simbolo": "🌙", "numero": "II"},
        {"nome": "A Imperatriz", "simbolo": "🌸", "numero": "III"},
        {"nome": "O Imperador", "simbolo": "👑", "numero": "IV"},
        {"nome": "O Hierofante", "simbolo": "⛪", "numero": "V"},
        {"nome": "Os Amantes", "simbolo": "💞", "numero": "VI"},
        {"nome": "O Carro", "simbolo": "⚡", "numero": "VII"},
        {"nome": "A Força", "simbolo": "🦁", "numero": "VIII"},
        {"nome": "O Eremita", "simbolo": "🕯️", "numero": "IX"},
        {"nome": "A Roda da Fortuna", "simbolo": "🎡", "numero": "X"},
        {"nome": "A Justiça", "simbolo": "⚖️", "numero": "XI"},
        {"nome": "O Enforcado", "simbolo": "🌿", "numero": "XII"},
        {"nome": "A Morte", "simbolo": "🦋", "numero": "XIII"},
        {"nome": "A Temperança", "simbolo": "🌊", "numero": "XIV"},
        {"nome": "O Diabo", "simbolo": "🔗", "numero": "XV"},
        {"nome": "A Torre", "simbolo": "⛈️", "numero": "XVI"},
        {"nome": "A Estrela", "simbolo": "✨", "numero": "XVII"},
        {"nome": "A Lua", "simbolo": "🌕", "numero": "XVIII"},
        {"nome": "O Sol", "simbolo": "☀️", "numero": "XIX"},
        {"nome": "O Julgamento", "simbolo": "🎺", "numero": "XX"},
        {"nome": "O Mundo", "simbolo": "🌍", "numero": "XXI"},
    ]

    if st.button("🃏 REVELAR MINHA CARTA DO DIA"):
        st.session_state['carta_do_dia'] = random.choice(ARCANOS)

    if 'carta_do_dia' in st.session_state:
        carta = st.session_state['carta_do_dia']
        st.markdown(f"""
        <div class='tarot-card'>
            <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;'>ARCANO {carta['numero']}</div>
            <div class='tarot-simbolo'>{carta['simbolo']}</div>
            <div class='tarot-titulo'>{carta['nome']}</div>
        </div>
        """, unsafe_allow_html=True)
        if chave_api:
            with st.spinner("O Ravengar interpreta os símbolos..."):
                sistema_tarot = (
                    "Você é o Ravengar, intérprete dos arcanos do Tarot. "
                    "Produza uma leitura profunda e envolvente em texto corrido — sem tópicos, sem listas. "
                    "Fale diretamente com quem tirou a carta, em segunda pessoa. "
                    "Aborde o significado geral, o que revela sobre o momento atual, as energias em jogo e uma orientação para as próximas horas. "
                    "Tom místico, sábio e acolhedor."
                )
                leitura = consultar_ravengar(sistema_tarot, f"A carta tirada foi: {carta['nome']} (Arcano {carta['numero']})", chave_api)
            st.markdown(f"<div class='ravengar-card'>🔮 <strong>Leitura da Carta</strong><br><br>{leitura}</div>", unsafe_allow_html=True)
        if st.button("🔄 TIRAR NOVA CARTA"):
            del st.session_state['carta_do_dia']
            st.rerun()

# --- ABA 7: MAPA ASTRAL ---
with tab7:
    st.markdown("### ⭐ Mapa Astral Rápido")
    st.markdown("*Informe seus dados de nascimento e o Ravengar revela os seus três signos fundamentais.*")

    col1, col2, col3 = st.columns(3)
    with col1:
        data_nasc = st.text_input("📅 Data de nascimento:", placeholder="ex: 15/03/1990", key="astral_data")
    with col2:
        hora_nasc = st.text_input("🕐 Hora de nascimento:", placeholder="ex: 14h30 (opcional)", key="astral_hora")
    with col3:
        cidade_nasc = st.text_input("📍 Cidade de nascimento:", placeholder="ex: São Paulo, SP", key="astral_cidade")

    if st.button("⭐ REVELAR MEU MAPA ASTRAL"):
        if data_nasc.strip():
            with st.spinner("Os astros se alinham..."):
                sistema_astral = (
                    "Você é o Ravengar, astrólogo ancestral. Com base na data, hora e cidade de nascimento fornecidas, "
                    "identifique o signo solar, o signo lunar provável e o ascendente provável da pessoa. "
                    "Se a hora não foi fornecida, mencione que o ascendente é estimado. "
                    "Escreva a leitura em texto corrido e fluido, como uma revelação direta à pessoa, em segunda pessoa. "
                    "Integre os três signos numa narrativa coerente sobre quem essa pessoa é, como pensa, como ama e qual sua missão. "
                    "Tom místico, profundo e revelador. Não use listas."
                )
                leitura_astral = consultar_ravengar(
                    sistema_astral,
                    f"Data: {data_nasc}. Hora: {hora_nasc or 'não informada'}. Cidade: {cidade_nasc or 'não informada'}.",
                    chave_api
                )
            st.markdown(f"""
            <div class='astral-box'>
                ⭐ <strong>Seu Mapa Astral</strong><br><br>{leitura_astral}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Informe ao menos a data de nascimento.")

# --- ABA 8: COMPATIBILIDADE ---
with tab8:
    st.markdown("### 💞 Compatibilidade entre Duas Almas")
    st.markdown("*O Ravengar revela se essas almas têm conexão kármica e o que o destino reserva para elas.*")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Alma 1**")
        nome1 = st.text_input("Nome:", key="comp_nome1", placeholder="ex: Maria")
        signo1 = st.selectbox("Signo:", ["Áries","Touro","Gêmeos","Câncer","Leão","Virgem","Libra","Escorpião","Sagitário","Capricórnio","Aquário","Peixes"], key="comp_signo1")
    with col2:
        st.markdown("**Alma 2**")
        nome2 = st.text_input("Nome:", key="comp_nome2", placeholder="ex: João")
        signo2 = st.selectbox("Signo:", ["Áries","Touro","Gêmeos","Câncer","Leão","Virgem","Libra","Escorpião","Sagitário","Capricórnio","Aquário","Peixes"], key="comp_signo2")

    tipo_relacao = st.selectbox("Tipo de relação:", ["Amor e romance","Amizade profunda","Parceria profissional","Família"], key="comp_tipo")

    if st.button("💞 REVELAR COMPATIBILIDADE"):
        if nome1.strip() and nome2.strip():
            with st.spinner("O Ravengar consulta os registros kármicos..."):
                sistema_comp = (
                    "Você é o Ravengar, guardião dos registros kármicos. "
                    "Analise a compatibilidade entre duas pessoas com base nos signos e tipo de relação. "
                    "Escreva em texto corrido, fluido e revelador — sem listas. "
                    "Aborde: o que une essas almas, o que pode gerar conflito, se há conexão kármica de vidas passadas, "
                    "o potencial da relação e o que o destino reserva para elas. "
                    "Tom místico, apaixonante e profundo."
                )
                leitura_comp = consultar_ravengar(
                    sistema_comp,
                    f"{nome1} ({signo1}) e {nome2} ({signo2}). Tipo de relação: {tipo_relacao}.",
                    chave_api
                )
            st.markdown(f"<div class='ravengar-card'>💞 <strong>{nome1} & {nome2}</strong><br><br>{leitura_comp}</div>", unsafe_allow_html=True)
        else:
            st.warning("Informe os dois nomes.")

# --- ABA 9: NUMEROLOGIA ---
with tab9:
    st.markdown("### 🔢 Numerologia do Nome e do Destino")
    st.markdown("*Seu nome completo e sua data de nascimento carregam um código numérico que o Ravengar pode decifrar.*")

    nome_num = st.text_input("✍️ Seu nome completo:", key="num_nome", placeholder="ex: Maria Aparecida Silva")
    data_num = st.text_input("📅 Sua data de nascimento:", key="num_data", placeholder="ex: 15/03/1990")

    if st.button("🔢 DECIFRAR MEU CÓDIGO NUMÉRICO"):
        if nome_num.strip() and data_num.strip():
            with st.spinner("O Ravengar calcula os números do seu destino..."):
                sistema_num = (
                    "Você é o Ravengar, numerólogo ancestral. Com base no nome completo e data de nascimento, "
                    "calcule e interprete: o Número do Destino (soma dos dígitos da data de nascimento reduzida), "
                    "o Número da Alma (soma das vogais do nome, reduzida) e o Número da Personalidade (soma das consoantes). "
                    "Mostre o cálculo de forma simples, depois escreva a interpretação integrada em texto corrido fluido, "
                    "em segunda pessoa, como uma revelação direta. Tom místico e revelador."
                )
                leitura_num = consultar_ravengar(
                    sistema_num,
                    f"Nome: {nome_num}. Data: {data_num}.",
                    chave_api
                )
            st.markdown(f"<div class='ravengar-card'>🔢 <strong>Seu Código Numérico</strong><br><br>{leitura_num}</div>", unsafe_allow_html=True)
        else:
            st.warning("Informe o nome completo e a data de nascimento.")

# --- ABA 10: ESPELHO NEGRO ---
with tab10:
    st.markdown("### 🖤 O Espelho Negro")
    st.markdown("*Descreva um sonho recorrente, perturbador ou aquele que nunca saiu da sua cabeça. O Ravengar vai ao fundo.*")

    sonho_input = st.text_area("🌙 Descreva o sonho com todos os detalhes que lembrar:", height=160, key="sonho_input",
        placeholder="ex: Estou sempre num corredor comprido e escuro, sem saída. Sinto que alguém me segue mas quando olho não há ninguém. Acordo com o coração acelerado...")

    if st.button("🖤 INTERPRETAR O SONHO"):
        if sonho_input.strip():
            with st.spinner("O Ravengar mergulha nas sombras do seu inconsciente..."):
                sistema_sonho = (
                    "Você é o Ravengar, intérprete do inconsciente e dos reinos oníricos. "
                    "Analise este sonho com profundidade — vá além do óbvio. "
                    "Escreva em texto corrido, fluido e perturbadoramente preciso, em segunda pessoa. "
                    "Aborde: o que os símbolos representam no inconsciente, o que a mente está tentando comunicar, "
                    "que emoção ou situação não resolvida pode estar gerando esse sonho, e o que ele revela sobre o momento atual da pessoa. "
                    "Tom sombrio, perspicaz e revelador — como se o Ravengar visse algo que a própria pessoa ainda não ousou olhar."
                )
                interpretacao = consultar_ravengar(sistema_sonho, f"O sonho: {sonho_input}", chave_api)
            st.markdown(f"<div class='ravengar-card'>🖤 <strong>O Que as Sombras Revelam</strong><br><br>{interpretacao}</div>", unsafe_allow_html=True)
        else:
            st.warning("Descreva o sonho antes de invocar o Espelho Negro.")

# --- ABA 11: RITUAL DE INTENÇÃO ---
with tab11:
    st.markdown("### 🌙 Ritual de Intenção")
    st.markdown("*Escreva o que você quer manifestar. O Ravengar cria um ritual personalizado para você.*")

    intencao_input = st.text_area("✨ O que você quer manifestar?", height=120, key="intencao_input",
        placeholder="ex: Quero encontrar um amor verdadeiro, quero prosperidade no meu negócio, quero me libertar de um relacionamento tóxico...")

    if st.button("🌙 CRIAR MEU RITUAL"):
        if intencao_input.strip():
            with st.spinner("O Ravengar consulta as forças do universo..."):
                sistema_ritual = (
                    "Você é o Ravengar, guardião dos rituais de intenção e manifestação. "
                    "Com base na intenção descrita, crie um ritual personalizado e simbólico. "
                    "Escreva em texto corrido, revelador e envolvente. Inclua: "
                    "a melhor fase da lua para realizar o ritual, o elemento associado (fogo, água, terra, ar), "
                    "uma afirmação poderosa personalizada para essa intenção específica, "
                    "um gesto físico simbólico para ancorar a intenção, "
                    "e uma orientação sobre como liberar o que precisa ser liberado para abrir espaço ao que se deseja manifestar. "
                    "Tom místico, poético e profundamente pessoal — como se o ritual tivesse sido criado especialmente para essa alma."
                )
                ritual = consultar_ravengar(sistema_ritual, f"Intenção: {intencao_input}", chave_api)
            st.markdown(f"<div class='ravengar-card'>🌙 <strong>Seu Ritual de Intenção</strong><br><br>{ritual}</div>", unsafe_allow_html=True)
        else:
            st.warning("Escreva sua intenção antes de invocar o ritual.")

# --- ABA 12: ORÁCULO DAS RUNAS ---
with tab12:
    st.markdown("### ᚠ Oráculo das Runas")
    st.markdown("*As runas nórdicas carregam a sabedoria ancestral dos povos do norte. Concentre-se e tire a sua.*")

    RUNAS = [
        {"nome": "Fehu", "simbolo": "ᚠ", "palavra": "Prosperidade", "elemento": "Fogo"},
        {"nome": "Uruz", "simbolo": "ᚢ", "palavra": "Força", "elemento": "Terra"},
        {"nome": "Thurisaz", "simbolo": "ᚦ", "palavra": "Proteção", "elemento": "Fogo"},
        {"nome": "Ansuz", "simbolo": "ᚨ", "palavra": "Sabedoria", "elemento": "Ar"},
        {"nome": "Raidho", "simbolo": "ᚱ", "palavra": "Jornada", "elemento": "Ar"},
        {"nome": "Kenaz", "simbolo": "ᚲ", "palavra": "Iluminação", "elemento": "Fogo"},
        {"nome": "Gebo", "simbolo": "ᚷ", "palavra": "Dádiva", "elemento": "Ar"},
        {"nome": "Wunjo", "simbolo": "ᚹ", "palavra": "Alegria", "elemento": "Terra"},
        {"nome": "Hagalaz", "simbolo": "ᚺ", "palavra": "Ruptura", "elemento": "Água"},
        {"nome": "Nauthiz", "simbolo": "ᚾ", "palavra": "Necessidade", "elemento": "Fogo"},
        {"nome": "Isa", "simbolo": "ᛁ", "palavra": "Pausa", "elemento": "Água"},
        {"nome": "Jera", "simbolo": "ᛃ", "palavra": "Colheita", "elemento": "Terra"},
        {"nome": "Eihwaz", "simbolo": "ᛇ", "palavra": "Transformação", "elemento": "Terra"},
        {"nome": "Perthro", "simbolo": "ᛈ", "palavra": "Mistério", "elemento": "Água"},
        {"nome": "Algiz", "simbolo": "ᛉ", "palavra": "Escudo", "elemento": "Ar"},
        {"nome": "Sowilo", "simbolo": "ᛊ", "palavra": "Vitória", "elemento": "Fogo"},
        {"nome": "Tiwaz", "simbolo": "ᛏ", "palavra": "Justiça", "elemento": "Ar"},
        {"nome": "Berkano", "simbolo": "ᛒ", "palavra": "Renascimento", "elemento": "Terra"},
        {"nome": "Ehwaz", "simbolo": "ᛖ", "palavra": "Movimento", "elemento": "Ar"},
        {"nome": "Mannaz", "simbolo": "ᛗ", "palavra": "Humanidade", "elemento": "Ar"},
        {"nome": "Laguz", "simbolo": "ᛚ", "palavra": "Fluxo", "elemento": "Água"},
        {"nome": "Ingwaz", "simbolo": "ᛜ", "palavra": "Fertilidade", "elemento": "Terra"},
        {"nome": "Dagaz", "simbolo": "ᛞ", "palavra": "Clareza", "elemento": "Fogo"},
        {"nome": "Othala", "simbolo": "ᛟ", "palavra": "Herança", "elemento": "Terra"},
    ]

    if st.button("ᚠ TIRAR MINHA RUNA"):
        st.session_state['runa_do_dia'] = random.choice(RUNAS)

    if 'runa_do_dia' in st.session_state:
        runa = st.session_state['runa_do_dia']
        st.markdown(f"""
        <div class='runa-card'>
            <div style='font-size:0.82em;opacity:0.6;letter-spacing:2px;'>RUNA DO DIA · {runa['elemento'].upper()}</div>
            <div class='runa-simbolo'>{runa['simbolo']}</div>
            <div class='runa-nome'>{runa['nome']}</div>
            <div style='font-size:0.95em;margin-top:6px;opacity:0.8;'>{runa['palavra']}</div>
        </div>
        """, unsafe_allow_html=True)

        if chave_api:
            with st.spinner("As runas sussurram..."):
                sistema_runa = (
                    "Você é o Ravengar, conhecedor da tradição rúnica nórdica e dos segredos do Elder Futhark. "
                    "Interprete esta runa de forma profunda e personalizada para quem a tirou hoje. "
                    "Escreva em texto corrido, em segunda pessoa, sem listas. "
                    "Aborde: o significado ancestral da runa, o que ela revela sobre o momento atual, "
                    "o que deve ser observado ou cuidado, e a mensagem que os ancestrais enviam através dela. "
                    "Tom sombrio, ancestral e revelador."
                )
                leitura_runa = consultar_ravengar(
                    sistema_runa,
                    f"A runa tirada foi: {runa['nome']} ({runa['simbolo']}) — {runa['palavra']}. Elemento: {runa['elemento']}.",
                    chave_api
                )
            st.markdown(f"<div class='ravengar-card'>ᚠ <strong>Mensagem dos Ancestrais</strong><br><br>{leitura_runa}</div>", unsafe_allow_html=True)

        if st.button("🔄 TIRAR NOVA RUNA"):
            del st.session_state['runa_do_dia']
            st.rerun()

# --- RODAPÉ ---
st.markdown("""
<div class='rodape-ravengar'>
    ✦ EXPLORANDO OS MISTÉRIOS DA MENTE E DO DESTINO ✦<br>
    © 2026 TENDA DO RAVENGAR
</div>
""", unsafe_allow_html=True)
