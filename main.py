import streamlit as st
from groq import Groq
import random
import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    /* Esconde a barra lateral completamente */
    [data-testid="stSidebar"] {{display: none;}}
    
    .stApp {{ background-color: #F7F7F7 !important; padding-bottom: 100px; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }}

    /* BOTÃO PRETO ESTILO NEXUS */
    .tool-link {{
        display: inline-block;
        background: #000000 !important;
        color: #FFFFFF !important;
        padding: 8px 15px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 8px;
        border: none;
    }}

    /* RODAPÉ AZUL FIXO ESTILO NEXUS */
    .footer-nexus {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #00BFFF !important;
        color: #000000 !important;
        text-align: center;
        padding: 15px 0;
        font-weight: bold;
        z-index: 9999;
        border-top: 2px solid #0080FF;
        font-size: 16px;
    }}

    .quiz-pergunta {{
        font-size: 26px !important;
        font-weight: 600 !important;
        margin-bottom: 30px !important;
        line-height: 1.4;
    }}

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

    .ravengar-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFD1DC !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    .msg-balao {{
        background-color: #FFF5F7 !important;
        border-left: 5px solid #FFB7C5 !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
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

# --- RODAPÉ FIXO ---
st.markdown("""
    <div class="footer-nexus">
        Acesse <a href="http://www.quizmaispremios.com.br" target="_blank" style="color: #000; text-decoration: underline;">www.quizmaispremios.com.br</a> 
        e venha se divertir com a gente e ganhar muitos prêmios!
    </div>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DO MURAL GLOBAL ---
@st.cache_resource
def obter_mural_global():
    return [] 

mural_global = obter_mural_global()

# --- 3. LÓGICA DE CONEXÃO ---
def consultar_ravengar(pergunta, api_key, setor="Destino", historico=None):
    prompts = {
        "Amor": "És o Ravengar, o Guardião dos Afetos. Tua linguagem é poética, profunda e empática.",
        "Trabalho": "És o Ravengar, o Estrategista das Sombras. Direta, fria e focada em poder.",
        "Futuro": "És o Ravengar, o Profeta do Tempo. Enigmática, vasta e mística.",
        "Saude": "És o Ravengar, o Alquimista da Vitalidade. Serena e equilibrada.",
        "Decifrador": "És o Ravengar. Traduz símbolos e sonhos com mistério.",
        "Detetive": "ÉS O RAVENGAR, o Detetive Virtual. Analisa o comportamento com lógica fria e mantém o fio da conversa.",
        "Noticias": "És o Ravengar. Resume notícias de forma mística e ácida.",
        "Tarot": "És o Ravengar, o mestre das cartas.",
        "Revelacao": "És o Ravengar. O usuário terminou o teste 'Quem você foi na vida passada'. Com base no perfil dele, faça uma REVELAÇÃO misteriosa e curta. Comece com 'Isso explica muita coisa...' e termine com um conselho ancestral."
    }
    
    sistema = prompts.get(setor, "És o Ravengar, um oráculo místico.")
    sistema += f" Nome do consulente: {st.session_state.get('nome_user', 'Visitante')}."

    if historico:
        mensagens = [{"role": "system", "content": sistema}] + historico
    else:
        mensagens = [{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}]

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=mensagens,
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

# --- 4. IDENTIFICAÇÃO ---
if 'usuario_identificado' not in st.session_state:
   st.session_state.usuario_identificado = False

if not st.session_state.usuario_identificado:
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    col_central = st.columns([1, 2, 1])[1]
    with col_central:
        nome_input = st.text_input("Como as sombras te devem chamar?")
        genero_input = st.radio("O teu género:", ["Masculino", "Feminino"])
        
        # --- LINK OBTER CHAVE ACIMA DO INPUT ---
        st.markdown("<a href='https://console.groq.com/keys' target='_blank' class='tool-link'>Obter chave Groq grátis</a>", unsafe_allow_html=True)
        chave_input = st.text_input("Sua Chave Groq API:", type="password")
        
        if st.button("ENTRAR NA TENDA"):
            if nome_input and chave_input:
                st.session_state.nome_user, st.session_state.genero_user = nome_input, genero_input
                st.session_state.chave_api = chave_input
                st.session_state.usuario_identificado = True
                st.rerun()
            else:
                st.error("Por favor, informe seu nome e sua chave API.")
else:
    # --- INTERFACE PRINCIPAL ---
    chave_api = st.session_state.chave_api
    st.markdown("<h1 style='text-align: center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>✨ Boas-vindas à Tenda, <b>{st.session_state.nome_user}</b>. <small>({len(mural_global)} mensagens no Mural)</small></p>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Oráculo", "📜 Vidas Passadas", "👁️ Decifrador", "🕵️ Detetive Virtual", "🧠 Quiz Psicológico", "👉 Biblioteca Secreta", "🧘 Seu Espaço", "🤝 Encontros"])

    with tabs[0]: # ORÁCULO
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            if st.button("❤️ AMOR", key="btn_Amor"): st.session_state.setor = "Amor"; st.rerun()
        with c2: 
            if st.button("💼 TRABALHO", key="btn_Trabalho"): st.session_state.setor = "Trabalho"; st.rerun()
        with c3: 
            if st.button("✨ FUTURO", key="btn_Futuro"): st.session_state.setor = "Futuro"; st.rerun()
        with c4: 
            if st.button("🌿 SAÚDE", key="btn_Saude"): st.session_state.setor = "Saude"; st.rerun()
        
        setor_atual = st.session_state.get('setor', 'Destino')
        pergunta_ora = st.text_area(f"O que desejas saber sobre o teu {setor_atual}?")
        if st.button("PROFERIR VEREDITO"):
            if chave_api and pergunta_ora:
                st.session_state['chat_ora'] = [{"content": consultar_ravengar(pergunta_ora, api_key=chave_api, setor=setor_atual)}]
        if 'chat_ora' in st.session_state:
            for msg in st.session_state['chat_ora']:
                st.markdown(f"<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    with tabs[1]: # QUEM VOCÊ FOI NA VIDA PASSADA
        if 'jogo_vp' not in st.session_state:
            st.session_state.jogo_vp = {"passo": 0, "pontos": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}}
        
        vp = st.session_state.jogo_vp

        if vp["passo"] == 0:
            st.markdown("<div style='text-align: center; padding: 20px;'><h2>Quem você foi na vida passada? 🔮</h2><p>As sombras guardam memórias que sua mente consciente esqueceu. Vamos buscá-las.</p></div>", unsafe_allow_html=True)
            if st.button("INICIAR REVELAÇÃO"):
                vp["passo"] = 1; st.rerun()
        
        elif vp["passo"] <= 7:
            perguntas_vp = [
                {"p": "Qual destes cenários te traz uma sensação estranha de 'já estive aqui'?", "o": {"A": "Uma sala de guerra estratégica", "B": "Um palco sob aplausos", "C": "Uma caravana sem destino", "D": "Um observatório solitário"}},
                {"p": "O que você mais valoriza em uma jornada?", "o": {"A": "O plano bem executado", "B": "O impacto deixado nas pessoas", "C": "A liberdade de mudar a rota", "D": "A compreensão dos sinais ocultos"}},
                {"p": "Como você lida com um novo grupo de pessoas?", "o": {"E": "Busco unir todos e criar harmonia", "F": "Prefiro ouvir e aprender tudo primeiro", "A": "Analiso quem é quem e as intenções", "B": "Tomo a frente naturalmente"}},
                {"p": "Qual o seu maior medo?", "o": {"C": "Ficar preso a uma rotina eterna", "D": "Ignorar um detalhe crucial", "E": "Ver o conflito separar as pessoas", "F": "Ficar na superfície do conhecimento"}},
                {"p": "Ao se deparar com uma injustiça, qual sua reação ancestral?", "o": {"A": "Punição imediata e justa", "E": "Diplomacia para acalmar os ânimos", "B": "Denúncia pública fervorosa", "D": "Observação fria para entender o motivo"}},
                {"p": "Se pudesse escolher um artefato antigo para carregar hoje:", "o": {"F": "Um pergaminho de sabedoria esquecida", "C": "Um mapa de terras nunca visitadas", "A": "Uma adaga de proteção leal", "B": "Um amuleto que atrai multidões"}},
                {"p": "Como você prefere terminar o seu dia?", "o": {"D": "Em silêncio, refletindo sobre o que vi", "F": "Estudando algo que me instruiga", "E": "Rodeado de quem traz paz", "C": "Planejando o próximo destino"}}
            ]
            q = perguntas_vp[vp["passo"]-1]
            st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
            for key, val in q['o'].items():
                if st.button(val, key=f"vp_{vp['passo']}_{key}"):
                    vp["pontos"][key] += 1
                    vp["passo"] += 1
                    st.rerun()
        else:
            vencedor = max(vp["pontos"], key=vp["pontos"].get)
            perfis = {
                "A": "🎯 O Estrategista\n“Você foi alguém que pensava à frente… Tomava decisões calculadas e raramente agia por impulso.”",
                "B": "🔥 O Influente\n“Você foi alguém que impactava pessoas… Sua presença chamava atenção naturalmente.”",
                "C": "🌍 O Livre\n“Você foi alguém que não aceitava limites… Sempre buscava novos caminhos.”",
                "D": "🧠 O Observador\n“Você foi alguém que enxergava além… Percebia detalhes que outros ignoravam.”",
                "E": "💬 O Conector\n“Você foi alguém que unia pessoas… Criava laços e resolvia conflitos.”",
                "F": "📚 O Buscador\n“Você foi alguém que buscava entender tudo… O conhecimento era sua essência.”"
            }
            perfil_final = perfis[vencedor]

            if 'revelacao_final' not in st.session_state:
                with st.spinner("Conectando com suas vidas passadas..."):
                    prompt_revelacao = f"Perfil: {perfil_final}. Faça uma leitura mística."
                    st.session_state.revelacao_final = consultar_ravengar(prompt_revelacao, chave_api, setor="Revelacao")
            
            st.markdown(f"<div class='ravengar-card'><h3>Sua Essência Ancestral</h3><p>{perfil_final}</p><hr><p>{st.session_state.revelacao_final}</p></div>", unsafe_allow_html=True)
            if st.button("REPETIR RITUAL"):
                del st.session_state.jogo_vp
                if 'revelacao_final' in st.session_state: del st.session_state.revelacao_final
                st.rerun()

    with tabs[2]: # DECIFRADOR
        texto_dec = st.text_area("Descreve o símbolo ou sonho:")
        if st.button("DECIFRAR MISTÉRIO"):
            if chave_api and texto_dec:
                st.session_state['chat_dec'] = [{"content": consultar_ravengar(texto_dec, api_key=chave_api, setor="Decifrador")}]
        if 'chat_dec' in st.session_state:
            for msg in st.session_state['chat_ora']:
                 st.markdown(f"<div class='ravengar-card'>👁️ {msg['content']}</div>", unsafe_allow_html=True)

    with tabs[3]: # DETETIVE VIRTUAL
        if 'historico_detetive' not in st.session_state:
            st.session_state.historico_detetive = []
        nome_alvo = st.text_input("Quem vamos investigar?", placeholder="Ex: A pessoa misteriosa...")
        for msg in st.session_state.historico_detetive:
            st.write(f"**{msg['role']}:** {msg['content']}")
        if prompt := st.chat_input("Diga alguma coisa..."):
            st.session_state.historico_detetive.append({"role": "user", "content": f"Sobre {nome_alvo}: {prompt}"})
            resposta = consultar_ravengar("", api_key=chave_api, setor="Detetive", historico=st.session_state.historive_detetive)
            st.session_state.historico_detetive.append({"role": "assistant", "content": resposta})
            st.rerun()

    with tabs[4]: # QUIZ PSICOLÓGICO
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR", key="start_quiz"):
                st.session_state.quiz_iniciado = True; st.session_state.passo = 0; st.session_state.analise = []; st.rerun()
        else:
            # Lógica das perguntas (Resumida para o código rodar sem erro)
            st.write("Caminhando pela floresta...")
            if st.button("Continuar"): st.session_state.passo += 1; st.rerun()

    with tabs[5]: # BIBLIOTECA SECRETA
        st.markdown("<h2 style='text-align: center;'>👉 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        cursos = [
            {"titulo": "🔮 Leitura Fria", "url": "https://drive.google.com/file/d/1Yn7BkHCKjJPEXb3Rtip11ZxO0R11a1bd/view?usp=sharing"},
            {"titulo": "✋ Leitura de Mãos", "url": "https://drive.google.com/file/d/1jDHSLRzxB2jQbTnpsdegLvMITqLKhHN5/view?usp=sharing"},
            {"titulo": "🔢 Numerologia", "url": "https://drive.google.com/file/d/1t0x1eEvlXQbEOO24OZghlAC4x8yLbvzh/view?usp=sharing"}
        ]
        for item in cursos:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4></div>", unsafe_allow_html=True)
            st.link_button("📥 Baixar PDF", item["url"])

    with tabs[6]: # SEU ESPAÇO
        st.markdown("### 🃏 Tarot do Dia")
        if st.button("PUXAR CARTA"):
            st.session_state.carta = random.choice(["O Mago", "O Louco", "A Estrela"])
            st.success(f"Sua carta é: {st.session_state.carta}")

    with tabs[7]: # ENCONTROS
        st.markdown("### 💬 Mural de Almas")
        msg_mural = st.text_area("Deixe sua marca...")
        if st.button("LANÇAR"):
            mural_global.append({"usuario": st.session_state.nome_user, "texto": msg_mural, "hora": "Agora"})
            st.rerun()

    if st.button("🔄 REINICIAR SESSÃO"):
        st.session_state.clear()
        st.rerun()
