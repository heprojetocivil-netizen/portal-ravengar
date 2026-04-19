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
    
    .stApp {{ background-color: #F7F7F7 !important; }}
    
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, label, div {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
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
                st.markdown(f<div class='ravengar-card'>🔮 **Ravengar:**<br>{msg['content']}</div>", unsafe_allow_html=True)

    with tabs[1]: # QUEM VOCÊ FOI NA VIDA PASSADA
        if 'jogo_vp' not in st.session_state:
            st.session_state.jogo_vp = {"passo": 0, "pontos": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}}
        
        vp = st.session_state.jogo_vp

        if vp["passo"] == 0:
            st.markdown("<div style='text-align: center; padding: 20px;'><h2>Quem você foi na vida passada? 🔮</h2><p>As sombras guardam memórias que sua mente consciente esqueceu. Vamos buscá-las.</p></div>", unsafe_allow_html=True)
            if st.button("INICIAR REVELAÇÃO"):
                vp["passo"] = 1; st.rerun()
        
        elif vp["passo"] <= 4:
            perguntas_vp = [
                {"p": "Qual destes cenários te traz uma sensação estranha de 'já estive aqui'?", "o": {"A": "Uma sala de guerra estratégica", "B": "Um palco sob aplausos", "C": "Uma caravana sem destino", "D": "Um observatório solitário"}},
                {"p": "O que você mais valoriza em uma jornada?", "o": {"A": "O plano bem executado", "B": "O impacto deixado nas pessoas", "C": "A liberdade de mudar a rota", "D": "A compreensão dos sinais ocultos"}},
                {"p": "Como você lida com um novo grupo de pessoas?", "o": {"E": "Busco unir todos e criar harmonia", "F": "Prefiro ouvir e aprender tudo primeiro", "A": "Analiso quem é quem e as intenções", "B": "Tomo a frente naturalmente"}},
                {"p": "Qual o seu maior medo?", "o": {"C": "Ficar preso a uma rotina eterna", "D": "Ignorar um detalhe crucial", "E": "Ver o conflito separar as pessoas", "F": "Ficar na superfície do conhecimento"}}
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
                "A": "🎯 O Estrategista\n“Você foi alguém que pensava à frente… Tomava decisões calculadas e raramente agia por impulso. Sua mente sempre esteve alguns passos à frente dos outros.”",
                "B": "🔥 O Influente\n“Você foi alguém que impactava pessoas… Sua presença chamava atenção naturalmente, e suas palavras tinham peso. Mesmo sem perceber, você guiava decisões ao seu redor.”",
                "C": "🌍 O Livre\n“Você foi alguém que não aceitava limites… Sempre buscava novos caminhos, novas experiências e novos começos. A rotina nunca conseguiu te prender.”",
                "D": "🧠 O Observador\n“Você foi alguém que enxergava além… Percebia detalhes, intenções e sinais que outros ignoravam. Enquanto muitos falavam, você entendia.”",
                "E": "💬 O Conector\n“Você foi alguém que unia pessoas… Criava laços, resolvia conflitos e aproximava caminhos. Tinha facilidade natural em lidar com diferentes tipos de pessoas.”",
                "F": "📚 O Buscador\n“Você foi alguém que buscava entender tudo… Nunca se contentava com o superficial e sempre queria ir mais fundo. O conhecimento era parte da sua essência.”"
            }
            perfil_final = perfis[vencedor]

            if 'revelacao_final' not in st.session_state:
                with st.spinner("Conectando com suas vidas passadas..."):
                    prompt_revelacao = f"O usuário foi identificado com o seguinte perfil de vida passada: {perfil_final}. Faça uma leitura mística e curta sobre como essa essência ancestral influencia o presente dele."
                    st.session_state.revelacao_final = consultar_ravengar(prompt_revelacao, chave_api, setor="Revelacao")
            
            st.markdown(f"<div class='ravengar-card'><h3>Sua Essência Ancestral</h3><p style='font-size: 1.2em; white-space: pre-wrap;'>{perfil_final}</p><hr><p>{st.session_state.revelacao_final}</p></div>", unsafe_allow_html=True)
            
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
            for msg in st.session_state['chat_dec']:
                st.markdown(f"<div class='ravengar-card'>👁️ {msg['content']}</div>", unsafe_allow_html=True)

    with tabs[3]: # DETETIVE VIRTUAL
        if 'historico_detetive' not in st.session_state:
            st.session_state.historico_detetive = []

        nome_alvo = st.text_input("Quem vamos investigar?", placeholder="Ex: A pessoa misteriosa...")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.historico_detetive:
                role_icon = "👤" if msg["role"] == "user" else "🕵️"
                st.markdown(f"**{role_icon} {msg['role'].capitalize()}:** {msg['content']}")
                if msg["role"] == "assistant": st.markdown("---")

        if prompt := st.chat_input("Diga alguma coisa..."):
            st.session_state.historico_detetive.append({"role": "user", "content": f"Sobre {nome_alvo}: {prompt}"})
            resposta = consultar_ravengar("", api_key=chave_api, setor="Detetive", historico=st.session_state.historico_detetive)
            st.session_state.historico_detetive.append({"role": "assistant", "content": resposta})
            st.rerun()
        
        col_det1, col_det2 = st.columns(2)
        with col_det1:
            if st.session_state.historico_detetive:
                conteudo_bloco = f"INVESTIGAÇÃO: {nome_alvo}\n" + "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.historico_detetive])
                st.download_button("💾 SALVAR NO BLOCO DE NOTAS", data=conteudo_bloco, file_name=f"investigacao_{nome_alvo}.txt", mime="text/plain")
        with col_det2:
            if st.session_state.historico_detetive:
                if st.button("🗑️ RESETAR CONVERSA"):
                    st.session_state.historico_detetive = []
                    st.rerun()

    with tabs[4]: # QUIZ
        if 'quiz_iniciado' not in st.session_state: st.session_state.quiz_iniciado = False
        if not st.session_state.quiz_iniciado:
            st.markdown("<div style='text-align: center; padding: 40px;'><h2>Você acha que se conhece bem? 🤔</h2><h4>Faça o nosso teste e descubra camadas da sua personalidade que você nunca percebeu.</h4></div>", unsafe_allow_html=True)
            if st.button("CLIQUE PARA INICIAR"):
                st.session_state.quiz_iniciado = True; st.session_state.passo = 0; st.session_state.analise = []; st.rerun()
        else:
            g = st.session_state.genero_user
            art, um, guerr, reser = ("o", "um", "guerreiro", "reservado") if g == "Masculino" else ("a", "uma", "guerreira", "reservada")
            perguntas = [
                {"contexto": "Você caminha por uma floresta densa...", "p": "Nesta caminhada, você está:", "o": ["Só", "Com alguém"], "s": {"Só": "Sua essência é de independência.", "Com alguém": "Você valoriza conexões próximas."}},
                {"contexto": "De repente, um animal surge à sua frente.", "p": "Que animal é este?", "o": ["Lobo", "Coelho", "Pássaro"], "s": {"Lobo": f"Sua mente age como {um} {guerr}.", "Coelho": "Sua natureza busca calma.", "Pássaro": "Sua agilidade mental é rara."}},
                {"contexto": "O animal encara você fixamente.", "p": "Qual é a sua reação imediata?", "o": ["Recuar", "Permanecer"], "s": {"Recuar": "Sua inteligência é movida pela cautela.", "Permanecer": "Você não teme o desconhecido."}},
                {"contexto": "A floresta abre-se, revelando uma estrada.", "p": "Como é esta estrada?", "o": ["Asfalto", "Terra"], "s": {"Asfalto": "Você opera com planejamento.", "Terra": "Seu espírito vibra na liberdade."}},
                {"contexto": "Você avista uma casa solitária.", "p": "Como descreveria esta casa?", "o": ["Grande", "Pequena"], "s": {"Grande": "Suas ambições são vastas.", "Pequena": "Sua alma entende o essencial."}},
                {"contexto": "Você aproxima-se da entrada.", "p": "A casa possui uma cerca ao redor?", "o": ["Sim", "Não"], "s": {"Sim": f"Você é {reser}, protegendo seu interior.", "Não": "Você acredita na transparência."}},
                {"contexto": "Você decide entrar. Há uma mesa de jantar na sala.", "p": "Como está esta mesa?", "o": ["Farta", "Vazia"], "s": {"Farta": "Você vive um momento de conexão emocional.", "Vazia": "Você busca algo profundo que ainda não encontrou."}},
                {"contexto": "Você nota uma xícara caída no chão.", "p": "O que você faz ao vê-la?", "o": ["Recolhe", "Ignora"], "s": {"Recolhe": "Você valoriza o que moldou seu passado.", "Ignora": "Seu foco está no horizonte à frente."}},
                {"contexto": "Você observa o material da xícara.", "p": "De que material ela é?", "o": ["Porcelana", "Metal"], "s": {"Porcelana": "Sua visão sobre o afeto é refinada.", "Metal": "Sua lealdade é inquebrável."}},
                {"contexto": "Ao sair, encontra um lago sereno.", "p": "Diante da água, qual sua atitude?", "o": ["Mergulha", "Toca a água", "Contempla"], "s": {"Mergulha": "Você se entrega de corpo e alma nos relacionamentos.", "Toca a água": "Você é uma pessoa equilibrada.", "Contempla": f"Você é {um} observador {reser}."}}
            ]
            if st.session_state.passo < len(perguntas):
                q = perguntas[st.session_state.passo]
                st.info(q['contexto'])
                st.markdown(f"<div class='quiz-pergunta'>{q['p']}</div>", unsafe_allow_html=True)
                cols = st.columns(len(q['o']))
                for i, opt in enumerate(q['o']):
                    if cols[i].button(opt, key=f"qz_{st.session_state.passo}_{i}"):
                        st.session_state.analise.append(q['s'][opt]); st.session_state.passo += 1; st.rerun()
            else:
                st.markdown(f"<div class='ravengar-card'><h3>O Veredito Psicológico de {st.session_state.nome_user}</h3><p>{' '.join(st.session_state.analise)}</p></div>", unsafe_allow_html=True)
                if st.button("REINICIAR JORNADA"): st.session_state.quiz_iniciado = False; st.rerun()

    with tabs[5]: # BIBLIOTECA
        st.markdown("<h2 style='text-align: center;'>🔮 BIBLIOTECA SECRETA</h2>", unsafe_allow_html=True)
        cursos = [
            {"id": "c1", "titulo": "🔮 Leitura Fria: Como Entender Qualquer Pessoa em Segundos", "desc": "Aprenda a interpretar comportamentos, identificar padrões ocultos e compreender o que as pessoas realmente pensam."},
            {"id": "c2", "titulo": "✋ Leitura de Mãos: Descubra o Que Suas Mãos Revelam Sobre Você", "desc": "Aprenda a identificar as principais linhas da mão e interpretar seus significados de forma simples e prática."},
            {"id": "c3", "titulo": "🔢 Numerologia do Nome: Descubra Seu Código Oculto", "desc": "Aprenda a transformar letras em números e interpretar o significado oculto por trás do seu nome."},
            {"id": "c4", "titulo": "🧠 Leitura Psicológica: Descubra Padrões Ocultos da Sua Mente", "desc": "Aprenda a identificar comportamentos inconscientes e reconhecer padrões que influenciam suas decisões."},
            {"id": "c5", "titulo": "❤️ Leitura de Intenção: Descubra o Que as Pessoas Realmente Sentem", "desc": "Aprenda a interpretar sinais sutis, atitudes e comportamentos que revelam o verdadeiro interesse."},
            {"id": "c6", "titulo": "🎯 Simulador de Futuro: Veja Para Onde Suas Decisões Estão Te Levando", "desc": "Aprenda a identificar padrões de comportamento e entender como suas escolhas impactam seu futuro."},
            {"id": "c7", "titulo": "🎁 Desbloqueio da Sorte: Ative Seu Potencial de Oportunidades", "desc": "Aprenda a desenvolver uma mentalidade estratégica para reconhecer e aproveitar oportunidades."}
        ]
        for item in cursos:
            st.markdown(f"<div class='biblioteca-card'><h4>{item['titulo']}</h4><p>{item['desc']}</p></div>", unsafe_allow_html=True)
            if st.button("📥 Baixar PDF", key=item["id"]):
                st.warning(f"**Acesso Liberado:** O material de '{item['titulo']}' está sendo preparado para você.")

    with tabs[6]: # SEU ESPAÇO
        st.markdown("<h2 style='text-align: center;'>🧘 SEU ESPAÇO</h2>", unsafe_allow_html=True)
        st.markdown("### 📰 Radar do Ravengar")
        tema = st.selectbox("Escolha um assunto:", ["Ciência", "Astronomia", "Saúde & Bem-estar", "Relacionamentos", "Tecnologia", "Games", "Esportes", "Cinema & TV"])
        if st.button("BUSCAR NO ÉTER"):
            if chave_api: st.session_state['noticias_dia'] = consultar_ravengar(f"Resuma 3 notícias sobre {tema} com tom místico.", api_key=chave_api, setor="Noticias")
        if 'noticias_dia' in st.session_state: st.markdown(f"<div class='ravengar-card'>{st.session_state['noticias_dia']}</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🃏 Tarot do Dia")
        if st.button("PUXAR CARTA DO DIA"):
            if chave_api:
                cartas = ["O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador", "O Hierofante", "Os Enamorados", "O Carro", "A Justiça", "O Eremita", "A Roda da Fortuna", "A Força", "O Pendurado", "A Morte", "A Temperança", "O Diabo", "A Torre", "A Estrela", "A Lua", "O Sol", "O Julgamento", "O Mundo", "O Louco"]
                carta = random.choice(cartas)
                st.session_state['carta_dia'] = (carta, consultar_ravengar(f"Carta '{carta}'. Veredito curto.", api_key=chave_api, setor="Tarot"))
        if 'carta_dia' in st.session_state:
            st.markdown(f"<div class='ravengar-card' style='text-align: center;'><h2 style='color: #FF69B4;'>{st.session_state['carta_dia'][0]}</h2><p>{st.session_state['carta_dia'][1]}</p></div>", unsafe_allow_html=True)

    with tabs[7]: # ENCONTROS
        st.markdown("<h2 style='text-align: center;'>🤝 ENCONTROS</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 💬 Mural de Almas")
            if not mural_global:
                st.write("*O silêncio ecoa... As sombras aguardam o primeiro registro.*")
            else:
                for m in reversed(mural_global[-15:]):
                    st.markdown(f"<div class='msg-balao'><small><b>{m['usuario']}</b> • {m['hora']}</small><br>{m['texto']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("### ✍️ Manifestar")
            msg_input = st.text_area("O que deseja dizer às sombras?", placeholder="Escreva sua mensagem...")
            if st.button("LANÇAR AO MURAL"):
                if msg_input:
                    mural_global.append({"usuario": st.session_state.nome_user, "texto": msg_input, "hora": datetime.datetime.now().strftime("%H:%M")})
                    st.rerun()
                        
    if st.button("🔄 REINICIAR SESSÃO"):
        st.session_state.clear()
        st.rerun()

    # --- 6. RODAPÉ ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Explorando os mistérios da mente e do destino.<br>"
        "© 2026 Tenda do Ravengar"
        "</div>", 
        unsafe_allow_html=True
    )
