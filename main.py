import streamlit as st
from groq import Groq
import random
import json
import os
from datetime import datetime

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Tenda do Ravengar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    </style>
""", unsafe_allow_html=True)

# --- CURSOS EMBUTIDOS ---
CURSOS = {
  "quiromancia": {
    "titulo": "Quiromancia — A Arte de Ler as Mãos",
    "descricao": "Aprenda a decifrar o mapa da alma humana através das linhas, montes e formas da mão. Um dos sistemas divinatórios mais antigos do mundo, praticado há mais de 5.000 anos.",
    "icone": "✋",
    "total_aulas": 8,
    "aulas": {
      "1": {
        "titulo": "A Mão como Mapa da Alma",
        "conteudo": "A quiromancia — do grego 'kheir' (mão) e 'manteia' (adivinhação) — é uma das práticas divinatórias mais antigas da humanidade. Registros de seu uso datam de mais de 5.000 anos, encontrados em textos hindus, chineses, sumérios e egípcios. A premissa central é poderosa em sua simplicidade: a mão não mente. Enquanto o rosto pode sorrir quando o coração chora, a mão carrega impressa a história real de uma pessoa — seus padrões, suas tendências, suas forças e suas vulnerabilidades.\n\nHá dois conceitos fundamentais que todo estudante de quiromância precisa compreender antes de olhar para qualquer linha. O primeiro é a distinção entre mão dominante e mão recessiva. A mão dominante — aquela com a qual você escreve — revela o que você fez com o potencial que recebeu. É a mão do presente e do futuro construído. A mão recessiva — a outra — revela o que você nasceu sendo, seu potencial original, o que o destino traçou antes que você começasse a agir sobre ele. Quando as linhas das duas mãos diferem muito, isso indica uma pessoa que trabalhou ativamente para transformar sua natureza original. Quando são muito similares, indica alguém que ainda está vivendo dentro dos padrões com que nasceu.\n\nO segundo conceito é que a mão é um sistema vivo. Ao contrário do que muitos pensam, as linhas da mão mudam ao longo do tempo. Novos ramos aparecem, linhas se aprofundam ou enfraquecem, marcas surgem e desaparecem. Isso é documentado em estudos médicos: pessoas que passam por mudanças psicológicas profundas — terapia intensa, traumas, conversões espirituais — frequentemente apresentam alterações visíveis nas linhas dentro de dois a três anos.\n\nExistem quatro tipos básicos de mão, e identificá-los é o primeiro passo de qualquer leitura séria. A mão de Terra tem palma quadrada e dedos curtos — seu portador é prático, estável, confia nos sentidos e na realidade tangível, tende ao conservadorismo e à desconfiança do abstrato. A mão de Ar tem palma quadrada e dedos longos — seu portador é analítico, comunicativo, curioso, mas pode ser frio emocionalmente e excessivamente intelectual. A mão de Água tem palma retangular e dedos longos — seu portador é sensível, criativo, empático, profundamente emocional, mas pode ser instável e facilmente influenciável. A mão de Fogo tem palma retangular e dedos curtos — seu portador é apaixonado, espontâneo, carismático, impulsivo, e frequentemente impaciente.\n\nAntes de qualquer leitura, observe a mão inteira como um todo: sua textura (mãos macias indicam sensibilidade; mãos ásperas indicam pragmatismo), sua flexibilidade (mãos muito flexíveis indicam adaptabilidade mas também falta de firmeza; mãos rígidas indicam determinação mas também teimosia), sua temperatura (mãos frias frequentemente acompanham pessoas que guardam emoções; mãos quentes acompanham pessoas expansivas) e sua cor geral (palidez pode indicar retraimento emocional; vermelhidão intensa pode indicar excesso de paixão ou raiva contida).",
        "exemplo": "Imagine que você encontra duas pessoas com mãos completamente diferentes. A primeira tem palma quadrada, dedos curtos e mão rígida com textura áspera — você já sabe, antes de ver uma única linha, que está diante de alguém prático, desconfiado do abstrato, que precisa ver para crer. A segunda tem palma longa, dedos finos e flexíveis, mão suave e levemente fria — você já percebe uma pessoa sensível, criativa, mas que guarda muito dentro de si. A forma da mão já conta metade da história antes mesmo de você tocar nas linhas.",
        "aplicacao": "1. Peça para a pessoa estender ambas as mãos com a palma para cima, relaxadas. 2. Observe primeiro a forma geral — palma quadrada ou retangular? Dedos curtos ou longos? 3. Classifique o tipo de mão (Terra, Ar, Água ou Fogo). 4. Observe a textura, flexibilidade e temperatura. 5. Compare as duas mãos — são similares ou muito diferentes? 6. Apenas depois dessas observações comece a olhar para as linhas.",
        "exercicio": "Examine sua própria mão agora. Identifique: qual é o tipo da sua mão? A palma é quadrada ou retangular? Os dedos são curtos ou longos? A mão é flexível ou rígida? Fria ou quente? Depois faça o mesmo com a mão de alguém próximo e compare. O que as diferenças dizem sobre vocês dois?",
        "gabarito": "Não existe resposta errada aqui — o objetivo é desenvolver o olhar. Uma mão de Terra com palma quadrada e dedos curtos indica alguém mais prático e concreto. Uma mão de Água com palma longa e dedos finos indica alguém mais sensível e intuitivo. O mais importante é perceber que você já extrai informações antes de ver uma única linha."
      },
      "2": {
        "titulo": "As Três Linhas Principais",
        "conteudo": "Existem dezenas de linhas que podem aparecer na palma da mão, mas três delas são universais — presentes em praticamente todas as mãos humanas — e constituem a espinha dorsal de qualquer leitura quiromântica. São a Linha da Vida, a Linha da Cabeça e a Linha do Coração. Compreendê-las profundamente é mais valioso do que conhecer superficialmente todas as outras dezenas de linhas menores.\n\nA LINHA DA VIDA é a linha que curva ao redor do monte de Vênus (o monte carnoso na base do polegar). Contrariamente ao que o folclore popular diz, ela NÃO prevê quanto tempo você vai viver. Estudos feitos com centenas de pessoas que morreram precocemente mostraram linhas da vida longas; e pessoas que viveram mais de noventa anos foram encontradas com linhas curtas. O que ela realmente revela é a QUALIDADE e a INTENSIDADE da vida — sua vitalidade, energia, resistência física e emocional, e os grandes ciclos e mudanças da vida.\n\nUma linha da vida profunda, clara e bem marcada indica boa vitalidade, resistência e uma vida vivida com intensidade. Uma linha fraca, fragmentada ou com muitas interrupções indica períodos de baixa energia, problemas de saúde recorrentes ou fases de grande instabilidade. Quando a linha faz um arco amplo em direção ao centro da palma, indica uma pessoa expansiva, que ocupa espaço no mundo. Quando fica colada ao polegar com um arco pequeno, indica alguém mais contido, que tende a se retrair.\n\nBifurcações na linha da vida são muito significativas: uma bifurcação no início indica uma infância dividida entre dois mundos ou influências muito diferentes. Uma bifurcação no meio indica uma grande virada — mudança de país, carreira, ou identidade. Uma bifurcação no final indica uma fase de dispersão de energia na velhice ou, em algumas tradições, a possibilidade de dois caminhos igualmente fortes se abrindo.\n\nA LINHA DA CABEÇA começa na mesma região que a linha da vida (entre o polegar e o indicador) e atravessa a palma horizontalmente. Ela revela o estilo de pensamento, a forma como a mente processa a realidade, a capacidade intelectual e a relação entre razão e emoção.\n\nSe a linha da cabeça começa unida à linha da vida por um trecho antes de se separar, indica uma pessoa cautelosa que precisa de segurança antes de agir — quanto mais longo o trecho unido, maior a influência da família e do passado nas decisões. Se começa separada da linha da vida, indica independência, coragem para agir sem precisar de aprovação.\n\nUma linha da cabeça reta indica pensamento lógico, pragmático e linear. Uma linha que desce em direção ao monte da Lua (na parte inferior da palma) indica imaginação fértil, pensamento criativo e poético, mas também tendência ao devaneio. Quanto mais a linha desce, mais pronunciada essa característica.\n\nA LINHA DO CORAÇÃO corre horizontalmente na parte superior da palma, sob os dedos. Ela revela a vida emocional, a capacidade de amar, a forma como a pessoa se relaciona afetivamente e o que ela precisa para se sentir amada.\n\nUma linha do coração que termina sob o dedo indicador indica um amor idealista, que busca a perfeição no parceiro e às vezes ama mais o ideal do que a pessoa real. Que termina sob o dedo médio indica uma pessoa que ama com possessividade e intensidade. Que termina entre os dois indica equilíbrio entre idealismo e realismo.\n\nUma linha profunda e clara indica intensa vida emocional. Uma linha com muitas pequenas ramificações indica que a pessoa já amou muito e com muitas pessoas diferentes. Uma linha encadeada (que parece uma corrente) indica insegurança emocional profunda, dificuldade de confiar.",
        "exemplo": "Imagine uma pessoa cuja linha da cabeça desce acentuadamente em direção à parte inferior da palma, enquanto a linha do coração tem muitas ramificações finas. Você já consegue ler: é uma pessoa de imaginação muito fértil (linha da cabeça descendente), que amou muito e com intensidade em várias ocasiões (ramificações na linha do coração), mas que provavelmente mistura muito amor com fantasia — ama a pessoa que imagina que o outro é tanto quanto ama o que o outro realmente é.",
        "aplicacao": "1. Identifique as três linhas principais. 2. Para cada uma, observe: profundidade (clara ou fraca?), comprimento (longa ou curta?), direção (reta ou curva?), e marcas (bifurcações, interrupções, ilhas). 3. Leia cada linha individualmente. 4. Depois integre as três numa narrativa — como a mente (linha da cabeça) e o coração (linha do coração) se relacionam? A vitalidade (linha da vida) suporta o estilo de vida que a pessoa leva?",
        "exercicio": "Examine as três linhas principais da sua mão dominante. Desenhe-as num papel. Para cada uma, responda: ela é profunda ou fraca? Longa ou curta? Tem interrupções ou bifurcações? Onde termina? Compare com a mão recessiva — o que mudou desde que você nasceu?",
        "gabarito": "O objetivo deste exercício é treinar o olhar para identificar e distinguir as três linhas. A interpretação virá com a prática. O mais importante é perceber que cada linha conta uma história diferente: a vida (vitalidade), a cabeça (mente) e o coração (emoções) — e que essas três histórias precisam ser lidas juntas para fazer sentido."
      },
      "3": {
        "titulo": "Os Montes da Mão",
        "conteudo": "Os montes são as elevações carnosas encontradas na palma da mão. Cada monte corresponde a um planeta da astrologia clássica e revela aspectos específicos da personalidade. Um monte desenvolvido (elevado e firme) indica que as qualidades daquele planeta estão presentes e ativas. Um monte plano ou afundado indica ausência ou repressão dessas qualidades. Um monte excessivamente desenvolvido pode indicar excesso ou compulsão.\n\nO MONTE DE JÚPITER fica na base do dedo indicador. Revela ambição, liderança, espiritualidade e desejo de reconhecimento. Bem desenvolvido: pessoa ambiciosa, com senso de missão, carismática e com vocação para liderar. Plano: falta de ambição, dificuldade de assumir responsabilidades. Excessivo: arrogância, necessidade compulsiva de poder e reconhecimento.\n\nO MONTE DE SATURNO fica na base do dedo médio. Revela prudência, seriedade, responsabilidade e capacidade de suportar dificuldades. Bem desenvolvido: pessoa séria, confiável, disciplinada, com profunda consciência moral. Plano: irresponsabilidade, fuga das consequências. Excessivo: pessimismo crônico, tendência à depressão e ao isolamento.\n\nO MONTE DE APOLO (ou Sol) fica na base do dedo anelar. Revela criatividade, gosto estético, desejo de brilhar e amor pela beleza. Bem desenvolvido: pessoa criativa, com bom gosto, que tem facilidade de ser amada e admirada. Plano: falta de criatividade, dificuldade de expressar-se. Excessivo: vaidade, necessidade excessiva de atenção e admiração.\n\nO MONTE DE MERCÚRIO fica na base do dedo mínimo. Revela comunicação, inteligência, capacidade de negociação e habilidade com palavras e negócios. Bem desenvolvido: pessoa eloquente, inteligente, boa negociadora. Plano: dificuldade de comunicação, timidez. Excessivo: tendência à desonestidade, manipulação através das palavras.\n\nO MONTE DE VÊNUS fica na base do polegar, circundado pela linha da vida. Revela capacidade de amar, sensualidade, vitalidade física e amor pela vida. Bem desenvolvido: pessoa amorosa, sensual, cheia de vida e energia. Plano: frieza emocional, baixa libido, dificuldade de se conectar. Excessivo: sensualidade compulsiva, excesso de paixões.\n\nO MONTE DA LUA fica na parte inferior da palma, no lado oposto ao polegar. Revela imaginação, intuição, espiritualidade e conexão com o inconsciente. Bem desenvolvido: pessoa intuitiva, criativa, com rica vida interior e tendência ao misticismo. Plano: falta de imaginação, excesso de materialismo. Excessivo: tendência a fugir da realidade, fantasias excessivas.\n\nO MONTE DE MARTE se divide em dois: Marte Positivo (entre o polegar e o monte de Júpiter) e Marte Negativo (na parte lateral da palma, entre o monte da Lua e o monte de Mercúrio). Juntos revelam coragem, resistência, capacidade de luta e controle emocional sob pressão.",
        "exemplo": "Uma mão com monte de Vênus muito desenvolvido, monte de Apolo proeminente e monte da Lua elevado descreve uma pessoa apaixonada e sensual (Vênus), criativa e que ama a beleza (Apolo), com forte vida interior e intuição aguçada (Lua). Se o monte de Saturno for plano nessa mesma mão, você tem alguém que vive intensamente mas com dificuldade de colocar limites e assumir responsabilidades práticas.",
        "aplicacao": "1. Observe cada monte individualmente, pressionando suavemente para sentir se é firme, mole ou plano. 2. Classifique cada um: desenvolvido, plano ou excessivo. 3. Identifique os dois ou três montes mais proeminentes — eles revelam as energias dominantes da pessoa. 4. Integre essa leitura com as linhas já estudadas.",
        "exercicio": "Observe os montes da sua mão. Quais são os dois mais desenvolvidos? Quais são os mais planos? Escreva uma frase sobre o que isso diz sobre você. Depois compare com alguém próximo.",
        "gabarito": "Os dois montes mais desenvolvidos revelam as forças dominantes da personalidade. Os mais planos revelam áreas de menor desenvolvimento ou pontos de crescimento. Não existe combinação perfeita — cada configuração tem pontos fortes e desafios."
      },
      "4": {
        "titulo": "As Linhas Secundárias",
        "conteudo": "Além das três linhas principais, existem linhas secundárias que aprofundam a leitura de forma significativa. As mais importantes são a Linha do Destino, a Linha do Sol, a Linha do Mercúrio e as Linhas de Afeto.\n\nA LINHA DO DESTINO (ou Linha de Saturno) sobe verticalmente pelo centro da palma em direção ao dedo médio. Ela não está presente em todas as mãos — e isso por si só já é uma informação. Quando ausente, indica uma pessoa que escreve seu próprio caminho sem um destino claramente definido, vivendo por impulso e escolhas momentâneas. Quando presente, indica que a pessoa tem um senso de missão ou direção, que sua vida segue um fio condutor reconhecível.\n\nO ponto de origem da linha do destino é crucial: quando começa na base da palma (perto do pulso), indica que o senso de propósito é precoce e vem de dentro. Quando começa na linha da vida, indica que a carreira ou missão foi fortemente moldada pela família. Quando começa no monte da Lua, indica uma carreira ou direção que depende do público, da aprovação alheia ou de colaborações — comum em artistas, políticos e professores.\n\nInterrupções na linha do destino indicam mudanças significativas de direção na vida. Uma linha que termina antes de chegar ao dedo médio indica que a pessoa para de seguir seu destino em algum momento — por escolha, medo ou circunstâncias.\n\nA LINHA DO SOL (ou Linha de Apolo) sobe em direção ao dedo anelar. Indica sucesso, reconhecimento, talento criativo e capacidade de brilhar publicamente. Quando presente e clara, indica que a pessoa tem potencial para ser reconhecida e admirada em sua área. Quando ausente, não significa fracasso — apenas que o sucesso virá de forma mais privada, sem reconhecimento público amplo.\n\nAs LINHAS DE AFETO (ou Linhas de União) são as linhas horizontais que aparecem na lateral da mão, abaixo do dedo mínimo. Cada linha marcada pode indicar um relacionamento significativo. O que importa não é a quantidade, mas a qualidade: uma linha profunda e clara indica um relacionamento duradouro e profundo; uma linha fraca ou fragmentada indica uma relação que começou mas não se consolidou; uma bifurcação no início pode indicar dificuldade para comprometer-se; uma bifurcação no final pode indicar separação.\n\nA LINHA DE MERCÚRIO (ou Linha de Saúde) desce diagonalmente do monte de Mercúrio em direção à base da palma. Paradoxalmente, quanto mais fraca ou ausente essa linha, melhor — indica saúde robusta e estável. Quando presente e marcada, pode indicar sensibilidade do sistema nervoso ou digestivo, ou uma mente que trabalha intensamente e precisa de mais cuidado com o corpo.",
        "exemplo": "Uma pessoa com linha do destino saindo do monte da Lua, linha do Sol presente e forte, e linhas de afeto com bifurcações no final tem uma história bastante legível: é alguém cuja carreira depende do público (monte da Lua), que tem talento reconhecido (linha do Sol), mas cujos relacionamentos tendem a chegar a crises ou separações (bifurcações nas linhas de afeto).",
        "aplicacao": "1. Procure a linha do destino — ela existe? De onde parte? Tem interrupções? 2. Procure a linha do Sol — está presente? É forte ou fraca? 3. Observe as linhas de afeto na lateral da mão — quantas são marcadas? Qual é a qualidade de cada uma? 4. Integre tudo numa leitura única.",
        "exercicio": "Examine se você tem linha do destino. Se sim, de onde ela parte? Isso ressoa com sua experiência de vida — você sente que tem um propósito claro? Se não tem a linha, isso também faz sentido para você?",
        "gabarito": "A ausência da linha do destino não é negativa — indica liberdade e fluidez. A presença indica senso de missão. O objetivo é sempre verificar se a leitura ressoa com a experiência real da pessoa."
      },
      "5": {
        "titulo": "Os Dedos e suas Falanges",
        "conteudo": "Os dedos são uma dimensão muitas vezes negligenciada da quiromância, mas revelam aspectos da personalidade tão importantes quanto as linhas. Cada dedo corresponde a um planeta e a uma área da vida, e cada falange (segmento do dedo) revela um nível diferente de expressão dessa energia.\n\nO POLEGAR revela força de vontade e lógica — a capacidade de transformar intenção em ação. Um polegar longo indica grande determinação e lógica forte. Um polegar curto indica impulsividade e dificuldade de sustentar esforços prolongados. Um polegar muito rígido indica teimosia e inflexibilidade. Um polegar muito flexível (que dobra muito para trás) indica adaptabilidade e generosidade, mas também facilidade para ceder demais.\n\nO INDICADOR (Júpiter) revela ambição, autoconfiança e relação com a autoridade. Quando é mais longo que o anelar, indica uma personalidade dominante, com forte necessidade de liderança e controle. Quando é mais curto que o anelar, indica introversão e tendência a deixar os outros liderarem.\n\nO DEDO MÉDIO (Saturno) revela equilíbrio, responsabilidade e senso de dever. É sempre o mais longo — quando é desproporcional mente longo em relação aos outros, indica uma personalidade séria e introspectiva em excesso. Quando é quase do mesmo tamanho que os vizinhos, indica alguém que não se leva demasiadamente a sério.\n\nO ANELAR (Apolo) revela criatividade, senso estético e necessidade de reconhecimento. Quando é mais longo que o indicador, indica uma personalidade criativa, voltada para as artes e para a expressão pessoal, que valoriza mais criar do que liderar. Homens com anelar mais longo que o indicador foram estudados em pesquisas que os associam a maior exposição a testosterona no útero e a personalidades mais assertivas e competitivas.\n\nO MÍNIMO (Mercúrio) revela comunicação, inteligência e habilidade social. Um dedo mínimo longo (que ultrapassa a primeira articulação do anelar) indica eloquência, habilidade com palavras e facilidade de convencer. Um mínimo curto pode indicar dificuldade de expressão verbal ou timidez social.\n\nAs FALANGES de cada dedo dividem-se em três: a superior (ponta do dedo) representa o aspecto mental ou espiritual daquela energia; a média representa o aspecto prático; e a inferior (próxima à palma) representa o aspecto material ou instintivo. Uma falange mais desenvolvida (mais carnuda ou longa) indica que aquele nível é dominante.",
        "exemplo": "Uma pessoa com polegar longo e rígido, indicador mais longo que o anelar e dedo mínimo comprido tem um perfil bastante definido: forte vontade e lógica (polegar longo), personalidade dominante que precisa liderar (indicador comprido), e grande facilidade de comunicação e persuasão (mínimo longo). É o perfil clássico de um líder nato com habilidade para convencer e executar.",
        "aplicacao": "1. Compare o comprimento dos dedos entre si. 2. Observe a flexibilidade do polegar. 3. Compare indicador e anelar — qual é maior? 4. Observe o comprimento do mínimo em relação ao anelar. 5. Para cada dedo, observe qual das três falanges é mais desenvolvida.",
        "exercicio": "Olhe para seus dedos agora. Indicador ou anelar — qual é maior? O que isso diz sobre você? Seu polegar é rígido ou flexível? Isso ressoa com sua forma de ser?",
        "gabarito": "Não existe combinação de dedos melhor que outra — cada configuração tem virtudes e desafios. O objetivo é reconhecer padrões e usá-los para compreender melhor a si mesmo e às pessoas ao redor."
      },
      "6": {
        "titulo": "Marcas Especiais na Mão",
        "conteudo": "Além das linhas e montes, existem marcas especiais que aparecem na palma e nos dedos, cada uma com significado específico. Conhecê-las aprofunda enormemente a leitura.\n\nO ANEL DE SALOMÃO é um arco ou linha que aparece na base do dedo indicador, circundando o monte de Júpiter. É uma das marcas mais valorizadas na quiromância — indica sabedoria, capacidade de liderança espiritual, tendência natural para o ensino e uma profunda intuição sobre as pessoas. Pessoas com esse anel raramente conseguem ser enganadas por muito tempo.\n\nO ANEL DE SATURNO é uma linha que circunda a base do dedo médio. Ao contrário do Anel de Salomão, é considerado uma marca desafiadora — indica tendência ao isolamento, dificuldade de se conectar com os outros, e em casos extremos, uma tendência à melancolia profunda.\n\nA CRUZ MÍSTICA aparece no centro da palma, na área chamada quadrângulo (entre as linhas da cabeça e do coração), sem tocar em nenhuma das linhas principais. É uma das marcas mais raras e valorizadas — indica forte intuição, interesse genuíno pelo oculto e místico, e frequentemente aparece em pessoas com dons mediúnicos ou grande sensibilidade espiritual.\n\nO TRIÂNGULO formado pelo encontro de três linhas em qualquer parte da mão é considerado uma marca de talento e proteção naquela área específica. Um triângulo sobre o monte de Mercúrio indica talento para negócios e comunicação. Sobre o monte de Apolo, talento artístico protegido.\n\nA ESTRELA é um conjunto de pequenas linhas que se cruzam formando uma estrela em qualquer ponto da mão. Sobre os montes, geralmente indica um evento súbito e poderoso relacionado àquele planeta — pode ser positivo ou negativo dependendo do contexto. Uma estrela sobre a linha da vida pode indicar um evento físico intenso.\n\nAS ILHAS são pequenas formações ovais dentro de uma linha, onde a linha se divide e depois se une novamente. Em qualquer linha que apareçam, indicam um período de dispersão, confusão ou dupla influência. Na linha da cabeça, podem indicar períodos de confusão mental ou problemas nervosos. Na linha do coração, períodos de conflito emocional.\n\nAS GRADES são conjuntos de linhas que se cruzam formando uma grade sobre um monte. Geralmente indicam bloqueio ou excesso de energia naquele monte — a energia existe mas está travada ou sendo mal direcionada.",
        "exemplo": "Uma pessoa com Anel de Salomão no indicador e Cruz Mística no centro da palma é alguém com marcas raras que indicam forte intuição humana (Anel de Salomão) e genuína sensibilidade para o oculto e espiritual (Cruz Mística). Se essa pessoa também tiver o monte da Lua bem desenvolvido, você está diante de alguém com capacidades mediúnicas ou intuitivas fora do comum.",
        "aplicacao": "1. Examine o centro da palma com boa iluminação — existe uma Cruz Mística? 2. Observe a base de cada dedo — há linhas circulares? 3. Procure triângulos formados pela confluência de linhas. 4. Observe se existem ilhas nas linhas principais.",
        "exercicio": "Com boa iluminação e uma lupa se necessário, examine sua mão em busca de marcas especiais. Anote todas que encontrar. Alguma ressoa com o que você sabe sobre si mesmo?",
        "gabarito": "As marcas especiais adicionam nuance à leitura. A Cruz Mística é a mais significativa para quem estuda o misticismo. O Anel de Salomão é muito valorizado. Lembre: marcas isoladas nunca contam a história completa — precisam ser integradas ao resto da leitura."
      },
      "7": {
        "titulo": "Leitura Integrada — Juntando Tudo",
        "conteudo": "Uma leitura quiromântica completa não é uma soma de partes isoladas — é uma narrativa integrada onde cada elemento confirma, contradiz ou enriquece os outros. O leitor experiente não lê linha por linha como um checklist; ele olha para a mão como um todo e deixa uma história emergir.\n\nO processo de uma leitura integrada começa com a impressão geral: qual é o primeiro sentimento que a mão transmite? Há harmonia entre os elementos ou existe tensão visível — como uma linha do coração profunda e intensa combinada com uma linha da cabeça muito racional e reta, indicando uma guerra interna entre coração e razão?\n\nDepois vêm os elementos dominantes: quais são os dois ou três aspectos mais proeminentes? Um monte de Vênus exuberante com linhas de afeto fragmentadas conta uma história muito específica — alguém com enorme capacidade de amar, mas cuja história amorosa foi marcada por rupturas e recomeços.\n\nEm seguida, as contradições internas: onde a mão mostra tensão? Uma linha da cabeça que desce muito (imaginação fértil) combinada com linha do destino partindo do monte da Lua (carreira dependente do público) e monte de Mercúrio desenvolvido (comunicação) aponta para um escritor, roteirista ou poeta — alguém que usa a imaginação para se comunicar com muitas pessoas.\n\nFinalmente, a questão do crescimento: o que a mão recessiva mostra de diferente da dominante? Essas diferenças revelam o trabalho que a pessoa fez sobre si mesma — ou deixou de fazer.\n\nAlguns princípios importantes para a leitura integrada: nunca faça previsões absolutas — sempre use linguagem de tendência ('isso sugere', 'há uma inclinação para'). Nunca assuste — informações sobre saúde ou eventos negativos devem ser comunicados com cuidado e acompanhados de possibilidades de ação. Sempre confirme com a pessoa — a leitura é um diálogo, não um monólogo. E nunca esqueça: a mão mostra tendências, não fatalidades. O livre-arbítrio existe e as linhas mudam.",
        "exemplo": "Imagine uma mão com: tipo Água (palma longa, dedos finos), monte da Lua muito desenvolvido, linha da cabeça descendente, linha do coração com muitas ramificações, linha do destino partindo do monte da Lua, Anel de Salomão no indicador. A narrativa integrada: pessoa profundamente sensível e imaginativa (tipo Água + monte da Lua + linha da cabeça descendente), que amou muito e de formas variadas (linha do coração com ramificações), cuja missão de vida envolve conectar-se com o público através da sensibilidade e intuição (linha do destino do monte da Lua), com profunda sabedoria sobre as pessoas (Anel de Salomão). Provavelmente um artista, terapeuta ou professor.",
        "aplicacao": "1. Observe a mão inteira por 30 segundos sem analisar nada. Que impressão geral você tem? 2. Identifique os 3 elementos mais proeminentes. 3. Identifique as possíveis contradições internas. 4. Compare as duas mãos. 5. Monte uma narrativa coerente. 6. Valide com a pessoa.",
        "exercicio": "Faça uma leitura completa da sua própria mão, seguindo os passos acima. Escreva um parágrafo — não uma lista — descrevendo quem você é com base no que vê. Compare com o que você sabe sobre si mesmo.",
        "gabarito": "Uma boa leitura integrada soa como alguém que conhece a pessoa há anos. Ela não lista características — ela conta uma história. O objetivo deste exercício é desenvolver exatamente essa capacidade narrativa."
      },
      "8": {
        "titulo": "Ética e Prática na Quiromância",
        "conteudo": "Aprender a ler mãos é adquirir uma responsabilidade. Quando você olha para a mão de alguém e começa a falar sobre sua vida, sua personalidade e seus padrões, você está entrando em território íntimo. A pessoa à sua frente pode estar vulnerável, em busca de respostas, ou simplesmente curiosa — mas em qualquer caso, suas palavras terão peso.\n\nO primeiro princípio ético é a não-maleficência: nunca provoque medo desnecessário. Se você vê marcas que poderiam ser interpretadas negativamente, sempre as enquadre em possibilidades e não em fatalidades, e sempre acompanhe com o que pode ser feito. 'Há uma tendência a períodos de baixa energia que merecem atenção ao cuidado do corpo' é muito diferente de 'você vai ter problemas de saúde graves'.\n\nO segundo princípio é a honestidade sobre seus limites: você é um estudante de quiromância, não um oráculo infalível. Dizer 'isso sugere uma tendência para...' ou 'o que vejo aqui pode indicar...' é mais honesto e mais eficaz do que afirmações absolutas.\n\nO terceiro princípio é o respeito à autonomia: a leitura deve empoderar, não criar dependência. O objetivo de uma boa leitura quiromântica é que a pessoa saia com mais clareza sobre si mesma, não com medo de seu destino ou com necessidade de voltar toda semana para saber o que fazer.\n\nO quarto princípio é a confidencialidade: o que você vê nas mãos de alguém é informação privada. Não compartilhe detalhes de uma leitura com terceiros sem permissão.\n\nFinalmente, o desenvolvimento do leitor: a quiromância é uma arte que se desenvolve com prática. Leia o máximo de mãos que puder — de pessoas que você conhece bem, para poder verificar se sua leitura ressoa. Mantenha um diário de leituras. Revisite suas interpretações. E nunca pare de estudar.",
        "exemplo": "Uma pessoa chega até você preocupada com seu relacionamento. Você vê linhas de afeto fragmentadas e uma linha do coração com ilhas. Em vez de dizer 'seu relacionamento vai terminar', você pode dizer: 'Vejo que você passou por períodos de confusão emocional nos relacionamentos — há uma tendência a entrar em fases de indecisão. O que você está sentindo agora sobre essa relação?' Isso abre um diálogo útil sem criar profecia autocumprida.",
        "aplicacao": "1. Sempre peça permissão antes de fazer uma leitura. 2. Nunca faça leituras de pessoas em estado emocional muito fragilizado sem cuidado redobrado. 3. Use sempre linguagem de tendência, nunca de certeza. 4. Finalize toda leitura com algo que empodere a pessoa. 5. Mantenha um diário de leituras para seu desenvolvimento.",
        "exercicio": "Pratique fazer uma leitura completa de alguém que você conhece bem. Depois pergunte à pessoa se o que você disse ressoou. Anote o que acertou e o que não acertou. Esse feedback é o maior professor.",
        "gabarito": "A ética na quiromância não é uma limitação — é o que separa um leitor genuíno de alguém que usa o misticismo para manipular ou assustar. O leitor ético usa seu conhecimento para iluminar, não para impressionar."
      }
    }
  },
  "leitura_fria": {
    "titulo": "Leitura Fria — A Arte de Ler Pessoas",
    "descricao": "Aprenda a extrair informações precisas sobre qualquer pessoa usando apenas observação, linguagem estratégica e conhecimento de psicologia humana. A técnica usada por médiuns, mentalistas e grandes líderes.",
    "icone": "🧊",
    "total_aulas": 8,
    "aulas": {
      "1": {
        "titulo": "O que é Leitura Fria — e o que não é",
        "conteudo": "Leitura fria é a capacidade de fazer afirmações precisas sobre uma pessoa desconhecida usando apenas observação, raciocínio dedutivo, conhecimento de psicologia humana e linguagem estrategicamente escolhida — sem qualquer informação prévia sobre ela. O nome vem do inglês 'cold reading': ler alguém 'a frio', sem aquecimento prévio de informações.\n\nAntes de tudo, é crucial entender o que a leitura fria NÃO é. Ela não é telepatia, clarividência ou dom sobrenatural. Ela é uma habilidade aprendível, baseada em princípios psicológicos documentados e em observação treinada. Isso não diminui seu poder — ao contrário, significa que qualquer pessoa suficientemente dedicada pode desenvolvê-la.\n\nA leitura fria é usada em contextos muito diversos: médiuns e videntes a usam (conscientemente ou não) para criar a impressão de acesso sobrenatural. Negociadores e advogados a usam para entender rapidamente com quem estão lidando. Médicos e psicólogos a usam para captar sinais que o paciente não verbaliza. Grandes vendedores a usam para adaptar sua abordagem em tempo real.\n\nOs pilares da leitura fria são quatro. O primeiro é a OBSERVAÇÃO: você coleta dados visuais antes de dizer qualquer palavra — aparência, postura, roupas, acessórios, mãos, rosto, forma de se mover. O segundo é o CONHECIMENTO ESTATÍSTICO: saber o que é verdade para a maioria das pessoas em determinado contexto permite fazer afirmações com alta probabilidade de acerto. O terceiro é a LINGUAGEM ESTRATÉGICA: a forma como você formula uma afirmação determina se ela será aceita ou rejeitada, independente de seu conteúdo. O quarto é a LEITURA DE REAÇÕES: você monitora continuamente como a pessoa responde ao que você diz, e ajusta sua leitura em tempo real.\n\nO efeito Barnum ou efeito Forer é o fenômeno psicológico central que explica parte do funcionamento da leitura fria. Em 1948, o psicólogo Bertram Forer deu a seus alunos um teste de personalidade e depois entregou a cada um um 'resultado personalizado'. Na verdade, todos receberam exatamente o mesmo texto — uma série de afirmações vagas e positivas. Quando pediu que avaliassem a precisão do resultado numa escala de 0 a 5, a média foi 4,26. O texto era composto por afirmações como 'Você tem necessidade de ser apreciado pelos outros' e 'Embora tenha algumas fraquezas, você geralmente é capaz de compensá-las'. Essas afirmações parecem pessoais mas se aplicam a praticamente todo ser humano.",
        "exemplo": "Um praticante experiente de leitura fria observa uma mulher que chega para uma consulta. Em 30 segundos, ele nota: ela usa aliança mas toca nela nervosamente (casamento com tensão), tem olheiras mas está bem maquiada (cansada mas se esforça para parecer bem), carrega uma agenda de papel em vez de usar o celular para anotações (organizada, valoriza o tangível), e tem uma pequena cicatriz no pulso que ela não esconde (passou por algo difícil e não tem vergonha disso). Antes de ela dizer uma palavra, ele já tem um esboço de quem ela é.",
        "aplicacao": "1. Antes de qualquer interação, pause e observe por 30 segundos sem falar. 2. Liste mentalmente 5 observações concretas. 3. Para cada observação, pergunte: o que isso provavelmente indica? 4. Formule hipóteses, não certezas. 5. Prepare-se para testar e ajustar.",
        "exercicio": "Vá a um lugar público (café, shopping, parque) e escolha uma pessoa que não te conheça. Observe por 2 minutos sem interagir. Escreva 10 observações e para cada uma, uma hipótese sobre essa pessoa. O objetivo não é acertar tudo — é treinar o olhar.",
        "gabarito": "Boas observações são específicas ('ela toca o anel nervosamente') e não vagas ('ela parece nervosa'). Boas hipóteses são baseadas na observação ('tensão no casamento?') e não em preconceitos. O treino está em separar o que você VÊ do que você IMAGINA."
      },
      "2": {
        "titulo": "A Arte das Afirmações Estratégicas",
        "conteudo": "Uma das ferramentas mais poderosas da leitura fria é a capacidade de formular afirmações que parecem específicas mas têm alta probabilidade de acerto. Existem várias técnicas para isso, e conhecê-las serve tanto para quem pratica leitura fria quanto para quem quer reconhecer quando alguém está usando essas técnicas nele.\n\nAs AFIRMAÇÕES BARNUM são declarações que parecem pessoais mas se aplicam à maioria das pessoas. 'Você às vezes se questiona se está no caminho certo' — isso é verdade para mais de 90% dos adultos. 'Há uma parte de você que as pessoas ao seu redor raramente conhecem' — também universal. 'Você tem uma capacidade maior do que a que costuma mostrar' — quase todo mundo concorda. O segredo é entregar essas afirmações com confiança e tom pessoal, como se você estivesse revelando algo específico sobre aquela pessoa.\n\nAs AFIRMAÇÕES DE ESPELHO são aquelas que cobrem os dois lados de uma característica ao mesmo tempo. 'Você pode ser muito generoso, mas também sabe quando precisa proteger o que é seu' — seja lá como a pessoa for, ela vai concordar com alguma parte disso. 'Você tem uma sensibilidade que nem sempre mostra, mas que as pessoas próximas a você percebem' — cobre tanto os extrovertidos (que escondem a sensibilidade) quanto os introvertidos (que a mostram apenas para poucos).\n\nAs AFIRMAÇÕES ESTATÍSTICAS são baseadas no conhecimento de probabilidades. Se a pessoa é mulher entre 30 e 50 anos, há alta probabilidade de que ela se preocupe com relacionamentos, com a saúde de familiares próximos, e com a questão de estar realizando seu potencial. Se é um homem de meia-idade, há alta probabilidade de que ele se preocupe com trabalho, com reconhecimento profissional e com questões financeiras. Essas são probabilidades — não certezas — mas funcionam como ponto de partida.\n\nA TÉCNICA DO JACKPOT é quando você faz uma série de afirmações em sequência, monitorando as reações, e quando percebe que uma acertou em cheio (a pessoa reage visivelmente), você aprofunda aquela linha e abandona as outras. É como uma pessoa procurando um sinal de rádio: quando encontra a frequência certa, para de girar o dial e aumenta o volume.\n\nA TÉCNICA DA AFIRMAÇÃO SUAVE é formular afirmações de forma que qualquer resposta — positiva ou negativa — se encaixe. 'Vejo uma figura masculina importante em sua vida, alguém que foi uma influência significativa...' Se a pessoa confirma, você continua nessa direção. Se ela diz 'não tenho pai', você diz 'às vezes essa figura pode ser um tio, um professor, ou mesmo uma ausência que deixou marca'. A afirmação era vaga o suficiente para se adaptar a qualquer cenário.",
        "exemplo": "Um praticante diz para uma mulher: 'Vejo que você tem uma força que as pessoas ao seu redor às vezes não percebem — você cuida de todos mas raramente pede ajuda.' A mulher fica emocionada e concorda. Isso funcionou porque é estatisticamente muito comum em mulheres de meia-idade, especialmente as que procuram consultas místicas — elas tendem a ser cuidadoras. A afirmação pareceu específica mas era estatisticamente provável.",
        "aplicacao": "1. Comece com afirmações Barnum para criar rapport. 2. Observe as reações e identifique onde há ressonância. 3. Quando encontrar um ponto de ressonância (a pessoa reage com emoção ou entusiasmo), aprofunde. 4. Use afirmações de espelho em áreas onde você não tem certeza. 5. Sempre ancore suas afirmações em observações reais.",
        "exercicio": "Escreva 5 afirmações Barnum — afirmações que parecem pessoais mas se aplicam à maioria. Depois teste-as com alguém próximo. Observe a reação. Isso vai te mostrar como funciona o efeito Barnum na prática.",
        "gabarito": "Boas afirmações Barnum são positivas ou neutras (nunca negativas), parecem específicas mas são amplas, e falam sobre características universais como ambição, sensibilidade, dualidade e capacidade não revelada. 'Você tem uma criatividade que nem sempre encontra espaço de expressão' é um exemplo clássico."
      },
      "3": {
        "titulo": "Leitura de Linguagem Corporal para Leitura Fria",
        "conteudo": "A linguagem corporal fornece à leitura fria uma camada de dados em tempo real que vai muito além das afirmações estatísticas. Quando você combina observação corporal com afirmações estratégicas, a precisão da leitura aumenta dramaticamente.\n\nA POSTURA revela o estado emocional de base da pessoa. Ombros para frente e cabeça levemente abaixada indicam defensividade ou baixa autoestima. Ombros para trás e queixo levemente erguido indicam confiança ou necessidade de projetar confiança. Uma pessoa que senta na ponta da cadeira está ansiosa ou muito engajada. Uma pessoa que senta bem encostada está relaxada ou indiferente.\n\nOs MICROGESTOS são movimentos involuntários que duram menos de um quinto de segundo e revelam emoções reais antes que a pessoa possa mascarar. O mais conhecido é a microexpressão facial — um flash de emoção genuína que aparece e desaparece antes do rosto assumir a expressão controlada. Outras microexpressões incluem: toque no nariz (pode indicar desconforto com o que está sendo dito), toque nos lábios (contenção de palavra), cruzar os braços (fechamento ou desconforto), piscar mais que o normal (estresse ou processamento de informação intensa).\n\nOS OLHOS são particularmente ricos em informação. O contato visual sustentado indica confiança ou domínio. Olhos que evitam contato indicam timidez, vergonha, ou em alguns contextos, mentira. Pupilas dilatadas indicam interesse genuíno ou excitação. Olhos que se movem para cima e para a esquerda (em pessoas destras) frequentemente acompanham a recuperação de uma memória visual real. Olhos que se movem para cima e para a direita frequentemente acompanham a construção de uma imagem — o que pode indicar imaginação ou construção de mentira.\n\nA VOZ fornece informação independente das palavras. Uma voz que sobe ao final de afirmações (como se fossem perguntas) indica insegurança. Uma voz que oscila em volume indica instabilidade emocional. Falar muito rápido indica ansiedade. Pausas longas antes de responder podem indicar cuidado ou, em alguns contextos, construção de resposta.\n\nAs ROUPAS e ACESSÓRIOS são dados ricos e frequentemente negligenciados. Roupas muito combinadas e impecáveis indicam necessidade de controle e boa impressão. Roupas confortáveis mas descuidadas indicam que a pessoa está em modo de autopreservação ou não se importa com opinião alheia neste momento. Acessórios muitos (anéis, pulseiras, colares) indicam expressividade e necessidade de adorno. Poucos acessórios indicam minimalismo ou praticidade.",
        "exemplo": "Uma pessoa entra numa sala com ombros levemente curvados, cruza os braços assim que senta, mas sorri amplamente ao ser cumprimentada. Leitura integrada: ela está defensiva ou vulnerável (postura), mas quer parecer aberta e receptiva (sorriso). Há uma tensão entre o que sente e o que quer projetar. Uma boa afirmação de abertura: 'Sinto que você carrega algo que não tem sido fácil de mostrar para os outros.'",
        "aplicacao": "1. Antes de começar qualquer leitura ou interação, observe postura e acessórios. 2. Durante a interação, monitore microgestos — especialmente toque no rosto e movimento dos olhos. 3. Ouça o tom de voz independente das palavras. 4. Quando perceber discrepância entre o que a pessoa diz e como o corpo reage, confie mais no corpo.",
        "exercicio": "Assista a 10 minutos de uma entrevista em vídeo sem som. Tente ler apenas a linguagem corporal do entrevistado. O que você percebe? Depois assista com som e compare.",
        "gabarito": "A linguagem corporal nunca deve ser lida em gestos isolados — sempre em clusters (grupos de gestos). Um braço cruzado sozinho pode ser frio. Braços cruzados + ombros retraídos + pouco contato visual formam um cluster de fechamento emocional."
      },
      "4": {
        "titulo": "O Feedback Loop — Ajustando a Leitura em Tempo Real",
        "conteudo": "A diferença entre um iniciante e um praticante experiente de leitura fria não está no que eles dizem — está em como eles ouvem e ajustam. A leitura fria não é um monólogo; é um diálogo altamente calibrado onde cada resposta da outra pessoa fornece informação para a próxima afirmação.\n\nO FEEDBACK POSITIVO é quando a pessoa confirma, concorda ou reage com emoção ao que você disse. Pode ser verbal ('sim, exatamente!') ou não-verbal (aceno de cabeça, olhos que se iluminam, postura que se abre). Quando isso acontece, você encontrou um ponto de ressonância — aprofunde imediatamente essa linha.\n\nO FEEDBACK NEGATIVO é quando a pessoa nega, questiona ou reage com frieza. Um praticante inexperiente para aqui. Um experiente nunca abandona uma afirmação de forma abrupta — ele a reformula: 'Talvez isso ainda não tenha se manifestado completamente, mas pode estar por vir' ou 'Talvez seja algo que você sente mas não reconhece conscientemente ainda'.\n\nO FEEDBACK NEUTRO é o mais desafiador — quando a pessoa não reage de forma clara. Nesse caso, use uma pergunta aberta para extrair informação: 'O que isso te faz pensar?' ou 'Isso ressoa com algo que você está vivendo agora?'\n\nA técnica do HOT READING — que não deve ser confundida com leitura fria — é quando o praticante obtém informações sobre a pessoa ANTES da sessão. Médiuns desonestos frequentemente usam assistentes que conversam com os visitantes na sala de espera. Na versão legítima, qualquer informação que você já tenha sobre a pessoa é apenas contexto — o que você faz com ela durante a sessão ainda é leitura fria.\n\nO EFEITO ÉLVIS é quando a pessoa começa a fornecer informações voluntariamente, empolgada com a leitura. Ela passa de receptor passivo para colaborador ativo — e frequentemente fornece exatamente as informações que confirmam e aprofundam a leitura. O praticante experiente sabe que, nesse momento, precisa escutar mais do que falar.\n\nA ARMADILHA DO EGO é o maior inimigo do praticante: quando você está tão focado em impressionar que para de ouvir. As melhores leituras acontecem quando o praticante está completamente presente e responsivo, não quando está ensaiando mentalmente a próxima afirmação impressionante.",
        "exemplo": "Você diz: 'Vejo que há uma figura feminina importante em sua vida que partiu cedo demais.' A pessoa franze a testa e diz: 'Não perdi ninguém assim.' Um praticante experiente não recua — ele reformula: 'Às vezes essa partida não é física — pode ser uma distância, uma ruptura, uma separação que aconteceu antes que estivesse pronta.' Se a pessoa reflete e diz 'minha mãe se foi quando eu tinha 12 anos mas ainda está viva, simplesmente sumiu da minha vida', você encontrou o ponto.",
        "aplicacao": "1. Após cada afirmação, pause e observe a reação ANTES de continuar. 2. Classifique a reação: positiva, negativa ou neutra. 3. Positiva: aprofunde. Negativa: reformule. Neutra: faça uma pergunta aberta. 4. Nunca abandone uma afirmação de forma abrupta — sempre ofereça uma saída alternativa. 5. Quando a pessoa começar a falar muito, ouça.",
        "exercicio": "Numa conversa normal com alguém próximo, pratique o feedback loop: faça uma afirmação sobre essa pessoa, observe a reação, e ajuste. Veja quantas vezes você consegue aprofundar uma linha usando apenas as reações dela.",
        "gabarito": "O feedback loop é a habilidade mais difícil de desenvolver porque exige dividir a atenção entre falar, observar e ajustar simultaneamente. Começa devagar e vai ficando automático com prática."
      },
      "5": {
        "titulo": "Perfis Estatísticos e Probabilidades",
        "conteudo": "Uma das bases mais sólidas da leitura fria é o conhecimento de perfis estatísticos — o que é verdadeiro para a maioria das pessoas em determinadas categorias. Esse conhecimento permite fazer afirmações com alta probabilidade de acerto mesmo antes de observar qualquer detalhe específico da pessoa.\n\nAs pessoas que buscam consultas místicas ou esotéricas têm um perfil muito específico segundo as pesquisas. A maioria está passando por uma transição de vida (fim de relacionamento, mudança de carreira, perda, nova fase). A maioria tem pelo menos uma área de vida onde sente que perdeu o controle. A maioria nutre esperança de que as coisas vão melhorar. E a maioria está em busca de validação e de ser ouvida tanto quanto está em busca de respostas.\n\nPerfis por FAIXA ETÁRIA: jovens adultos (18-30) geralmente se preocupam com identidade, carreira, relacionamentos e independência. Adultos de meia-idade (30-50) geralmente se preocupam com realizações, relacionamentos em curso, filhos e sentido de vida. Pessoas mais velhas (50+) geralmente se preocupam com saúde, legado, relacionamentos com filhos adultos e a questão de ter vivido bem.\n\nPerfis por APARÊNCIA E ESTILO: roupas muito formais em contexto informal indicam alguém que precisa de controle e boa impressão. Roupas alternativas ou artísticas indicam alguém que valoriza a expressão individual e provavelmente tem perspectivas não-convencionais. Roupas práticas e funcionais indicam alguém focado em resultados. Muito uso de marcas visíveis indica necessidade de status.\n\nPerfis por ESTADO CIVIL E SITUAÇÃO FAMILIAR: alianças, fotos visíveis, referências a filhos — tudo isso fornece contexto. Pessoas casadas com filhos pequenos geralmente carregam tensão entre realização pessoal e responsabilidade familiar. Pessoas solteiras após os 35 frequentemente carregam alguma ambiguidade sobre o assunto — seja paz com a escolha, seja mágoa de histórias não resolvidas.\n\nÉ CRUCIAL entender que perfis estatísticos são FERRAMENTAS, não verdades absolutas. Eles aumentam a probabilidade de acerto mas não garantem nada. O uso consciente deles é o que separa a leitura fria ética da manipulação.",
        "exemplo": "Uma mulher de aproximadamente 40 anos, bem vestida, com aliança mas sem fotos de filhos visíveis, que procura uma consulta num dia útil pela manhã. Perfil estatístico: casada, possivelmente sem filhos ou com filhos crescidos, tem tempo e recursos disponíveis, veio num horário que sugere que controla seu próprio tempo (empresária ou profissional liberal). A preocupação mais provável: algo no casamento ou na realização pessoal. Afirmação de abertura: 'Sinto que você chegou até aqui buscando clareza sobre uma decisão importante — algo que envolve tanto o que você construiu quanto o que ainda quer construir.'",
        "aplicacao": "1. Antes de qualquer interação, colete dados demográficos visíveis. 2. Use perfis estatísticos para formular hipóteses iniciais. 3. Teste essas hipóteses com afirmações abertas. 4. Ajuste conforme o feedback. 5. Nunca trate um perfil estatístico como certeza.",
        "exercicio": "Escolha três pessoas que você conhece superficialmente (não íntimas). Para cada uma, liste o que você sabe sobre elas estatisticamente (faixa etária, situação aparente, estilo). Formule 3 afirmações prováveis para cada uma. Depois, numa conversa natural, veja quantas ressoam.",
        "gabarito": "Perfis estatísticos bem aplicados têm taxa de acerto de 60-80% — muito acima do acaso. O treino está em aprender quais afirmações têm maior probabilidade para cada perfil e como formulá-las de forma que ressoem."
      },
      "6": {
        "titulo": "A Leitura Fria em Diferentes Contextos",
        "conteudo": "A leitura fria não existe apenas no contexto místico — ela é uma habilidade que se aplica a praticamente qualquer interação humana. Conhecer suas aplicações amplia tanto o uso quanto a defesa contra usos manipuladores.\n\nNO CONTEXTO MÍSTICO E DIVINATÓRIO, a leitura fria é a espinha dorsal de muitas consultas de tarot, quiromância, astrologia e mediunidade. Isso não significa que essas práticas são todas fraude — significa que a intuição genuína e a leitura fria frequentemente coexistem, e que mesmo praticantes honestos usam elementos de leitura fria sem necessariamente perceber. O praticante ético sabe disso e é honesto sobre o que é observação e o que é algo mais.\n\nNAS VENDAS E NEGOCIAÇÃO, a leitura fria determina qual abordagem usar com qual pessoa. Um bom vendedor percebe em 30 segundos se está diante de alguém que decide pela lógica ou pela emoção, e adapta a apresentação. Um bom negociador percebe o que a outra parte mais teme perder, e usa isso como alavanca.\n\nNA MEDICINA E PSICOLOGIA CLÍNICA, a leitura fria bem aplicada ajuda o profissional a perceber o que o paciente não está dizendo verbalmente — dor que minimiza, angústia que esconde, ou ao contrário, ansiedade que amplifica. Os melhores clínicos são leitores frios altamente treinados, mesmo sem usar esse nome.\n\nNOS RELACIONAMENTOS PESSOAIS, a leitura fria é a base da empatia profunda. Perceber quando alguém está sofrendo mas dizendo que está bem, quando alguém está com raiva mas expressando indiferença, quando alguém precisa de espaço mas pede atenção — tudo isso é leitura fria aplicada ao amor.\n\nA DEFESA CONTRA LEITURA FRIA é tão importante quanto aprender a fazê-la. Você está vulnerável à leitura fria quando está emocionalmente carregado, quando quer muito acreditar em algo, ou quando é tomado de surpresa. Conhecer as técnicas é a melhor defesa: quando alguém faz uma afirmação Barnum, você reconhece. Quando alguém usa o jackpot, você percebe. Isso não destrói a experiência — apenas te coloca no controle dela.",
        "exemplo": "Você está sendo entrevistado para um emprego. O entrevistador é um praticante intuitivo de leitura fria. Ele observa que você está levemente tenso (dedos entrelaçados), mas confiante no conteúdo (voz firme). Ele diz: 'Me fale sobre um momento em que você precisou trabalhar sob pressão.' Enquanto você responde, ele lê sua linguagem corporal para avaliar se você fala da experiência com orgulho, com ansiedade, ou com relutância — e isso diz mais sobre como você lida com pressão do que as palavras que você escolhe.",
        "aplicacao": "1. Identifique em qual contexto você mais quer desenvolver essa habilidade. 2. Estude os perfis estatísticos específicos desse contexto. 3. Pratique a observação nesse ambiente específico. 4. Desenvolva também sua capacidade de reconhecer quando outros estão usando leitura fria em você.",
        "exercicio": "Na próxima semana, em pelo menos 3 interações diferentes (trabalho, relacionamento, conversa casual), pratique conscientemente: observe antes de falar, formule hipóteses, teste com afirmações ou perguntas abertas, ajuste pelo feedback. Anote o que aprendeu em cada uma.",
        "gabarito": "A leitura fria é mais eficaz quando passa despercebida. O objetivo não é impressionar — é conectar, entender e adaptar. Quanto mais natural e menos performática ela for, mais poderosa será."
      },
      "7": {
        "titulo": "A Psicologia do Acreditar — Por que Funciona",
        "conteudo": "Para usar a leitura fria com consciência e responsabilidade, é essencial entender por que as pessoas acreditam — os mecanismos psicológicos que tornam essa técnica eficaz mesmo quando as afirmações são vagas ou incorretas.\n\nO VIÉS DE CONFIRMAÇÃO é talvez o mais poderoso: as pessoas tendem a lembrar e valorizar as informações que confirmam o que já acreditam ou querem acreditar, e a esquecer ou minimizar as que contradizem. Depois de uma sessão de tarot ou quiromância, a pessoa lembra das afirmações que acertaram com muito mais vivacidade do que das que erraram. Isso cria uma sensação subjetiva de alta precisão mesmo quando a taxa objetiva de acerto foi mediana.\n\nA VALIDAÇÃO EMOCIONAL é frequentemente mais importante do que a precisão factual. Quando um leitor diz 'você carrega uma força que os outros raramente percebem', a pessoa não está avaliando se isso é estatisticamente provável — ela está sentindo que alguém finalmente a viu. Essa sensação de ser visto e compreendido é extremamente poderosa e está frequentemente por trás da experiência de 'ele sabia tudo sobre mim'.\n\nO EFEITO DE COLABORAÇÃO ATIVA é quando a pessoa começa a preencher as lacunas com suas próprias informações, sem perceber que está fazendo isso. Um leitor diz: 'Vejo uma viagem importante em sua vida que mudou algo fundamental.' A pessoa pensa na viagem que fez dois anos atrás e concorda — mas foi ela quem forneceu a especificidade. O leitor apenas abriu a porta.\n\nA ILUSÃO DE ESPECIFICIDADE ocorre quando afirmações vagas são percebidas como específicas porque a pessoa as interpreta através de seu próprio contexto. 'Há alguém em sua vida que não é quem aparenta ser' — essa frase pode se aplicar a uma infinidade de situações, mas a pessoa imediatamente pensa em alguém específico e fica impressionada com a 'precisão'.\n\nO ESTADO DE ABERTURA EMOCIONAL em que as pessoas chegam a consultas místicas as torna mais receptivas a sugestões. Quando alguém está vulnerável, em transição, ou buscando respostas, o cérebro está mais aberto a aceitar afirmações sem o filtro crítico habitual — é um estado semelhante à hipnose leve.\n\nConhecer esses mecanismos serve a dois propósitos: permite ao praticante ser mais eficaz E mais ético, pois ele entende o poder que tem sobre a pessoa naquele momento. E permite ao consultante manter sua agência, aproveitando a experiência sem perder o senso crítico.",
        "exemplo": "Após uma consulta, uma pessoa relata para amigos: 'Ela sabia exatamente que eu passei por uma decepção amorosa recente e que estou repensando minha carreira.' O que realmente aconteceu: o leitor fez afirmações Barnum sobre transições e decepções (universal), a pessoa preencheu com suas experiências específicas, e o viés de confirmação fez o resto. Isso não torna a experiência inválida — mas é importante entender o que realmente aconteceu.",
        "aplicacao": "1. Ao receber uma leitura de qualquer tipo, observe ativamente: quais afirmações eram realmente específicas? Quais eram Barnum? Você preencheu alguma lacuna? 2. Ao fazer uma leitura, seja honesto consigo mesmo sobre o que é observação, o que é probabilidade estatística e o que é genuína intuição.",
        "exercicio": "Releia as afirmações desta aula e identifique 3 afirmações Barnum que você poderia usar. Depois imagine como essas afirmações seriam recebidas por pessoas em diferentes estados emocionais (alguém estável vs alguém em crise). O que muda?",
        "gabarito": "A eficácia da leitura fria não depende de engano — depende de psicologia. Usar esse conhecimento com honestidade é o que distingue o praticante íntegro."
      },
      "8": {
        "titulo": "Ética, Limites e Responsabilidade",
        "conteudo": "A leitura fria é uma das habilidades mais poderosas que uma pessoa pode desenvolver — e exatamente por isso requer uma reflexão ética profunda. O poder de fazer alguém sentir que você 'sabe' coisas sobre ela cria uma responsabilidade real.\n\nO PRINCÍPIO DA NÃO-MANIPULAÇÃO é fundamental: existe uma diferença enorme entre usar a leitura fria para criar conexão genuína, entender melhor as pessoas e ajudá-las — e usá-la para criar dependência, extrair dinheiro, ou exercer controle. A linha pode parecer sutil mas é clara: a intenção e o resultado.\n\nA TRANSPARÊNCIA QUANDO RELEVANTE: em contextos onde alguém acredita que você tem poderes sobrenaturais quando na verdade está usando técnicas aprendíveis, há uma questão ética real. Cada praticante precisa decidir onde fica sua linha. Alguns optam por total transparência. Outros argumentam que a experiência criada tem valor real independente do mecanismo. O mínimo ético é nunca explorar financeiramente essa crença de forma abusiva.\n\nO CUIDADO COM PESSOAS VULNERÁVEIS: pessoas em crise, luto, doenças graves ou perturbação mental estão em estado de maior suscetibilidade. Usar leitura fria (ou qualquer técnica de influência) com essas pessoas exige redobrado cuidado. Nunca crie dependência em alguém que está em estado vulnerável. Nunca substitua ajuda profissional real por uma consulta mística.\n\nA QUESTÃO DO DIAGNÓSTICO: nunca faça afirmações sobre saúde que possam ser interpretadas como diagnóstico médico. 'Vejo uma sensibilidade no sistema nervoso' pode levar uma pessoa a ignorar sintomas reais ou, ao contrário, a entrar em pânico desnecessário.\n\nA HONESTIDADE SOBRE OS ERROS: em qualquer prática honesta de leitura fria ou leitura intuitiva, haverá erros. A forma como o praticante lida com os erros é reveladora de sua integridade. Admitir 'errei nessa' é sinal de praticante sério. Redirecionar ou tentar salvar toda afirmação errada é sinal de falta de integridade.\n\nFINALMENTE: a leitura fria, quando praticada com integridade, não é um engodo — é uma habilidade de percepção e conexão humana profunda. Os melhores praticantes — sejam eles médiuns, psicólogos, médicos ou negociadores — usam essas técnicas para genuinamente ajudar, entender e conectar. É o propósito que define o caráter da prática.",
        "exemplo": "Um praticante recebe uma mulher que, claramente, está procurando uma razão para permanecer num relacionamento problemático. Usando leitura fria, ele percebe isso rapidamente. A decisão ética: não confirmar o que ela quer ouvir apenas para agradá-la, mas também não fazer afirmações absolutas sobre o relacionamento. Em vez disso, direcionar a conversa para o que ela quer e merece, não para o que o parceiro vai ou não vai fazer.",
        "aplicacao": "1. Defina sua própria linha ética antes de praticar leitura fria em qualquer contexto. 2. Nunca use a técnica para criar dependência ou para influenciar decisões importantes de forma unilateral. 3. Seja honesto sobre seus erros. 4. Em contextos profissionais (vendas, liderança), seja consciente de quando está usando e para quê.",
        "exercicio": "Reflita: em que contextos da sua vida você já foi 'lido' por alguém usando essas técnicas — conscientemente ou não? Como se sentiu? O que teria mudado se você tivesse reconhecido a técnica na hora?",
        "gabarito": "A resposta a este exercício é pessoal, mas o objetivo é desenvolver consciência crítica — tanto para usar a técnica com integridade quanto para não ser manipulado por ela."
      }
    }
  },
  "numerologia": {
    "titulo": "Numerologia — O Código dos Números",
    "descricao": "Os números são a linguagem do universo. Aprenda a decifrar o código numérico do seu nome e data de nascimento para revelar sua missão, personalidade e destino.",
    "icone": "🔢",
    "total_aulas": 6,
    "aulas": {
      "1": {
        "titulo": "Os Fundamentos — Como Calcular",
        "conteudo": "A numerologia é o estudo da relação entre números e eventos, personalidades e destinos. Suas raízes estão em Pitágoras (570 a.C.), que acreditava que 'tudo é número' — que a realidade é fundamentalmente matemática e que os números carregam vibrações próprias que influenciam a vida humana. A numerologia pitagórica, base do sistema mais usado no ocidente, reduz todos os números a um dígito de 1 a 9, com exceção dos números mestres 11, 22 e 33.\n\nO SISTEMA DE REDUÇÃO: qualquer número maior que 9 é reduzido somando seus dígitos até chegar a um único algarismo. Exemplo: 29 = 2+9 = 11 (número mestre, não reduz mais) ou 37 = 3+7 = 10 = 1+0 = 1. Os NÚMEROS MESTRES 11, 22 e 33 não são reduzidos porque carregam uma vibração especial — são considerados números de missão elevada.\n\nO NÚMERO DO CAMINHO DE VIDA é calculado a partir da data de nascimento completa. Exemplo: nascido em 15/03/1990. Some: 1+5 = 6 (dia); 0+3 = 3 (mês); 1+9+9+0 = 19 = 1+9 = 10 = 1+0 = 1 (ano). Depois some os resultados: 6+3+1 = 10 = 1+0 = 1. Caminho de vida 1.\n\nO NÚMERO DA EXPRESSÃO (ou do Destino) é calculado a partir do nome completo. Cada letra recebe um valor numérico: A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=1, K=2, L=3, M=4, N=5, O=6, P=7, Q=8, R=9, S=1, T=2, U=3, V=4, W=5, X=6, Y=7, Z=8. Some todos os valores do nome completo e reduza.\n\nO NÚMERO DA ALMA é calculado usando apenas as VOGAIS do nome completo. Revela o que você deseja profundamente, sua motivação interior.\n\nO NÚMERO DA PERSONALIDADE é calculado usando apenas as CONSOANTES do nome completo. Revela como os outros te percebem, sua máscara social.",
        "exemplo": "Maria Silva: M(4)+A(1)+R(9)+I(9)+A(1) = 24; S(1)+I(9)+L(3)+V(4)+A(1) = 18. Total: 24+18 = 42 = 4+2 = 6. Expressão 6 — alguém com forte vocação para cuidar, harmonizar e servir. As vogais: A+I+A+I+A = 1+9+1+9+1 = 21 = 3. Alma 3 — desejo profundo de criatividade e expressão.",
        "aplicacao": "1. Calcule seu Caminho de Vida. 2. Calcule sua Expressão usando o nome completo de registro. 3. Calcule sua Alma (só vogais). 4. Calcule sua Personalidade (só consoantes). 5. Anote os quatro números e veja quais se repetem — repetições indicam ênfase.",
        "exercicio": "Calcule seus quatro números fundamentais agora. Algum número se repete? O Caminho de Vida e a Expressão são harmônicos (próximos ou iguais) ou contrastantes (muito diferentes)? O que isso pode indicar sobre tensões internas?",
        "gabarito": "Quando Caminho de Vida e Expressão são iguais ou muito próximos, indica alinhamento entre missão e forma de se expressar. Quando são opostos, indica tensão entre quem você é chamado a ser e como você naturalmente age."
      },
      "2": {
        "titulo": "Os Números de 1 a 9 — Significados Completos",
        "conteudo": "NÚMERO 1 — O Pioneiro: independência, liderança, originalidade, coragem para iniciar. Missão: tornar-se líder de si mesmo antes de liderar outros. Desafio: tendência ao egoísmo, dificuldade de colaborar e de aceitar ajuda. Vibração: solar, masculina, ativa.\n\nNÚMERO 2 — O Diplomata: cooperação, sensibilidade, parceria, intuição. Missão: criar harmonia e ser a ponte entre forças opostas. Desafio: excesso de dependência dos outros, dificuldade de tomar decisões sozinho, sensibilidade excessiva à crítica. Vibração: lunar, feminina, receptiva.\n\nNÚMERO 3 — O Criativo: expressão, alegria, criatividade, comunicação, sociabilidade. Missão: inspirar, criar e trazer leveza ao mundo. Desafio: dispersão, superficialidade, dificuldade de focar e completar projetos. Vibração: jovial, expansiva.\n\nNÚMERO 4 — O Construtor: trabalho, disciplina, estabilidade, organização, perseverança. Missão: construir bases sólidas e duradouras. Desafio: rigidez, excesso de controle, resistência à mudança, tendência ao workaholism. Vibração: terrosa, sólida.\n\nNÚMERO 5 — O Aventureiro: liberdade, mudança, versatilidade, experiência, sensualidade. Missão: viver plenamente a experiência humana em sua diversidade. Desafio: impulsividade, fuga do compromisso, excesso de mudanças, tendência às vícios. Vibração: mercurial, mutável.\n\nNÚMERO 6 — O Guardião: amor, responsabilidade, família, cura, serviço. Missão: cuidar, harmonizar e criar beleza no mundo. Desafio: excesso de sacrifício pessoal, tendência ao controle disfarçado de cuidado, dificuldade de receber. Vibração: venusina, nutritiva.\n\nNÚMERO 7 — O Buscador: análise, espiritualidade, introspecção, sabedoria, mistério. Missão: ir fundo na busca pela verdade, seja científica ou espiritual. Desafio: isolamento, desconfiança, frieza emocional, ceticismo que se torna cinismo. Vibração: solitária, profunda.\n\nNÚMERO 8 — O Realizador: poder, abundância, ambição, autoridade, sucesso material. Missão: aprender a usar o poder com sabedoria e criar abundância para si e para outros. Desafio: materialismo, abuso de poder, obsessão por controle e sucesso. Vibração: saturnal, intensa.\n\nNÚMERO 9 — O Humanista: compaixão, universalidade, finalização, idealismo. Missão: servir à humanidade e ao bem maior, deixar ir o que não serve mais. Desafio: dificuldade de focar no pessoal (ama a humanidade mas pode negligenciar as pessoas próximas), tendência ao martírio. Vibração: nobre, expansiva.",
        "exemplo": "Uma pessoa com Caminho de Vida 7 e Expressão 3 vive uma tensão fascinante: a missão de aprofundar, refletir e buscar a verdade interior (7) expressa através da comunicação, criatividade e sociabilidade (3). O resultado típico: um escritor, filósofo ou artista que usa a expressão criativa para compartilhar insights profundos. Pense em Carl Jung (Caminho 7, altamente analítico e espiritual) ou em um poeta místico.",
        "aplicacao": "1. Leia o significado do seu Caminho de Vida. Ressoa? 2. Leia o significado da sua Expressão. 3. Compare os dois — são harmônicos ou criam tensão? 4. Leia o desafio de cada número — reconhece esses padrões em você?",
        "exercicio": "Para cada um dos seus quatro números, identifique: uma forma como essa energia se manifesta positivamente na sua vida, e uma forma como o desafio desse número aparece. Seja honesto.",
        "gabarito": "Os desafios dos números não são fraquezas — são áreas de aprendizado. Um 8 que aprende a usar o poder com generosidade torna-se um líder extraordinário. Um 5 que aprende a comprometer-se transforma a versatilidade em riqueza."
      },
      "3": {
        "titulo": "Números Mestres — 11, 22 e 33",
        "conteudo": "Os números mestres são considerados na numerologia como vibrações de missão elevada — carregam o potencial amplificado dos números base (2, 4 e 6) mas com uma intensidade e uma chamada espiritual mais alta. Quem tem número mestre no Caminho de Vida, Expressão ou outros cálculos importantes carrega tanto o potencial extraordinário quanto o desafio correspondente.\n\nNÚMERO MESTRE 11 — O Iluminado: é o 2 amplificado. Onde o 2 busca harmonia e parceria, o 11 busca iluminar, inspirar e elevar. É o número da intuição extrema, da sensibilidade espiritual aguçada, da capacidade de captar o que ainda não é visível para os outros. Missão: ser um canal de inspiração para outras pessoas, usando a sensibilidade e a intuição como ferramentas. Desafio: extrema sensibilidade que pode virar ansiedade crônica, tendência a carregar o peso do mundo, dificuldade de aterrar as visões elevadas na realidade prática.\n\nNÚMERO MESTRE 22 — O Construtor Mestre: é o 4 amplificado. Onde o 4 constrói estruturas pessoais com disciplina, o 22 constrói estruturas que impactam muitas pessoas — projetos de grande escala, sistemas, legados. É o número com maior potencial de realização concreta de todos. Missão: transformar sonhos visionários em realidades tangíveis que beneficiem muitos. Desafio: a grandiosidade da missão pode paralisar (o peso do potencial), ou pode levar ao outro extremo — a pessoa que, incapaz de suportar a responsabilidade, vive aquém de seu potencial por toda a vida.\n\nNÚMERO MESTRE 33 — O Mestre do Amor: é o 6 amplificado. Extremamente raro como número do Caminho de Vida (requer uma data de nascimento específica). Representa o amor incondicional, a cura e o ensinamento do mais alto nível. Missão: curar através do amor e do exemplo. Desafio: antes que a energia do 33 possa ser usada, o portador precisa dominar completamente as energias do 11 e do 22 — o que torna este um número de desenvolvimento extremamente lento e cheio de provas.\n\nPessoas com números mestres frequentemente relatam uma sensação de que a vida exige mais delas do que das outras pessoas — que o padrão para si mesmos é mais alto, que as provas são mais intensas e que as recompensas, quando vêm, são também mais profundas.",
        "exemplo": "Nikola Tesla, Albert Einstein e Barack Obama têm sido associados ao número mestre 11 em diferentes sistemas de cálculo. O que eles têm em comum: uma capacidade de perceber e articular o que a maioria ainda não via, uma sensibilidade intensa (Tesla tinha obsessões e fobias; Einstein era profundamente solitário), e uma missão que claramente transcendeu o pessoal para impactar a humanidade.",
        "aplicacao": "1. Verifique se algum dos seus números principais é 11, 22 ou 33. 2. Se sim, leia o significado do número amplificado E do número base (11 = também leia o 2). 3. Reflita: você sente o peso e o potencial dessa vibração na sua vida?",
        "exercicio": "Se você tem um número mestre: identifique 3 momentos da sua vida onde a intensidade desse número se manifestou claramente — positiva ou negativamente. Se não tem número mestre: identifique uma pessoa próxima que tenha e observe como esses temas aparecem na vida dela.",
        "gabarito": "Os números mestres não tornam ninguém automaticamente superior ou mais especial — eles indicam um caminho mais desafiador e com maior responsabilidade. Muitos portadores de números mestres vivem como o número base (2, 4 ou 6) durante grande parte da vida, só abraçando o potencial mais elevado na maturidade."
      },
      "4": {
        "titulo": "Ciclos Numerológicos — O Ritmo da Vida",
        "conteudo": "A numerologia não é estática — ela descreve ciclos temporais que explicam por que determinados temas surgem em determinadas fases da vida. Os principais ciclos são o Ano Pessoal, o Mês Pessoal e os Ciclos de Vida (Pínáculos e Desafios).\n\nO ANO PESSOAL é calculado somando o dia e mês de nascimento com o ano em curso. Exemplo: nascida em 15/03, no ano 2025: 1+5+0+3+2+0+2+5 = 18 = 1+8 = 9. Ano Pessoal 9. Cada Ano Pessoal tem um tema que influencia o que a vida traz naquele período.\n\nAno 1: começos, novos projetos, plantio, independência. Momento de iniciar, não de colher.\nAno 2: parceria, paciência, cooperação, detalhes. Ano de espera e de cultivar.\nAno 3: expressão, criatividade, socialização, alegria. Ano de florescer e comunicar.\nAno 4: trabalho, fundação, disciplina, construção. Ano de trabalhar duro.\nAno 5: mudança, liberdade, aventura, imprevisibilidade. Ano de transformação.\nAno 6: família, responsabilidade, amor, compromisso. Ano de cuidar e harmonizar.\nAno 7: reflexão, estudo, espiritualidade, introspecção. Ano interior.\nAno 8: poder, dinheiro, autoridade, colheita. Ano de resultados materiais.\nAno 9: conclusão, liberação, perdão, universalidade. Ano de finalizar e soltar.\n\nO CICLO DE 9 ANOS: a vida se organiza em ciclos de 9 anos. Após um Ano 9, vem um novo Ano 1 — um recomeço. Entender em qual ano do ciclo você está ajuda a não nadar contra a maré: quem tenta colher num Ano 4 (de trabalho e plantio) se frustra. Quem trabalha duro num Ano 8 (de colheita) maximiza os resultados.\n\nOS PÍNÁCULOS são quatro grandes fases da vida, cada uma com sua vibração. O primeiro Pináculo vai do nascimento até os 36 menos o Caminho de Vida (por exemplo, para Caminho de Vida 7, termina aos 29 anos). Cada Pináculo tem um número que revela o tema dominante daquela fase.",
        "exemplo": "Uma pessoa descobre que está num Ano Pessoal 9 e fica surpresa — está exatamente num momento de grandes encerramentos: fim de relacionamento longo, mudança de cidade, saída de um emprego. O Ano 9 explica: é exatamente isso que deveria estar acontecendo. Resistir a esses encerramentos seria nadar contra a maré. O Ano 1 que vem a seguir trará novos começos — mas só se os encerramentos do 9 forem completados.",
        "aplicacao": "1. Calcule seu Ano Pessoal atual. 2. Leia o tema desse ano. 3. Olhe para o que está acontecendo na sua vida — isso ressoa? 4. Calcule o Ano Pessoal do ano passado e do próximo — veja a sequência.",
        "exercicio": "Calcule seus Anos Pessoais para os últimos 5 anos. Para cada ano, escreva o tema numerológico e um evento ou fase significativa daquele período. Quantos se encaixam?",
        "gabarito": "A maioria das pessoas encontra forte correspondência entre os temas do Ano Pessoal e os eventos de suas vidas quando olham retrospectivamente. Isso não prova que a numerologia é 'verdade' absoluta — mas sugere que esses ritmos descrevem algo real sobre os ciclos da vida."
      },
      "5": {
        "titulo": "Numerologia do Nome — Análise Avançada",
        "conteudo": "O nome é muito mais do que uma etiqueta — na numerologia, ele é um campo de vibração que influencia como nos expressamos e como somos percebidos. A análise avançada do nome vai além dos quatro números básicos.\n\nO NOME DE BATISMO vs NOME SOCIAL: o nome completo de registro revela o potencial total — é a 'partitura completa'. O nome pelo qual você é chamado no dia a dia revela a vibração que você projeta no presente. Mudanças de nome (casamento, adoção de nome artístico, apelido consolidado) trazem novas vibrações — e a numerologia diz que não são neutras.\n\nNÚMEROS OCULTOS: quando alguns números não aparecem em nenhuma letra do nome completo, isso indica 'karmas ocultos' — áreas de vida onde a pessoa precisa desenvolver conscientemente o que não veio naturalmente. Por exemplo, se não há nenhuma letra com valor 4 no nome, pode haver dificuldade com disciplina, estrutura e compromisso de longo prazo.\n\nNÚMEROS DOMINANTES: números que aparecem muitas vezes nas letras do nome indicam uma ênfase. Um nome com muitas letras de valor 1 (A, J, S) indica alguém com forte energia de liderança e independência expressa na identidade.\n\nA TABELA COMPLETA DE LETRAS E NÚMEROS:\n1: A, J, S\n2: B, K, T\n3: C, L, U\n4: D, M, V\n5: E, N, W\n6: F, O, X\n7: G, P, Y\n8: H, Q, Z\n9: I, R\n\nCOMPATIBILIDADE NUMEROLÓGICA ENTRE NOMES: quando dois nomes têm vibrações que se completam (por exemplo, um 1 e um 2 — liderança e cooperação), há harmonia natural. Quando as vibrações colidem (dois 1s, por exemplo — duas lideranças que disputam espaço), há mais conflito natural mas também mais dinamismo.",
        "exemplo": "Uma artista que nasceu com nome de registro com Expressão 8 (vibração de poder e materialidade) adota um nome artístico que calcula para 3 (criatividade e expressão). A mudança de nome foi uma mudança de vibração — ela transitou de uma identidade de realizadora material para uma identidade de expressão criativa. Isso é numerologicamente coerente com a mudança de carreira.",
        "aplicacao": "1. Liste todas as letras do seu nome completo e calcule a tabela numérica. 2. Identifique quais números de 1 a 9 estão ausentes. 3. Identifique quais aparecem mais vezes. 4. Se você tem apelido ou nome social diferente do de registro, calcule os dois e compare.",
        "exercicio": "Calcule a Expressão do seu nome de registro e do nome pelo qual você é chamado cotidianamente (se diferente). O que muda? A vibração do nome cotidiano ressoa mais com quem você se sente sendo hoje?",
        "gabarito": "Não há nome 'melhor' ou 'pior' — cada vibração tem seu propósito. O objetivo é entender qual vibração você está projetando e se ela está alinhada com quem você quer ser."
      },
      "6": {
        "titulo": "Numerologia na Prática — Integrando os Números",
        "conteudo": "Uma análise numerológica completa não é uma soma de descrições isoladas — é uma síntese que revela quem a pessoa é, qual é sua missão, que desafios enfrenta e em que fase de vida está.\n\nO MAPA NUMEROLÓGICO COMPLETO inclui pelo menos: Caminho de Vida (missão fundamental), Expressão (talentos e forma de agir), Alma (desejos profundos), Personalidade (máscara social), Ano Pessoal (fase atual), e números ausentes (karmas).\n\nCOMO INTEGRAR: comece pelo Caminho de Vida — ele é a missão, o fio condutor. Depois veja a Expressão — como essa missão é expressa naturalmente. Se Caminho e Expressão são harmônicos, a pessoa tende a fluir. Se são contrastantes, há tensão interna que pode ser fonte de criatividade ou de conflito.\n\nDepois olhe a Alma — o que a pessoa deseja profundamente. Se a Alma está alinhada com o Caminho e a Expressão, há coerência interna. Se a Alma deseja algo diferente do que o Caminho pede, há uma sensação de sacrifício ou de algo não vivido.\n\nOs NÚMEROS AUSENTES revelam onde o trabalho é mais necessário. Uma pessoa sem nenhum 6 no nome pode ter dificuldade com cuidado, família e responsabilidade — ou pode ser exatamente aí que sua maior lição de vida está.\n\nO ANO PESSOAL posiciona tudo isso no tempo: que aspectos do mapa estão sendo ativados agora? Um Caminho de Vida 1 num Ano 1 sente o impulso de liderança amplificado. Um Caminho 7 num Ano 9 está num momento de profunda introspecção e finalização.\n\nA PRECISÃO DE UMA BOA LEITURA: como em qualquer sistema simbólico, o numerólogo experiente usa os números como mapa, não como território. As descrições são arquétipos — cada pessoa os vive de forma única. O objetivo não é encaixar a pessoa num número, mas usar o número para abrir conversa sobre quem ela é.",
        "exemplo": "Ana, Caminho de Vida 7, Expressão 3, Alma 9, Personalidade 3, Ano Pessoal 4, ausência do número 1. Leitura integrada: Ana é uma buscadora espiritual (7) que se expressa de forma criativa e comunicativa (Expressão e Personalidade 3), com um desejo profundo de servir à humanidade (Alma 9). O Ano 4 atual é de trabalho duro e construção de bases — provavelmente um período menos glamouroso mas de grande importância estrutural. A ausência do 1 sugere que iniciativa e liderança pessoal são áreas de desenvolvimento consciente para ela.",
        "aplicacao": "1. Monte seu mapa completo com os cinco números. 2. Escreva um parágrafo integrando todos eles. 3. Identifique as harmonias e as tensões. 4. Veja o que o Ano Pessoal atual está ativando no mapa.",
        "exercicio": "Faça a análise numerológica completa de alguém que você conhece bem (com permissão). Escreva um parágrafo integrando os números. Mostre para a pessoa e pergunte se ressoa. Anote o feedback.",
        "gabarito": "Uma boa leitura numerológica integradora ressoa porque descreve padrões reais da personalidade, não porque é mágica. O sistema funciona como um espelho estruturado que ajuda a pessoa a ver a si mesma com mais clareza."
      }
    }
  },
  "runas": {
    "titulo": "Runas Nórdicas — O Alfabeto dos Ancestrais",
    "descricao": "As runas são o sistema de escrita e adivinhação dos povos germânicos e nórdicos. Cada runa é uma letra, um conceito e uma força cósmica. Aprenda a ler, lançar e interpretar as 24 runas do Elder Futhark.",
    "icone": "ᚠ",
    "total_aulas": 6,
    "aulas": {
      "1": {
        "titulo": "A Origem das Runas",
        "conteudo": "As runas (do proto-germânico 'rūnō', que significa 'segredo' ou 'sussurro') são o mais antigo sistema de escrita dos povos germânicos e nórdicos. Os registros arqueológicos mais antigos de runas datam do século II d.C., mas a tradição oral sugere uso muito anterior. Elas foram usadas simultaneamente como alfabeto (para inscrições em pedras, armas, jóias e madeira) e como sistema divinatório e mágico.\n\nA mitologia nórdica conta que as runas não foram inventadas — foram descobertas. Odin, o deus supremo dos nórdicos, pendurou-se de cabeça para baixo na Yggdrasil (a Árvore do Mundo) por nove dias e nove noites sem comer ou beber, em sacrifício de si mesmo para si mesmo, até que as runas se revelaram a ele em visão. Essa narrativa não é apenas mito — ela revela a natureza das runas: não são criações humanas, mas forças que existem no tecido da realidade e que foram acessadas através de sacrifício e contemplação profunda.\n\nO ELDER FUTHARK é o mais antigo e completo alfabeto rúnico, composto por 24 runas divididas em três grupos de 8 chamados Aettir (plural de Aett, 'família'): o Aett de Freyr/Freyja (runas 1-8), o Aett de Heimdall (runas 9-16) e o Aett de Tyr (runas 17-24). O nome 'Futhark' vem das seis primeiras runas: Fehu, Uruz, Thurisaz, Ansuz, Raidho, Kenaz.\n\nNa adivinhação rúnica, cada runa pode aparecer em posição direta (upright) ou invertida (merkstave). A posição invertida não significa necessariamente algo negativo — indica a energia da runa em sua manifestação mais desafiadora, bloqueada ou interiorizada. Nem todas as runas têm merkstave (runas simétricas como Isa ou Gebo têm o mesmo significado em qualquer posição).\n\nAs runas não 'preveem' o futuro de forma determinista — elas revelam as energias em jogo no momento presente e os padrões que, se continuarem, produzirão determinados resultados. São uma ferramenta de consciência, não de fatalismo.",
        "exemplo": "Uma escavação arqueológica na Noruega encontrou uma runa Tiwaz (ᛏ) gravada numa faca de guerra viking. Não era decoração — era um encantamento pedindo proteção divina de Tyr, o deus da guerra justa. As runas eram inseparáveis da vida cotidiana, espiritual e guerreira dos nórdicos.",
        "aplicacao": "1. Familiarize-se com os símbolos das 24 runas. 2. Aprenda o nome de cada uma. 3. Entenda a divisão em três Aettir. 4. Comece a perceber runas em contextos culturais — logotipos, tatuagens, símbolos modernos que derivam das runas.",
        "exercicio": "Desenhe as 24 runas do Elder Futhark de memória (ou copiando) e escreva o nome de cada uma ao lado. Esse ato de escrever manualmente é, em si, uma forma de conexão com a tradição rúnica.",
        "gabarito": "As 24 runas são: Fehu, Uruz, Thurisaz, Ansuz, Raidho, Kenaz, Gebo, Wunjo, Hagalaz, Nauthiz, Isa, Jera, Eihwaz, Perthro, Algiz, Sowilo, Tiwaz, Berkano, Ehwaz, Mannaz, Laguz, Ingwaz, Dagaz, Othala."
      },
      "2": {
        "titulo": "O Primeiro Aett — As Runas de Freyr",
        "conteudo": "O Primeiro Aett está sob a regência de Freyr e Freyja, os deuses da fertilidade, abundância, amor e magia. As oito runas deste grupo lidam com forças fundamentais da vida material e instintiva.\n\nFEHU (ᚠ) — Gado/Riqueza: a primeira runa é sobre prosperidade, abundância e o fluxo de riqueza. Antigamente, o gado era a riqueza mais fundamental. Fehu não é sobre dinheiro parado — é sobre riqueza em movimento, circulando, crescendo. Direta: prosperidade merecida, energia vital forte, momento de colheita. Merkstave: perda material, energia estagnada, ganância.\n\nURUZ (ᚢ) — Auroque/Força Bruta: o auroque era um boi selvagem de força imensuravelmente superior à do boi domesticado. Uruz é a força primitiva, a saúde robusta, a vitalidade animal. Direta: força, saúde, potencial não domesticado, momento de agir com vigor. Merkstave: fraqueza, doença, força mal direcionada.\n\nTHURISAZ (ᚦ) — Gigante/Espinho: é a runa do caos controlado, da força destruidora que também limpa o caminho. Associada a Thor e seus inimigos, os Jötnar (gigantes). Direta: proteção, força destrutiva utilizada construtivamente, momento de confrontar. Merkstave: perigo, compulsão, energia destrutiva descontrolada.\n\nANSUZ (ᚨ) — Boca/Mensagem Divina: a runa da comunicação divina, das palavras, da sabedoria de Odin. Direta: mensagem importante chegando, comunicação clara, sabedoria, bênção divina. Merkstave: má comunicação, engano, manipulação através de palavras.\n\nRAIDHO (ᚱ) — Roda/Jornada: movimento, viagem, ritmo. A roda é o veículo, a jornada é tanto física quanto espiritual. Direta: jornada positiva, progresso, bom timing, as coisas fluindo no ritmo certo. Merkstave: jornada bloqueada, timing errado, planos que precisam ser revistos.\n\nKENAZ (ᚲ) — Tocha/Conhecimento: a luz que ilumina o que estava escuro. Conhecimento, criatividade, transformação pelo fogo. Direta: iluminação, revelação, novo conhecimento, criatividade em chamas. Merkstave: falsa clareza, fogo destruidor, conhecimento usado de forma errada.\n\nGEBO (ᚷ) — Presente/Troca: a runa da dádiva, da troca equilibrada, da parceria. Não tem merkstave (é simétrica). Sempre significa: presente, intercâmbio, parceria, generosidade que cria conexão.\n\nWUNJO (ᚹ) — Alegria/Clã: bem-estar, alegria, a sensação de pertencer. Direta: felicidade, harmonia, objetivos alcançados, sentido de comunidade. Merkstave: alegria vazia, felicidade superficial, conflito dentro do grupo.",
        "exemplo": "Numa tiragem para alguém que pergunta sobre sua situação financeira, Fehu aparece merkstave e Raidho aparece direta. Leitura: há uma estagnação ou perda na área financeira (Fehu invertida), mas o movimento está a caminho (Raidho direta) — a situação está em transição, não em colapso.",
        "aplicacao": "1. Memorize as 8 runas do Primeiro Aett e seus significados. 2. Para cada uma, pense numa situação da sua vida onde aquela energia esteve presente. 3. Pratique identificar qual seria o significado merkstave de cada uma.",
        "exercicio": "Escolha uma runa do Primeiro Aett que ressoa com algo que você está vivendo agora. Escreva seu símbolo três vezes, pronuncie seu nome em voz alta, e reflita por 5 minutos sobre como essa energia está presente (ou ausente) na sua vida.",
        "gabarito": "As runas do Primeiro Aett lidam com as forças mais fundamentais: sobrevivência, recursos, força, comunicação, jornada, conhecimento, troca e alegria. São as runas da vida terrestre e instintiva."
      },
      "3": {
        "titulo": "O Segundo Aett — As Runas de Heimdall",
        "conteudo": "O Segundo Aett está sob a regência de Heimdall (o guardião dos mundos) e Mordgud. Estas runas lidam com desafios, transformação, e os ciclos mais profundos da existência.\n\nHAGALAZ (ᚺ) — Granizo: destruição súbita vinda de forças fora do nosso controle, como uma tempestade de granizo que arrasa a colheita. Não tem merkstave (é simétrica no Elder Futhark). Sempre significa: ruptura súbita, crise fora do controle, caos necessário para transformação. É uma das runas mais temidas mas também uma das mais transformadoras — o granizo destrói, mas fertiliza o solo para nova plantação.\n\nNAUTHIZ (ᚾ) — Necessidade/Limitação: a runa da restrição, da necessidade não satisfeita, mas também da resistência que fortalece. É no atrito que a faísca nasce. Direta: necessidade, limitação que ensina, paciência forçada, perseverança necessária. Merkstave: limitação paralisante, resistência que sufoca, recusa em aceitar restrições.\n\nISA (ᛁ) — Gelo: paralisia, congelamento, quietude forçada. Não tem merkstave. Sempre significa: tudo parou, é hora de aguardar, não force nada agora. O gelo não é o fim — é a preservação durante o inverno.\n\nJERA (ᛃ) — Ano/Colheita: o ciclo completo, a colheita que vem depois do plantio e da espera. Não tem merkstave. Sempre significa: o tempo certo chegou, a colheita é proporcional ao plantio, os ciclos da vida estão se completando.\n\nEIHWAZ (ᛇ) — Teixo/Transformação: o teixo é a árvore que vive por milênios, cuja madeira era usada para arcos de guerra, e que cresce em cemitérios — ela conecta vida e morte. Runa da transformação profunda e da perseverança através das crises. Direta: transformação, força que vem de dentro, confiabilidade. Merkstave: fraqueza interna, rigidez, bloqueio na transformação.\n\nPERTHRO (ᛈ) — Copa/Mistério: a mais misteriosa das runas. Seu significado exato é debatido. Associada ao destino, ao acaso, ao que está escondido. Direta: mistério se revelando, o acaso trabalhando a seu favor, prazer oculto. Merkstave: segredos dolorosos, o acaso trabalhando contra, vícios ocultos.\n\nALGIZ (ᛉ) — Alce/Escudo: proteção, conexão com o divino, consciência expandida. Direta: proteção, conexão espiritual, estar no lugar certo. Merkstave: vulnerabilidade, proteção enfraquecida, conexão com forças que drenam.\n\nSOWILO (ᛊ) — Sol: vitória, força solar, clareza. Não tem merkstave. Sempre positiva: sucesso, energia vital, clareza de propósito, vitória.",
        "exemplo": "Hagalaz aparece numa tiragem sobre um relacionamento. Em vez de dizer 'crise devastadora', o leitor experiente diz: 'Há uma ruptura que não pode ser controlada chegando — ou já acontecendo. Mas o granizo fertiliza o solo. O que está sendo destruído aqui pode ser o espaço para algo novo e mais autêntico crescer.'",
        "aplicacao": "1. Memorize as 8 runas do Segundo Aett. 2. Perceba que várias delas (Hagalaz, Isa, Jera) não têm merkstave — são forças neutras que se manifestam como são. 3. Identifique qual dessas energias está mais presente na sua vida agora.",
        "exercicio": "Qual das runas do Segundo Aett descreve melhor a fase que você está vivendo? Escreva um parágrafo sobre como essa energia está se manifestando na sua vida.",
        "gabarito": "O Segundo Aett lida com forças além do controle humano — crise, necessidade, congelamento, ciclos, mistério. Aprender a trabalhar com essas forças, em vez de resistir a elas, é a sabedoria central deste grupo."
      },
      "4": {
        "titulo": "O Terceiro Aett — As Runas de Tyr",
        "conteudo": "O Terceiro Aett está sob a regência de Tyr (deus da guerra justa e da lei) e Zisa. Estas runas lidam com humanidade, comunidade, herança e o fim dos ciclos.\n\nTIWAZ (ᛏ) — Tyr/Justiça: nomeada pelo deus que sacrificou a mão para acorrentar o lobo Fenrir, Tiwaz é a runa do sacrifício pelo bem maior, da justiça, da coragem moral. Direta: justiça, sacrifício honroso, vitória pela integridade. Merkstave: injustiça, sacrifício em vão, motivações desonestas disfarçadas de nobreza.\n\nBERKANO (ᛒ) — Bétula/Renascimento: a bétula é a primeira árvore a brotar após um incêndio florestal. Runa do renascimento, da feminidade, do cuidado que nutre. Direta: novo começo, nutrição, cura, renascimento após destruição. Merkstave: estagnação, incapacidade de crescer, controle disfarçado de cuidado.\n\nEHWAZ (ᛖ) — Cavalo/Parceria: dois cavalos trabalhando juntos — parceria que multiplica o poder de cada um. Direta: parceria frutífera, movimento em sincronia, confiança mútua. Merkstave: parceria desequilibrada, movimento sem direção, desconfiança.\n\nMANNAZ (ᛗ) — Humanidade: a runa da natureza humana, do ser social, da consciência de si mesmo dentro da coletividade. Direta: humanidade em equilíbrio, consciência expandida, cooperação. Merkstave: ego inflado, manipulação, perda da perspectiva sobre si mesmo.\n\nLAGUZ (ᛚ) — Água/Fluxo: a água que não pode ser controlada mas pode ser navegada. Intuição, inconsciente, fluxo das emoções. Direta: intuição confiável, fluir com a vida, emoções como guia. Merkstave: intuição bloqueada, emoções avassaladoras, afogamento nos sentimentos.\n\nINGWAZ (ᛜ) — Ing/Potencial: associada ao deus Ingwaz (Freyr), é a semente antes de germinar — potencial concentrado pronto para explodir. Não tem merkstave. Sempre significa: potencial pronto para se manifestar, conclusão de uma fase, energia concentrada.\n\nDAGAZ (ᛞ) — Amanhecer/Clareza: o momento entre a noite e o dia, quando tudo muda. Transformação, clareza repentina, breakthrough. Não tem merkstave. Sempre significa: transformação profunda, clareza que vem de dentro, novo dia que começa.\n\nOTHALA (ᛟ) — Herança/Lar: o que foi herdado — terra, sangue, tradição, valores familiares. Direta: herança valiosa, raízes que sustentam, propriedade e pertencimento. Merkstave: herança que prende, valores familiares tóxicos, incapacidade de deixar o passado.",
        "exemplo": "Dagaz aparece numa tiragem para alguém que está no meio de uma crise existencial profunda. A mensagem: você está no limiar — não na escuridão, não na luz, mas no momento exato de transição. Dagaz não promete que vai ser fácil, mas confirma que a clareza está chegando e que esta crise é, na verdade, o amanhecer de algo novo.",
        "aplicacao": "1. Memorize as 8 runas do Terceiro Aett. 2. Perceba a progressão dos três Aettir: do instintivo e material (1º) ao caótico e transformador (2º) ao humano e comunitário (3º). 3. Identifique onde cada Aett aparece na sua vida agora.",
        "exercicio": "Escolha uma runa do Terceiro Aett e pesquise sua mitologia nórdica associada. Como a história do deus ou símbolo relacionado ilumina o significado da runa?",
        "gabarito": "O Terceiro Aett representa a dimensão mais humana e espiritual das runas — justiça, renascimento, parceria, humanidade, intuição, potencial e herança. É onde o ciclo completo da existência se fecha."
      },
      "5": {
        "titulo": "Métodos de Tiragem Rúnica",
        "conteudo": "Existem muitas formas de fazer uma tiragem rúnica. As mais comuns vão de uma única runa a layouts complexos de 9 ou mais runas. A escolha do método depende da complexidade da pergunta e da profundidade de resposta desejada.\n\nA RUNA DO DIA: tire uma única runa pela manhã como orientação para o dia. Não faça uma pergunta específica — simplesmente abra a mente para receber uma mensagem. A runa revelada pode ser literal (Raidho num dia de viagem) ou simbólica (Isa num dia que pede pausa e reflexão).\n\nA TIRAGEM DE TRÊS RUNAS é o layout mais versátil. Dependendo da intenção, pode representar: Passado-Presente-Futuro / Situação-Ação-Resultado / Problema-Causa-Solução / Você-O Outro-A Relação. Esta flexibilidade torna a tiragem de três runas adequada para quase qualquer pergunta.\n\nA TIRAGEM DE CINCO RUNAS expande para: Situação Atual / O que Está Oculto / Conselho / Caminho Mais Provável / Resultado Final. É boa para situações mais complexas onde a dimensão oculta é importante.\n\nA CRUZ NÓRDICA (5 runas em forma de cruz) oferece: Centro (o coração da questão) / Norte (o passado relevante) / Sul (o possível futuro) / Leste (forças que ajudam) / Oeste (forças que dificultam).\n\nO CAST (lançamento livre) é o método mais antigo: as runas são jogadas sobre uma superfície e lidas com base em quais caíram com a face para cima, quais caíram perto do centro (mais relevantes), quais ficaram agrupadas, e quais caíram sozinhas.\n\nCOMO PREPARAR-SE: antes de qualquer tiragem, crie um estado de concentração e intenção. Muitos praticantes seguram as runas nas mãos por um momento, respiram profundamente, e formulam uma pergunta clara. A clareza da pergunta influencia a clareza da resposta.\n\nCOMO LIMPAR AS RUNAS: após uso, especialmente para outros, algumas tradições recomendam passar as runas pela fumaça de ervas (sálvia, arruda), enterrá-las brevemente na terra, ou simplesmente guardá-las num saco escuro por um tempo.",
        "exemplo": "Alguém pergunta sobre uma decisão profissional. Tiragem de três runas: Passado (Fehu direta — prosperidade que construiu), Presente (Isa — pausa, congelamento, espera necessária), Futuro (Jera — colheita proporcional). Leitura: você construiu algo real (Fehu), está num momento de aparente paralisia que é na verdade necessário (Isa), e se respeitar esse ritmo, a colheita virá no tempo certo (Jera). Não force. Confie no ciclo.",
        "aplicacao": "1. Comece com a runa do dia por pelo menos uma semana. 2. Depois experimente a tiragem de três runas para uma pergunta real. 3. Registre suas tiragens e depois verifique se a orientação se mostrou relevante.",
        "exercicio": "Faça uma tiragem de três runas para uma situação real que você está vivendo. Use o modelo Situação-Ação-Resultado. Escreva sua interpretação e volte a ela em 2 semanas.",
        "gabarito": "A interpretação de uma tiragem melhora com prática. No começo, leia cada runa individualmente. Com o tempo, você começa a ver como as runas dialogam entre si numa tiragem — o conjunto conta uma história mais rica do que as peças isoladas."
      },
      "6": {
        "titulo": "Magia Rúnica e Runas de Proteção",
        "conteudo": "Além da adivinhação, as runas foram historicamente usadas para magia — gravar runas em objetos para invocar proteção, amor, cura ou vitória. Essa tradição é chamada de galdrastafir (uso de runas em fórmulas mágicas) e está documentada em centenas de inscrições arqueológicas.\n\nAs RUNAS DE PROTEÇÃO mais poderosas incluem Algiz (proteção e conexão espiritual), Tiwaz (proteção guerreira e justiça), Thurisaz (barreira contra inimigos) e Isa (congelar situações negativas).\n\nAs RUNAS DE CURA incluem Berkano (renascimento e cura feminina), Laguz (fluxo e purificação emocional), Uruz (força vital e saúde) e Sowilo (energia solar e vitalidade).\n\nOs BINDRUNES são runas combinadas — duas ou mais runas sobrepostas para criar um símbolo composto com as energias de ambas. Muitos logos modernos e símbolos culturais são, na verdade, bindrunes ancestrais.\n\nA MAGIA RÚNICA na prática moderna não requer crença sobrenatural — pode ser entendida como um sistema de intenção simbólica. Gravar uma runa numa vela, carregar uma pedra com uma runa pintada, ou desenhar uma runa ao acordar são formas de intenção ritual que funcionam através da psicologia da intenção e do foco.\n\nRUNAS E MEDITAÇÃO: cada runa pode ser objeto de meditação. Sente-se em posição confortável, visualize a runa à sua frente, pronuncie seu nome repetidamente (canto rúnico ou 'galdr'), e abra-se para as imagens e sentimentos que surgem. Esta é a forma mais antiga de 'estudar' as runas — não através de livros, mas através de experiência direta.\n\nÉTICA NA PRÁTICA RÚNICA: como qualquer sistema de poder, as runas pedem responsabilidade. A tradição nórdica é clara: o uso de magia para prejudicar outros tem consequências — não necessariamente 'kármicas' no sentido orientalista, mas no sentido de que quem manipula energias destrutivas eventualmente é consumido por elas. A magia rúnica mais poderosa é sempre a que alinha a vontade pessoal com forças maiores, não a que tenta forçar resultados contra a natureza das coisas.",
        "exemplo": "Uma pessoa que se sentindo particularmente vulnerável num momento difícil desenha a runa Algiz no interior do pulso com uma caneta comum ao sair de casa. Para ela, não é um encantamento sobrenatural — é um lembrete intencional de que ela carrega proteção consigo, um âncora simbólica de força. O efeito psicológico é real: ela se sente mais centrada durante o dia.",
        "aplicacao": "1. Escolha uma runa que corresponde a algo que você quer desenvolver ou se proteger. 2. Desenhe-a num papel e coloque em lugar visível. 3. Toda vez que vê o símbolo, recorde sua intenção. 4. Pratique a meditação rúnica com pelo menos uma runa por semana.",
        "exercicio": "Escolha uma situação na sua vida que precisa de uma força específica (proteção, cura, clareza, nova energia). Identifique qual runa corresponde a essa energia. Crie um ritual simples usando essa runa — pode ser desenhá-la, meditar com ela, ou carregá-la escrita num papel por uma semana.",
        "gabarito": "A magia rúnica é, em sua essência, uma forma de psicologia simbólica: você usa um símbolo carregado de significado para ancorar uma intenção na mente e no comportamento. O 'poder' da runa é o poder que você investe nela através da intenção focada."
      }
    }
  },
  "tarot": {
    "titulo": "Tarô Completo — Os 78 Arcanos",
    "descricao": "O Tarô é um sistema de 78 cartas que mapeia a jornada da consciência humana. Aprenda a ler os Arcanos Maiores e Menores, os naipes e os métodos de tiragem.",
    "icone": "🃏",
    "total_aulas": 8,
    "aulas": {
      "1": {
        "titulo": "História e Estrutura do Tarô",
        "conteudo": "O Tarô como o conhecemos hoje surgiu na Europa do século XV como jogo de cartas aristocrático — os 'trionfi' italianos. Sua associação com adivinhação e misticismo só se consolidou no século XVIII, especialmente através da figura do ocultista Antoine Court de Gébelin, que afirmou (incorretamente) que o Tarô seria um repositório do conhecimento do Egito Antigo. Apesar da afirmação histórica ser falsa, ela catalisou o uso do Tarô como ferramenta divinatória e esotérica que se aprofundou nos séculos seguintes.\n\nO baralho de Tarô padrão tem 78 cartas divididas em duas partes: os 22 ARCANOS MAIORES (do latim 'arcanum', segredo) que representam forças arquetípicas universais, e os 56 ARCANOS MENORES que lidam com os aspectos cotidianos da existência.\n\nOs ARCANOS MAIORES vão do 0 (O Louco) ao XXI (O Mundo) e narram a jornada do herói — a Jornada do Louco — desde a inocência inicial até a realização completa. Cada arcano maior é um arquétipo que todos os seres humanos encontram em suas vidas.\n\nOs ARCANOS MENORES dividem-se em quatro naipes, cada um associado a um elemento:\n- PAUS (Fogo): energia, paixão, criatividade, trabalho, ambição\n- COPAS (Água): emoções, amor, relacionamentos, intuição, inconsciente\n- ESPADAS (Ar): mente, conflito, comunicação, verdade, desafios mentais\n- OUROS (Terra): dinheiro, trabalho concreto, corpo, materialidade, recursos\n\nDentro de cada naipe há 14 cartas: Ás (1) até 10, mais quatro cartas da corte: Valete, Cavaleiro, Rainha e Rei. As cartas de 1 a 10 narram uma progressão temática dentro de cada naipe. As cartas da corte representam aspectos de personalidade ou pessoas reais.\n\nO BARALHO DE RIDER-WAITE (1909) é o mais influente da história moderna. Criado pelo ocultista Arthur Edward Waite e ilustrado pela artista Pamela Colman Smith, foi o primeiro baralho a ter ilustrações completas em todas as 78 cartas (antes, as cartas menores eram apenas símbolos repetidos). A maioria dos baralhos modernos é baseada neste sistema.",
        "exemplo": "Uma pessoa que nunca viu um baralho de Tarô percebe que as cartas dos Arcanos Maiores contam uma história: O Louco (0) parte sem planos; O Mago (I) usa suas ferramentas; A Sacerdotisa (II) desenvolve intuição; e assim por diante até O Mundo (XXI) onde a jornada se completa. Essa narrativa é a jornada de qualquer vida humana — de iniciante a sábio.",
        "aplicacao": "1. Familiarize-se com a estrutura dos 78 arcanos. 2. Observe os quatro naipes e seus elementos. 3. Passe por todas as cartas da corte de cada naipe. 4. Identifique qual naipe parece mais familiar ou confortável para você.",
        "exercicio": "Pegue um baralho (físico ou imagens digitais) e divida as 78 cartas em: Arcanos Maiores, Paus, Copas, Espadas e Ouros. Observe as imagens de cada grupo. Que impressão geral cada grupo transmite?",
        "gabarito": "Os Arcanos Maiores têm uma qualidade mais dramática e universal. Os Paus têm energia e movimento. As Copas têm fluidez e emoção. As Espadas têm clareza cortante. Os Ouros têm solidez e concretude. Perceber essas atmosferas é o primeiro passo da leitura intuitiva."
      },
      "2": {
        "titulo": "Os Arcanos Maiores — A Jornada do Louco (0-X)",
        "conteudo": "O LOUCO (0): o início de tudo. Inocência, espontaneidade, o salto no desconhecido com confiança total. Não é estupidez — é a coragem de começar sem saber onde vai terminar. Pergunta central: o que você está prestes a iniciar sem garantias?\n\nO MAGO (I): vontade, habilidade, poder de manifestação. O Mago tem todos os quatro elementos (Paus, Copas, Espadas, Ouros) sobre sua mesa — ele tem as ferramentas, basta usá-las. Pergunta central: você está usando todo o seu potencial?\n\nA SACERDOTISA (II): intuição, mistério, conhecimento que não vem dos livros mas do silêncio e da escuta interior. O que está oculto. Pergunta central: o que você sabe mas ainda não reconhece saber?\n\nA IMPERATRIZ (III): fertilidade, abundância, natureza, maternidade, criação. A terra fértil que nutre. Pergunta central: o que em sua vida está crescendo e precisando de cuidado?\n\nO IMPERADOR (IV): estrutura, autoridade, ordem, paternidade, o poder que organiza. Pergunta central: onde você precisa estabelecer mais limites e estrutura?\n\nO HIEROFANTE (V): tradição, ensino, instituições, transmissão de sabedoria estabelecida. Pode ser o professor ou a doutrina. Pergunta central: que crenças ou tradições estão guiando (ou aprisionando) você?\n\nOS AMANTES (VI): escolha, amor, valores, alinhamento entre coração e mente. Não é necessariamente sobre romance — é sobre a grande escolha que define quem você é. Pergunta central: qual é a escolha fundamental que você está evitando?\n\nO CARRO (VII): vitória através do controle de forças opostas, determinação, movimento com propósito. Pergunta central: você está no controle do seu caminho ou sendo levado pelas circunstâncias?\n\nA FORÇA (VIII): força interior, compaixão que domina o instinto bruto, coragem que não precisa de força física. A mulher que doma o leão com amor. Pergunta central: onde você precisa de suavidade para encontrar sua força real?\n\nO EREMITA (IX): recolhimento, sabedoria interior, a jornada solitária em busca de luz. O lanterna que ilumina apenas o próximo passo. Pergunta central: que resposta você só encontrará no silêncio?\n\nA RODA DA FORTUNA (X): ciclos, sorte, destino, os movimentos maiores da vida que estão além do controle pessoal. Pergunta central: que ciclo está se completando ou começando na sua vida?",
        "exemplo": "Uma pessoa atravessa uma fase de isolamento intenso e tira O Eremita. Em vez de interpretar isso como 'sinal negativo', o leitor percebe o alinhamento: a carta confirma e valida a fase. 'Você está num período de recollhimento necessário — não é fraqueza, é sabedoria. O Eremita não fica no escuro por punição; ele escolhe o silêncio para encontrar a luz que vai iluminar os outros depois.'",
        "aplicacao": "1. Tire cada uma dessas cartas individualmente e estude sua imagem. 2. Para cada uma, identifique: qual é o desafio dessa carta? Qual é o presente? 3. Qual dessas cartas sente mais próxima de onde você está agora?",
        "exercicio": "Escolha dois Arcanos Maiores desta lista — um que ressoa positivamente e um que te desconforta. Para cada um, escreva: por que essa carta me atrai/repele? O que ela diz sobre onde estou agora?",
        "gabarito": "A carta que mais te desconforta frequentemente é a que mais tem a te ensinar. A carta que mais ressoa frequentemente confirma algo que você já sabe mas talvez não tenha nomeado."
      },
      "3": {
        "titulo": "Os Arcanos Maiores — A Jornada do Louco (XI-XXI)",
        "conteudo": "A JUSTIÇA (XI): causa e efeito, equilíbrio, consequências das escolhas. Não é punição — é equilíbrio. O que você colhe é o que plantou. Pergunta central: que padrão em sua vida está produzindo as consequências que você está vivendo?\n\nO ENFORCADO (XII): suspensão voluntária, mudança de perspectiva, sacrifício de uma forma de ver para ganhar uma mais verdadeira. O Enforcado escolheu se suspender — não é vítima. Pergunta central: que ponto de vista você precisa abandonar para enxergar mais claro?\n\nA MORTE (XIII): transformação profunda, fim de uma fase, o encerramento necessário para o novo começo. Raramente significa morte física — quase sempre significa a morte de uma identidade, relacionamento, ou forma de vida. Pergunta central: o que precisa morrer em você para que algo novo possa nascer?\n\nA TEMPERANÇA (XIV): equilíbrio, paciência, mistura cuidadosa de opostos, alquimia interior. Pergunta central: que extremos em sua vida precisam ser integrados?\n\nO DIABO (XV): ilusão de prisão, sombra, vícios, apego a coisas que nos limitam. Note na imagem do Rider-Waite: as correntes dos cativos são soltas o suficiente para que eles possam se libertar — eles ficam por escolha. Pergunta central: a que você está preso que na verdade não te prende?\n\nA TORRE (XVI): ruptura súbita, revelação que desaba estruturas falsas, libertação violenta de algo que precisava cair. É a carta mais temida mas frequentemente a mais libertadora. Pergunta central: que estrutura em sua vida está sendo desafiada porque era baseada em algo falso?\n\nA ESTRELA (XVII): esperança, renovação, cura, conexão com o divino após a escuridão. Depois da Torre, a Estrela. Sempre positiva: você está sendo renovado. Pergunta central: onde está a esperança que você ainda não permite ver?\n\nA LUA (XVIII): ilusão, medo, o inconsciente que emerge, o caminho tortuoso que deve ser navegado com intuição mais do que razão. Pergunta central: que medo ou ilusão está distorcendo sua percepção da realidade?\n\nO SOL (XIX): alegria, clareza, sucesso, vitalidade, a criança que sabe brincar. Sempre positiva: luz, transparência, vida plena. Pergunta central: onde você está proibindo a si mesmo de sentir alegria?\n\nO JULGAMENTO (XX): chamada, despertar, transformação final antes da conclusão, avaliação honesta de si mesmo. Pergunta central: qual chamada em sua vida você tem ignorado?\n\nO MUNDO (XXI): completude, integração, celebração do ciclo completo, síntese de tudo que foi aprendido. E então o ciclo recomeça com O Louco. Sempre positiva: você chegou num ponto de completude. Pergunta central: o que em sua vida está chegando a uma conclusão digna de celebração?",
        "exemplo": "A Torre aparece numa tiragem sobre um casamento em crise. O leitor inexperiente teme. O experiente diz: 'O que está sendo sacudido aqui não é o amor — é a estrutura que vocês construíram em torno do amor que talvez não seja mais verdadeira. A Torre não destrói o que é real. O que vai ficar de pé depois é o que merece ficar.'",
        "aplicacao": "1. Memorize as onze cartas desta aula. 2. Note as cartas difíceis (Morte, Diabo, Torre, Lua) e como cada uma tem uma face transformadora além do aspecto temível. 3. Complete a sequência da Jornada do Louco na sua mente.",
        "exercicio": "Leia a sequência completa da Jornada do Louco (0 ao XXI) como se fosse uma história. Onde você está nessa jornada agora? Em qual carta você se reconhece?",
        "gabarito": "A Jornada do Louco não é linear — voltamos às mesmas cartas em espiral, sempre em um nível mais profundo. Você pode estar na Morte pela terceira vez na vida, mas cada vez é uma transformação diferente, mais profunda."
      },
      "4": {
        "titulo": "Os Arcanos Menores — Os Quatro Naipes",
        "conteudo": "Os Arcanos Menores descrevem as experiências cotidianas da vida. Enquanto os Maiores lidam com forças arquetípicas universais, os Menores lidam com o que acontece dia a dia — conversas, dinheiro, sentimentos, conflitos, decisões.\n\nAS CARTAS DE ÁS representam o puro potencial de cada naipe, a semente antes de qualquer desenvolvimento:\n- Ás de Paus: centelha criativa, nova inspiração, o início de um projeto com entusiasmo genuíno\n- Ás de Copas: novo amor, abertura emocional, um coração que recomeça\n- Ás de Espadas: clareza cortante, verdade revelada, novo insight\n- Ás de Ouros: nova oportunidade material, semente de prosperidade\n\nAS CARTAS DE 2 AO 10 narram uma progressão:\n- 2: equilíbrio inicial, escolha entre dois caminhos\n- 3: expansão, criatividade, resultado inicial das sementes plantadas\n- 4: estabilidade, descanso, consolidação\n- 5: desafio, conflito, perda temporária\n- 6: harmonia recuperada, presente, generosidade\n- 7: reflexão, estratégia, autoexame\n- 8: movimento rápido, poder em ação, mudanças\n- 9: quase lá, intensidade antes do final, o pico da jornada do naipe\n- 10: conclusão, completude, fim de um ciclo (pode ser fardo ou realização dependendo do naipe)\n\nEXEMPLOS POR NAIPE:\n10 de Paus: fardo excessivo, carregar responsabilidades demais — é hora de delegar\n10 de Copas: família em harmonia, felicidade emocional completa — realização\n10 de Espadas: derrota aparente, fundo do poço — mas o sol está nascendo ao fundo da imagem\n10 de Ouros: riqueza duradoura, legado familiar, abundância consolidada\n\nAS CARTAS DA CORTE representam aspectos de personalidade (partes de você) ou pessoas reais em sua vida:\n- VALETE: energia jovem, aprendiz, mensagens, início de algo\n- CAVALEIRO: ação, movimento, excesso da energia do naipe\n- RAINHA: domínio maduro da energia interior do naipe\n- REI: domínio maduro da energia exterior e de liderança do naipe",
        "exemplo": "3 de Espadas — a carta com três espadas atravessando um coração sob chuva. É uma das cartas mais literalmente dolorosas do baralho. Significa: dor emocional real, tristeza, separação, decepção. Um bom leitor não ameniza: 'Isso dói. A carta não mente. Mas observe: a chuva passa. E dor processada honestamente é a que liberta.'",
        "aplicacao": "1. Familiarize-se com a progressão numérica em cada naipe. 2. Compare a mesma posição numérica nos quatro naipes — o 5 de Paus (luta física/competição) vs o 5 de Copas (perda emocional) vs o 5 de Espadas (conflito mental) vs o 5 de Ouros (dificuldade material). 3. Pratique com as cartas da corte — qual Rainha você é? Qual Rei?",
        "exercicio": "Separe todos os Ases. Para cada um, escreva: que novo começo esse naipe representa na sua vida agora? Há uma centelha de Paus, uma abertura de Copas, uma clareza de Espadas ou uma oportunidade de Ouros chegando?",
        "gabarito": "Os Arcanos Menores ganham profundidade quando você percebe as progressões. O 5 sempre traz desafio — mas o 6 sempre traz recuperação. Saber disso numa leitura permite oferecer contexto: 'Você está no 5, mas o 6 está a caminho se você...'"
      },
      "5": {
        "titulo": "Métodos de Tiragem — Do Simples ao Complexo",
        "conteudo": "A CARTA DO DIA é o método mais simples e poderoso para quem está aprendendo. Tire uma carta pela manhã e carregue a questão que ela levanta durante o dia. À noite, reflita: como essa energia se manifestou? Esse exercício, feito por 30 dias consecutivos, desenvolve mais intuição do que anos de estudo teórico.\n\nA TIRAGEM DE TRÊS CARTAS é a mais versátil:\n- Passado / Presente / Futuro\n- Situação / Conselho / Resultado\n- Mente / Corpo / Espírito\n- Você / O Outro / A Relação\n- O Problema / A Causa / A Solução\n\nA CRUZ CELTA é o layout mais tradicional e completo, com 10 cartas:\n1. A situação central\n2. O que cruza (obstáculo ou apoio)\n3. O que está abaixo (fundação, o que você não vê)\n4. O que ficou para trás\n5. O que pode vir\n6. O que está à frente imediatamente\n7. Como você se vê\n8. Como os outros te veem\n9. Esperanças e medos\n10. O resultado mais provável\n\nA TIRAGEM DA LUA (especial para questões emocionais e relacionamentos):\n1. Onde você está emocionalmente agora\n2. O que está oculto no inconsciente\n3. O que o coração realmente quer\n4. O que a mente diz\n5. O que está impedindo\n6. O que pode ser feito\n7. O resultado se seguir o coração\n\nA LEITURA INVERTIDA: quando uma carta aparece de cabeça para baixo, pode significar: energia bloqueada ou interiorizada, resistência a essa energia, ou o aspecto shadow da carta. Não há consenso entre leitores — alguns não leem invertidas; outros as consideram essenciais. Experimente os dois sistemas e veja qual ressoa mais com você.\n\nO DIÁRIO DE TAROT: manter um caderno onde você registra cada tiragem, sua interpretação inicial e depois o que realmente aconteceu é o método mais eficaz de aprendizado. Com o tempo, você cria seu próprio sistema de referências baseado na experiência real.",
        "exemplo": "Uma leitora faz uma Cruz Celta para entender por que não consegue avançar num projeto criativo. A posição 3 (o que está abaixo, fundação oculta) revela O Enforcado — ela está se suspendendo voluntariamente, esperando algo (talvez permissão) que nunca vai chegar de fora. A posição 7 (como ela se vê) revela O Eremita. A integração: ela se vê como alguém que precisa de mais preparação e isolamento, mas na verdade está usando a introspecção como desculpa para não agir.",
        "aplicacao": "1. Comece com carta do dia por 30 dias. 2. Depois pratique tiragem de 3 cartas para situações reais. 3. Experimente a Cruz Celta apenas quando estiver confortável com as cartas individuais. 4. Mantenha diário.",
        "exercicio": "Faça uma tiragem de três cartas para uma situação real: Situação-Conselho-Resultado. Fotografe ou escreva as cartas. Escreva sua interpretação. Em duas semanas, volte e compare com o que aconteceu.",
        "gabarito": "Uma tiragem bem feita não diz o que vai acontecer — orienta sobre energias presentes e possíveis caminhos. O resultado muda conforme as escolhas. O Tarô mapeia possibilidades, não fatalidades."
      },
      "6": {
        "titulo": "Intuição no Tarô — Além das Definições",
        "conteudo": "Memorizar os significados das 78 cartas é apenas o primeiro nível de aprendizado no Tarô. O segundo nível — e o mais poderoso — é desenvolver a leitura intuitiva: a capacidade de olhar para uma carta dentro de um contexto específico e deixar que ela fale além das definições tradicionais.\n\nO MÉTODO INTUITIVO começa com a imagem: antes de pensar no significado aprendido, olhe para a imagem. O que você vê? Que emoção a imagem evoca? Que personagem na carta chama mais sua atenção? Onde seus olhos vão primeiro? Essas respostas são frequentemente mais relevantes para a pessoa à sua frente do que o significado genérico.\n\nO CONTEXTO TRANSFORMA O SIGNIFICADO: a Morte numa pergunta sobre saúde tem uma qualidade diferente do que a Morte numa pergunta sobre carreira. O contexto restringe e aprofunda o significado. A Lua para alguém perguntando sobre criatividade fala de imaginação e sonho; para alguém perguntando sobre relacionamento, fala de ilusão e projeção.\n\nA CONVERSA COM O CONSULTANTE: as melhores leituras não são monólogos — são diálogos. Perguntar 'o que essa imagem te faz pensar?' ou 'alguém específico vem à mente quando você vê essa carta?' frequentemente revela a camada mais profunda da leitura. O consultante sempre sabe mais do que você sobre a situação dele.\n\nAS COMBINAÇÕES ENTRE CARTAS: na Cruz Celta ou qualquer layout com múltiplas cartas, as cartas conversam entre si. Duas cartas de Espadas juntas amplificam o tema mental/conflitual. Uma carta de Copas entre duas de Espadas pode indicar emoções no meio de um conflito intelectual. Aprender a ver padrões entre cartas é o nível avançado.\n\nO DESCONFORTO HONESTO: algumas cartas são difíceis de entregar. A Torre para alguém que acabou de se casar. A Morte para alguém doente. O Diabo para alguém que acredita muito em si mesmo. O leitor experiente não evita essas cartas — ele encontra a forma honesta e compassiva de entregá-las. Omitir informação importante para não desconfortar é uma forma de desrespeito ao consultante.\n\nA CONFIANÇA NO PROCESSO: com o tempo, muitos leitores de Tarô descrevem uma experiência que vai além do conhecimento — uma sensação de que certas palavras simplesmente 'vêm' durante uma leitura, ou que certas cartas parecem 'querer' ser lidas de determinada forma naquele contexto. Isso pode ser chamado de intuição, inconsciente, conexão espiritual — o nome importa menos que cultivar essa abertura.",
        "exemplo": "Um leitor faz uma tiragem para uma mulher sobre sua carreira. Ele tira A Imperatriz, e em vez de citar a definição clássica ('fertilidade, abundância, criatividade'), ele olha para a imagem e diz: 'Vejo uma mulher que tem tudo para nutrir e criar, mas que está confortavelmente sentada em seu trono quando o terreno ao redor dela está pedindo que ela se levante e plante.' A mulher chora: é exatamente o que está acontecendo — ela tem potencial mas está esperando as condições perfeitas para agir.",
        "aplicacao": "1. Para cada nova carta que estuda, passe 2 minutos olhando apenas para a imagem antes de ler o significado. 2. Numa leitura real, diga o que a imagem te faz sentir ANTES de citar o significado aprendido. 3. Convide o consultante a participar.",
        "exercicio": "Tire uma carta agora. Antes de pensar no significado, olhe para a imagem por 1 minuto. Escreva tudo que você observa e que emoção ela evoca. Depois leia o significado tradicional. Que diferenças há entre sua leitura intuitiva e a definição? O que sua leitura acrescentou?",
        "gabarito": "Leituras intuitivas frequentemente captam nuances que as definições clássicas não cobrem. O objetivo não é substituir o conhecimento — é integrá-lo com percepção direta. As melhores leituras combinam os dois."
      },
      "7": {
        "titulo": "Ética e Responsabilidade na Leitura do Tarô",
        "conteudo": "Ler Tarô para outros é um ato de responsabilidade. As pessoas que procuram leituras frequentemente estão em momentos de vulnerabilidade, indecisão ou dor. O que um leitor diz — e como diz — tem impacto real.\n\nNUNCA FAÇA PREVISÕES ABSOLUTAS: 'Você vai se separar' ou 'Esse negócio vai falir' são afirmações irresponsáveis que podem criar profecias autocumpridas ou gerar ansiedade desnecessária. O Tarô mostra tendências, não fatalidades. A linguagem correta: 'As energias presentes sugerem...', 'Há uma tendência para...', 'Se nada mudar, a direção parece ser...'.\n\nNÃO SUBSTITUA AJUDA PROFISSIONAL: se alguém chega com sinais claros de depressão grave, pensamentos autodestrutivos, ou situação de abuso, o Tarô não é a ferramenta adequada como única resposta. O leitor responsável reconhece seus limites e direciona para ajuda profissional quando necessário.\n\nCONFIDENCIALIDADE: o que se compartilha numa leitura é privado. Usar informações de uma leitura para fofoca ou para impressionar outros é uma violação ética grave.\n\nO CÓDIGO DAS TRÊS ÉTICAS do Tarô, como proposto por Rachel Pollack: (1) O consultante tem o direito de saber o que as cartas mostram. (2) O consultante tem o direito de não saber se preferir. (3) O leitor tem o dever de entregar informações difíceis de forma responsável.\n\nLEITURAS PARA TERCEIROS: ler cartas sobre outra pessoa (sem sua presença ou conhecimento) é eticamente questionável. Você está analisando alguém que não deu permissão. Se fizer isso, mantenha o foco em ajudar o consultante a entender a dinâmica, não em 'expor' o terceiro.\n\nSEU PRÓPRIO ESTADO EMOCIONAL: não leia para outros quando estiver em estado emocional muito carregado. Sua perturbação afeta a leitura — tanto a clareza da interpretação quanto a qualidade da presença que você oferece. E seja cuidadoso ao ler para si mesmo sobre situações em que você está muito investido emocionalmente — é muito fácil ver o que quer ver.",
        "exemplo": "Uma cliente pede uma leitura sobre se deve se separar do marido. Um leitor ético não diz 'as cartas dizem para se separar' — isso seria tirar uma decisão vital das mãos dela. Ele usa as cartas para ajudá-la a clarificar o que ela já sente: 'O que as cartas mostram sobre como você se sente nessa relação? O que elas mostram sobre o que você mais teme? O que elas dizem sobre o que você realmente quer?'",
        "aplicacao": "1. Defina sua própria política de leituras — o que você lê, para quem, e como. 2. Desenvolva um 'protocolo de acolhimento' para começar uma leitura criando um espaço seguro. 3. Pratique a linguagem de possibilidade vs certeza.",
        "exercicio": "Escreva 5 exemplos de afirmações problemáticas e reformule cada uma de forma responsável. Ex: 'Você vai ter problemas de saúde' → 'Há uma energia pedindo mais atenção ao corpo e ao descanso neste período.'",
        "gabarito": "A reformulação responsável mantém a honestidade sem criar fatalismo. 'Há tendência para X se Y não mudar' é sempre mais útil do que 'X vai acontecer'. O objetivo é empoderar, não assustar."
      },
      "8": {
        "titulo": "Desenvolvendo seu Estilo de Leitura",
        "conteudo": "Depois de aprender os fundamentos, o próximo passo é desenvolver seu estilo único de leitura. Cada leitor é diferente — e a tentativa de imitar outro leitor produz leituras mecânicas e sem vida.\n\nENCONTRE SEU BARALHO: o baralho de Rider-Waite é a base de ensino, mas não precisa ser o baralho com o qual você lê. Explore diferentes baralhos até encontrar um cujas imagens falam diretamente à sua intuição. Alguns preferem o Thoth Tarot (mais hermético e simbólico), outros o Tarot de Marselha (mais antigo, sem cenas nas cartas menores), outros baralhos modernos com estilos variados.\n\nDEFINA SUA ABORDAGEM FILOSÓFICA: você lê Tarô como ferramenta psicológica, como sistema espiritual, como tradição esotérica, ou como uma combinação? Não há resposta certa — mas clareza sobre sua própria abordagem torna as leituras mais coesas.\n\nDESENVOLVA RITUAIS DE PREPARAÇÃO: muitos leitores têm um ritual simples antes de uma leitura — embaralhar as cartas de uma forma específica, um momento de silêncio, uma vela, uma pergunta mental de intenção. Esses rituais não são superstição — são ferramentas de foco que criam um estado mental propício para a leitura.\n\nAPRECIE AS CARTAS DIFÍCEIS: os leitores que mais crescem são os que aprendem a amar as cartas que antes temiam. A Torre, o Diabo, a Morte, o Dez de Espadas — cada uma dessas cartas, quando entendida profundamente, torna-se uma aliada poderosa. Elas aparecem quando são necessárias.\n\nESTUDE OS SISTEMAS CONECTADOS: o Tarô está profundamente conectado à Cabala, à astrologia e à numerologia. Os Arcanos Maiores correspondem a caminhos na Árvore da Vida cabalística. Cada naipe corresponde a um elemento astrológico. Cada número tem um significado numerológico. Esses sistemas se iluminam mutuamente.\n\nA JORNADA NUNCA TERMINA: praticantes com décadas de experiência continuam descobrindo novas camadas nas mesmas cartas. O Tarô é um sistema suficientemente rico para durar uma vida inteira de exploração. Cada fase da sua vida ilumina as cartas de uma nova forma — e as cartas iluminam cada fase.",
        "exemplo": "Uma leitora com 10 anos de experiência conta que só entendeu O Enforcado de verdade quando passou por uma fase de sua própria vida onde precisou parar, esperar e mudar completamente de perspectiva. 'Antes eu ensinava o Enforcado. Depois de vivê-lo, passei a sentir o Enforcado nas leituras. Essa é a diferença entre saber e compreender.'",
        "aplicacao": "1. Experimente pelo menos 3 baralhos diferentes. 2. Defina sua abordagem filosófica em uma frase. 3. Crie um ritual simples de preparação para leituras. 4. Escolha uma carta com a qual você tem dificuldade e passe um mês estudando apenas ela.",
        "exercicio": "Escreva sua 'declaração de intenção' como leitora/leitor de Tarô: por que você lê? Para quem? Com que objetivo? Que valores guiam sua prática? Esse texto se torna sua âncora ética e filosófica.",
        "gabarito": "Não há estilo certo de leitura — há estilos mais ou menos alinhados com quem você é e com o que você quer oferecer. A consistência entre seus valores, sua abordagem e sua prática é o que cria um leitor em quem as pessoas confiam."
      }
    }
  },
  "astrologia": {
    "titulo": "Astrologia — A Linguagem dos Astros",
    "descricao": "A astrologia é um dos mais antigos sistemas de autoconhecimento da humanidade. Aprenda a ler um mapa astral, entender os doze signos, os planetas e as casas astrológicas.",
    "icone": "⭐",
    "total_aulas": 6,
    "aulas": {
      "1": {
        "titulo": "O que é Astrologia e como funciona",
        "conteudo": "A astrologia é o estudo da relação entre as posições dos corpos celestes e os padrões da vida humana. Suas raízes remontam à Mesopotâmia, há mais de 4.000 anos, e ela é encontrada em praticamente todas as grandes civilizações — babilônica, egípcia, grega, romana, indiana (Jyotish) e chinesa. A versão ocidental que conhecemos hoje é uma síntese greco-romana desenvolvida entre 400 a.C. e 200 d.C.\n\nA PREMISSA FUNDAMENTAL da astrologia não é que os planetas 'causam' eventos — é que o cosmo e a vida humana são espelhos um do outro, seguindo os mesmos padrões. Como escreveu Hermes Trismegisto: 'Como é em cima, é embaixo; como é embaixo, é em cima.' Os planetas não determinam — eles indicam energias e tendências que se manifestam tanto no céu quanto na Terra.\n\nO MAPA NATAL (ou Mapa Astral) é uma fotografia do céu no exato momento e lugar do nascimento de uma pessoa. É um círculo dividido em 12 casas, com os 10 planetas posicionados nos 12 signos. A interpretação desse mapa revela a personalidade, os talentos, os desafios, os padrões relacionais e a trajetória de vida da pessoa.\n\nOs ELEMENTOS FUNDAMENTAIS do mapa são três: os PLANETAS (o que), os SIGNOS (como) e as CASAS (onde). Por exemplo: Marte (o que — ação, energia, desejo) em Escorpião (como — intenso, obsessivo, transformador) na 7ª Casa (onde — nos relacionamentos). Leitura: a pessoa age de forma intensa e transformadora especialmente nos relacionamentos.\n\nOs ASPECTOS são os ângulos entre planetas no mapa — as relações entre eles. Uma conjunção (planetas próximos) intensifica as energias. Uma oposição cria tensão. Um trígono facilita o fluxo. Um quadrado cria atrito que produz força. Um sextil cria oportunidade.\n\nA DIFERENÇA entre a astrologia solar (dos horóscopos de jornal) e a astrologia completa é enorme. O signo solar — o que a maioria das pessoas conhece — é apenas um dos muitos elementos do mapa. É como julgar uma sinfonia pela nota de abertura.",
        "exemplo": "Dois Áries completamente diferentes: um tem Lua em Câncer e Ascendente em Peixes — por baixo da energia aguerrida de Áries há uma sensibilidade emocional profunda e uma presença suave. O outro tem Lua em Escorpião e Ascendente em Capricórnio — a energia de Áries é amplificada por intensidade emocional e ambição estruturada. O signo solar sozinho não conta a história completa.",
        "aplicacao": "1. Calcule seu mapa natal (use Astro.com, gratuito, com data, hora e cidade de nascimento). 2. Identifique seu signo solar, lunar e ascendente. 3. Observe onde estão os planetas nos signos. 4. Familiarize-se com a estrutura das 12 casas.",
        "exercicio": "Calcule seu mapa natal completo agora. Identifique: signo solar, signo lunar, ascendente. São harmônicos (do mesmo elemento) ou contrastantes? O que isso sugere sobre possíveis tensões internas?",
        "gabarito": "Quando solar, lunar e ascendente são do mesmo elemento (ex: Áries, Leão, Sagitário — todos Fogo), há harmonia e clareza de identidade mas possível falta de equilíbrio. Quando são de elementos contrastantes (ex: Touro, Aquário, Escorpião), há maior complexidade e possível sensação de divisão interna."
      },
      "2": {
        "titulo": "Os Doze Signos — Arquétipos do Zodíaco",
        "conteudo": "ÁRIES (Fogo, Cardinal, Marte): o pioneiro, o guerreiro, o iniciador. Energia: ação direta, coragem, impulsividade, liderança instintiva. Desafio: impaciência, incapacidade de terminar o que começa, ego inflado. Dom: capacidade de iniciar o que outros não ousam começar.\n\nTOURO (Terra, Fixo, Vênus): o cultivador, o construtor de valores. Energia: sensualidade, estabilidade, determinação, amor pela beleza e pelo conforto. Desafio: teimosia, resistência à mudança, possessividade. Dom: perseverança e capacidade de criar valor duradouro.\n\nGÊMEOS (Ar, Mutável, Mercúrio): o comunicador, o eterno curioso. Energia: versatilidade, comunicação, curiosidade, habilidade de ver múltiplos lados. Desafio: superficialidade, dificuldade de comprometimento, ansiedade. Dom: adaptabilidade e capacidade de conectar ideias e pessoas.\n\nCÂNCER (Água, Cardinal, Lua): o nutrido, o guardião do lar. Energia: sensibilidade, memória emocional, cuidado, intuição, lealdade. Desafio: humor instável, dependência emocional, rancor que não libera. Dom: profunda empatia e capacidade de criar segurança para outros.\n\nLEÃO (Fogo, Fixo, Sol): o criador, o rei/rainha. Energia: criatividade, generosidade, carisma, necessidade de expressão e reconhecimento. Desafio: ego, necessidade de aprovação, dramaturgia. Dom: capacidade de inspirar e iluminar os outros.\n\nVIRGEM (Terra, Mutável, Mercúrio): o analista, o servidor dedicado. Energia: análise, precisão, serviço, atenção ao detalhe, pragmatismo. Desafio: perfeccionismo que paralisa, autocrítica excessiva, ansiedade. Dom: capacidade de ver o que precisa ser melhorado e de servir com excelência.\n\nLIBRA (Ar, Cardinal, Vênus): o diplomata, o buscador de harmonia. Energia: equilíbrio, beleza, relacionamentos, justiça, parceria. Desafio: indecisão, dependência do outro, aversão ao conflito que vira desonestidade. Dom: capacidade única de ver todos os lados e criar harmonia.\n\nESCORPIÃO (Água, Fixo, Plutão/Marte): o transformador, o mergulhador nas profundezas. Energia: intensidade, poder, transformação, lealdade absoluta, capacidade de ir ao fundo de qualquer questão. Desafio: controle, obsessão, rancor, manipulação. Dom: capacidade de morrer e renascer, de transformar o mais sombrio em ouro.\n\nSAGITÁRIO (Fogo, Mutável, Júpiter): o filósofo, o explorador. Energia: expansão, otimismo, busca por significado, aventura, visão de futuro. Desafio: irresponsabilidade, excesso de promessas, dogmatismo disfarçado de abertura. Dom: capacidade de enxergar além do imediato e inspirar esperança.\n\nCAPRICÓRNIO (Terra, Cardinal, Saturno): o realizador, o construtor de legados. Energia: ambição, disciplina, responsabilidade, estrutura, maturidade. Desafio: frieza emocional, workaholic, rigidez, medo do fracasso. Dom: capacidade de construir estruturas que duram além de uma vida.\n\nAQUÁRIO (Ar, Fixo, Urano/Saturno): o visionário, o rebelde. Energia: originalidade, pensamento inovador, humanitarismo, desapego. Desafio: frieza emocional, rebeldia pela rebeldia, desconexão com o individual em nome do coletivo. Dom: capacidade de ver o futuro e de criar novas formas de organização humana.\n\nPEIXES (Água, Mutável, Netuno/Júpiter): o místico, o dissoluto. Energia: compaixão, espiritualidade, criatividade, empatia universal, dissolução de fronteiras. Desafio: fuga da realidade, dificuldade de limites, vitimização. Dom: capacidade de conexão espiritual e de compaixão que transcende o ego.",
        "exemplo": "Uma pessoa com Sol em Capricórnio, Lua em Câncer e Ascendente em Leão vive uma tríade fascinante e tensa: a ambição estruturada e séria de Capricórnio (Solar) com uma vida emocional profundamente ligada ao lar e à família (Lunar Câncer), mas projetando para o mundo uma presença calorosa, criativa e que quer ser admirada (Ascendente Leão). Essa pessoa trabalha muito (Capricórnio), precisa de segurança emocional para funcionar (Câncer), mas precisa também brilhar e ser reconhecida (Leão).",
        "aplicacao": "1. Leia com atenção seu signo solar, lunar e ascendente. 2. Para cada um, identifique os dons e os desafios. 3. Perceba como esses três aspectos interagem na sua vida. 4. Identifique qual dos três parece mais dominante no seu dia a dia.",
        "exercicio": "Para cada um dos seus três signos principais, escreva um exemplo concreto de como aquela energia se manifesta positivamente na sua vida, e um exemplo de como o desafio daquele signo aparece.",
        "gabarito": "Reconhecer os desafios dos próprios signos sem julgamento é o passo mais difícil e mais libertador. Um Escorpião que reconhece a tendência ao controle pode trabalhar conscientemente com ela. Um Gêmeos que reconhece a dispersão pode criar estruturas para compensar."
      },
      "3": {
        "titulo": "Os Planetas — Vozes do Mapa",
        "conteudo": "Cada planeta representa uma função psicológica, uma 'voz' dentro da psique humana. A posição do planeta no signo diz como essa função se expressa; a posição na casa diz em qual área da vida ela atua.\n\nSOL: a identidade central, o ego, a vontade criativa. O que você está aqui para ser. O signo solar é a qualidade que você está desenvolvendo ao longo de toda a vida — não é o que você nasceu sendo, mas o que está se tornando.\n\nLUA: o mundo emocional, os instintos, as necessidades de segurança, o passado, a infância, a mãe. O signo lunar revela como você reage emocionalmente, o que te faz sentir seguro ou ameaçado, e como seu mundo interior funciona.\n\nMERCÚRIO: a mente, a comunicação, a forma de pensar e de processar informação. Revela se você pensa de forma linear ou associativa, se se comunica de forma direta ou indireta.\n\nVÊNUS: amor, beleza, valores, prazer, relacionamentos, o que te atrai e o que você acha belo. Revela o que você busca em relacionamentos e em experiências estéticas.\n\nMART: ação, desejo, energia, sexualidade, agressividade. Como você age para conseguir o que quer. Onde você coloca sua energia e força.\n\nJÚPITER: expansão, abundância, oportunidade, sabedoria, filosofia. Onde a vida tende a se expandir e oferecer oportunidades — mas também onde o excesso pode aparecer.\n\nSATURNO: limitação, disciplina, responsabilidade, karma, estrutura, medos profundos. Onde a vida exige mais esforço e onde as maiores conquistas são construídas através da perseverança. Saturno é severo mas justo.\n\nURANO: revolução, originalidade, ruptura súbita, liberdade, o futuro. Onde você é rebelde e onde rupturas são necessárias para crescimento.\n\nNETUNO: espiritualidade, ilusão, dissolução, sonhos, compaixão universal, o inconsciente coletivo. Onde você busca o transcendente — e onde pode se iludir.\n\nPLUTÃO: transformação profunda, poder, morte e renascimento, o inconsciente mais profundo. Onde você experimenta as transformações mais radicais da vida.",
        "exemplo": "Saturno em Câncer na 4ª Casa: a função de Saturno (disciplina, responsabilidade, medo, construção lenta) expressa de forma canceriana (emocional, ligada ao lar, cuidadora) na área da família e lar (4ª Casa). Provável: responsabilidades familiares pesadas desde cedo, relação com a família que exigiu muito, dificuldade de sentir segurança emocional — mas também, quando trabalhado, capacidade de construir uma base familiar extraordinariamente sólida.",
        "aplicacao": "1. No seu mapa natal, identifique a posição de cada planeta. 2. Para os planetas pessoais (Sol, Lua, Mercúrio, Vênus, Marte), leia signo e casa. 3. Para Saturno especificamente, leia com atenção — ele revela onde está o maior trabalho e a maior recompensa.",
        "exercicio": "Onde está Saturno no seu mapa? Em qual signo e em qual casa? Esse posicionamento ressoa com os desafios e aprendizados mais constantes da sua vida?",
        "gabarito": "Saturno é frequentemente o planeta que mais ressoa com a experiência real de vida porque ele descreve os padrões de dificuldade que retornam até serem dominados. Saturno em Gêmeos pode indicar dificuldade de comunicação ou aprendizado difícil; Saturno em Escorpião pode indicar lutas com poder e transformação."
      },
      "4": {
        "titulo": "As Doze Casas Astrológicas",
        "conteudo": "As 12 casas do mapa natal representam as 12 áreas da vida onde os planetas e signos atuam. Elas são determinadas pelo horário e local de nascimento — por isso o mesmo Sol em Áries de duas pessoas pode manifestar-se de formas muito diferentes dependendo de em qual casa ele está.\n\n1ª CASA (Ascendente): identidade, aparência, como você se apresenta ao mundo, a máscara social, o início de tudo. O signo na cúspide da 1ª casa é o Ascendente — a impressão imediata que você passa.\n\n2ª CASA: valores, recursos pessoais, dinheiro, posses, autoestima. Como você ganha e gasta. O que você considera valioso.\n\n3ª CASA: comunicação, irmãos, vizinhança, aprendizado básico, viagens curtas, mente cotidiana. Como você pensa e se comunica no dia a dia.\n\n4ª CASA (Fundo do Céu): lar, família de origem, raízes, o que está na base de tudo, a vida privada. A mãe ou figura materna.\n\n5ª CASA: criatividade, prazer, filhos, amor romântico (diferente de parceria), jogo, autoexpressão espontânea. Onde você se diverte e cria.\n\n6ª CASA: trabalho cotidiano (diferente de carreira), saúde, rotinas, serviço, os pequenos hábitos que constroem a vida.\n\n7ª CASA (Descendente): parcerias, casamento, contratos, o que você busca no outro, como são seus relacionamentos sérios. O oposto do Ascendente — o que você precisa do outro para se completar.\n\n8ª CASA: transformação, morte e renascimento, sexualidade profunda, heranças, recursos compartilhados, o que é oculto, o inconsciente.\n\n9ª CASA: filosofia, espiritualidade, viagens longas, ensino superior, busca por significado, o pai ou figura paterna, crenças expansivas.\n\n10ª CASA (Meio do Céu): carreira, reputação pública, status, autoridade, o que você quer conquistar no mundo. Como você é visto profissionalmente.\n\n11ª CASA: amizades, grupos, coletivo, causas, esperanças, o futuro, redes de apoio.\n\n12ª CASA: o inconsciente profundo, o que está oculto, padrões kármicos, isolamento, espiritualidade, o que precisa ser liberado.",
        "exemplo": "Sol na 12ª Casa: a identidade central (Sol) expressa-se no domínio do que está oculto, do inconsciente e do espiritual (12ª Casa). Frequentemente indica alguém que prefere trabalhar nos bastidores, que tem dificuldade de brilhar publicamente mesmo com grande talento, e que tem uma vida espiritual ou psicológica rica. Muitos monges, artistas reclusisos e terapeutas têm Sol na 12ª Casa.",
        "aplicacao": "1. Identifique em qual casa está cada planeta pessoal no seu mapa. 2. Para cada planeta em casa, combine: função do planeta + qualidade do signo + área da casa. 3. Identifique suas casas mais cheias (com vários planetas) — elas indicam as áreas mais ativas da sua vida.",
        "exercicio": "Identifique as três casas mais cheias do seu mapa. Essas áreas da vida são realmente as mais ativas, complexas ou significativas para você? Como se manifestam?",
        "gabarito": "Casas com muitos planetas são áreas de muito movimento, aprendizado e atividade. Casas vazias não são problemas — são áreas de menor foco, onde a vida flui mais simplesmente. Todos temos casas cheias e casas vazias."
      },
      "5": {
        "titulo": "Trânsitos e Progressões — A Astrologia do Tempo",
        "conteudo": "O mapa natal é fixo — uma fotografia do nascimento. Mas os planetas continuam se movendo após o nascimento, e quando eles transitam sobre pontos do mapa natal, ativam aquelas energias. Isso é a astrologia preditiva ou de timing.\n\nOS TRÂNSITOS são as posições dos planetas no céu hoje, comparadas com seu mapa natal. Quando Saturno transita sobre seu Sol natal, você entra numa fase de responsabilidades, limitações e maturidade forçada — dura aproximadamente 2 anos. Quando Júpiter transita sobre seu Sol, você entra numa fase de expansão, oportunidades e otimismo — dura cerca de 1 ano.\n\nOs PLANETAS LENTOS (Saturno, Urano, Netuno, Plutão) criam os trânsitos mais impactantes porque ficam mais tempo sobre cada ponto e ativam transformações profundas e duradouras. Os planetas rápidos (Sol, Lua, Mercúrio, Vênus, Marte) criam ativações menores e mais passageiras.\n\nO RETORNO DE SATURNO acontece quando Saturno volta à mesma posição que ocupava no nascimento — o que acontece aproximadamente aos 29-30 anos, 58-60 anos e 87-90 anos. É uma das grandes iniciações da vida: Saturno apresenta a conta das escolhas feitas e força uma reavaliação profunda. Os 'crises dos 30' que muitas pessoas descrevem são frequentemente o Retorno de Saturno.\n\nO RETORNO SOLAR acontece todo ano, quando o Sol volta à mesma posição do nascimento. O aniversário, basicamente. Um mapa do Retorno Solar (calculado para o momento exato em que o Sol retorna à posição natal) revela os temas do ano que se inicia.\n\nAS PROGRESSÕES são um sistema diferente onde o mapa natal 'avança' simbolicamente — um dia depois do nascimento equivale a um ano de vida. As progressões revelam o desenvolvimento interno, mais lento e profundo do que os trânsitos.",
        "exemplo": "Uma mulher passa por uma crise existencial profunda aos 29 anos: fim de relacionamento longo, questionamento da carreira, sensação de que tudo que construiu não é mais suficiente. O mapa mostra Saturno transitando exatamente sobre seu Sol natal — o Retorno de Saturno clássico. A astrologia nomeia e contextualiza: não é crise, é iniciação. Saturno está pedindo que ela construa sua vida sobre bases mais verdadeiras.",
        "aplicacao": "1. Verifique onde Saturno está no céu hoje e em qual posição do seu mapa ele está transitando. 2. Se você tem entre 28-30, 57-60 ou 86-89 anos, você está num Retorno de Saturno. 3. Use sites como Astro.com (seção de trânsitos) para visualizar os trânsitos atuais no seu mapa.",
        "exercicio": "Pesquise os trânsitos atuais dos planetas lentos (Saturno, Urano, Netuno, Plutão) no seu mapa natal. Em qual casa cada um está? Esses temas de vida estão ativos agora?",
        "gabarito": "Os trânsitos não causam eventos — eles descrevem energias que estão presentes. Plutão transitando pela 7ª Casa não significa que seu casamento vai acabar — significa que as relações estão passando por transformação profunda. Como essa transformação se manifesta depende de muitos fatores, incluindo suas escolhas."
      },
      "6": {
        "titulo": "Lendo um Mapa Astral — Integrando Tudo",
        "conteudo": "Uma leitura astrológica completa integra todos os elementos estudados numa narrativa coerente sobre quem a pessoa é, qual é sua jornada e em que momento ela está.\n\nO PROCESSO DE LEITURA começa com a impressão geral: qual elemento domina (Fogo, Terra, Ar ou Água)? Qual modalidade (Cardinal, Fixo ou Mutável)? Há um desequilíbrio óbvio (todos os planetas num lado do mapa, muitos em certas casas, elemento ausente)?\n\nDEPOIS vêm os três pontos fundamentais: Sol (identidade central e missão), Lua (mundo emocional e necessidades), Ascendente (forma de se apresentar e perceber o mundo).\n\nEM SEGUIDA os planetas pessoais (Mercúrio, Vênus, Marte) revelam como a pessoa pensa, o que ama e como age. Depois os planetas sociais (Júpiter, Saturno) revelam onde há expansão e onde há trabalho.\n\nOS ASPECTOS MAIS IMPORTANTES entre planetas revelam as dinâmicas internas — conjunções (fusão de energias), oposições (tensão que pede integração), trígonos (fluxo natural), quadrados (atrito que produz força).\n\nA SÍNTESE é o momento onde o astrólogo (ou você, lendo seu próprio mapa) monta a narrativa: não é uma lista de características — é uma história sobre quem essa pessoa é, que desafios carrega, que dons tem, e em que está no momento.\n\nASTROLOGIA E LIVRE-ARBÍTRIO: a astrologia mostra tendências, não fatalidades. Dois mapas idênticos (gêmeos) produzem vidas diferentes porque as escolhas são diferentes. O mapa é o terreno — você é o jardineiro. Mesmo o terreno mais difícil, cultivado com sabedoria, pode produzir flores extraordinárias.\n\nETICA NA PRÁTICA ASTROLÓGICA: assim como no Tarô, a astrologia pede responsabilidade. Nunca assuste com aspectos difíceis. Nunca faça previsões absolutas. Sempre use a linguagem de tendência e possibilidade. E lembre: o objetivo é iluminar, não determinar.",
        "exemplo": "Um homem de 35 anos com Sol em Capricórnio (12ª Casa), Lua em Escorpião (10ª Casa), Ascendente Touro, Saturno em Escorpião (7ª Casa), e Júpiter em Áries (12ª Casa). Leitura integrada: há uma tensão fundamental entre a necessidade de ser visto e reconhecido profissionalmente (Lua em Escorpião na 10ª) e a tendência a trabalhar nos bastidores ou de forma oculta (Sol na 12ª). O Ascendente Touro apresenta ao mundo uma pessoa estável e confiável, mas por baixo há uma profundidade emocional e uma ambição que poucos percebem. Saturno na 7ª indica relacionamentos que são trabalho sério, onde as maiores lições de vida acontecem.",
        "aplicacao": "1. Leia seu mapa natal completo seguindo a sequência: impressão geral, trídade básica (Sol-Lua-Asc), planetas pessoais, aspectos principais. 2. Escreva uma síntese de um parágrafo. 3. Compare com o que você sabe sobre si mesmo.",
        "exercicio": "Escreva uma síntese de três parágrafos sobre seu próprio mapa natal: quem você é (Sun, Moon, Asc), como você age e o que busca (Mercúrio, Vênus, Marte), e qual é o seu maior desafio e maior dom (Saturno e Júpiter). Use linguagem de tendência, não de certeza.",
        "gabarito": "Uma boa síntese astrológica soa como alguém que te conhece profundamente — porque ela integra múltiplas camadas numa narrativa coerente. O objetivo nunca é encaixar a pessoa num signo, mas usar o mapa como espelho para iluminar quem ela já é."
      }
    }
  }
}

# --- 2. LÓGICA DE CONEXÃO ---
def consultar_ravengar(sistema, pergunta, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sistema}, {"role": "user", "content": pergunta}],
            model="openai/gpt-oss-120b",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na conexão mística: {str(e)}"

# --- 3. TELA DE ENTRADA ---
if 'chave_api' not in st.session_state or not st.session_state.chave_api:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🔮 Tenda do Ravengar</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#888;'>Mistérios da Mente e do Destino</p>", unsafe_allow_html=True)
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
    st.markdown("<p style='font-size:0.88em;color:#888;margin-bottom:6px;'>Clique em ▶ para tocar. Ative o loop manualmente se desejar repetir.</p>", unsafe_allow_html=True)
    SONS = {
        "🌙 Atmosfera Mística": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌊 Sons da Natureza": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🔮 Ambient Profundo": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    }
    som_escolhido = st.selectbox("Escolha o som:", list(SONS.keys()), key="select_som_ambiente", label_visibility="collapsed")
    st.audio(SONS[som_escolhido], format="audio/mp3")


# --- ABAS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "🔮 Oráculo", "👁️ Decifrador", "🔥 Teste de Intenção",
    "🧠 Quiz Psicológico", "🌀 Vidas Passadas", "🃏 Carta do Tarot",
    "⭐ Mapa Astral", "💞 Compatibilidade", "🔢 Numerologia",
    "🖤 Espelho Negro", "🌙 Ritual de Intenção", "ᚠ Oráculo das Runas",
    "🎓 Cursos Grátis"
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

# --- ABA 13: CURSOS GRÁTIS ---
with tab13:
    st.markdown("### 🎓 Cursos Grátis")
    st.markdown("*Aprofunde seu conhecimento místico com cursos completos e gratuitos.*")

    if not CURSOS:
        st.warning("Arquivo de cursos não encontrado. Certifique-se que o arquivo `cursos_ravengar.json` está na mesma pasta do app.")
    else:
        # Inicializa estado dos cursos
        if 'curso_ativo' not in st.session_state:
            st.session_state.curso_ativo = None
        if 'aula_ativa' not in st.session_state:
            st.session_state.aula_ativa = None
        if 'aulas_concluidas' not in st.session_state:
            st.session_state.aulas_concluidas = {}
        if 'quiz_ativo' not in st.session_state:
            st.session_state.quiz_ativo = False
        if 'quiz_resposta' not in st.session_state:
            st.session_state.quiz_resposta = ""
        if 'quiz_resultado' not in st.session_state:
            st.session_state.quiz_resultado = None

        # --- TELA: LISTA DE CURSOS ---
        if st.session_state.curso_ativo is None:
            cols = st.columns(3)
            for idx, (chave, curso) in enumerate(CURSOS.items()):
                col = cols[idx % 3]
                concluidas = len(st.session_state.aulas_concluidas.get(chave, []))
                total = curso['total_aulas']
                pct = int(concluidas / total * 100) if total > 0 else 0
                with col:
                    st.markdown(f"""
                    <div class='curso-card'>
                        <div style='font-size:2.2em;'>{curso['icone']}</div>
                        <div style='font-size:1.1em;font-weight:bold;margin:6px 0;'>{curso['titulo']}</div>
                        <div style='font-size:0.82em;opacity:0.8;'>{curso['descricao'][:80]}...</div>
                        <div style='margin-top:10px;font-size:0.85em;'>{total} aulas · {pct}% concluído</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if col.button(f"ENTRAR NO CURSO", key=f"entrar_{chave}"):
                        st.session_state.curso_ativo = chave
                        st.session_state.aula_ativa = None
                        st.session_state.quiz_ativo = False
                        st.session_state.quiz_resultado = None
                        st.rerun()

        # --- TELA: LISTA DE AULAS DO CURSO ---
        elif st.session_state.aula_ativa is None:
            chave = st.session_state.curso_ativo
            curso = CURSOS[chave]
            concluidas = st.session_state.aulas_concluidas.get(chave, [])

            col_v, col_b = st.columns([5, 1])
            with col_b:
                if st.button("← Voltar", key="voltar_cursos"):
                    st.session_state.curso_ativo = None
                    st.rerun()

            st.markdown(f"## {curso['icone']} {curso['titulo']}")
            st.markdown(f"*{curso['descricao']}*")

            pct = int(len(concluidas) / curso['total_aulas'] * 100)
            st.markdown(f"""
            <div class='progresso-curso'>
                📚 {len(concluidas)} de {curso['total_aulas']} aulas concluídas — {pct}% do curso
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct / 100)

            st.markdown("### 📋 Aulas do Curso")

            for num, aula in curso['aulas'].items():
                concluida = num in concluidas
                status = "✅" if concluida else "📖"
                col_a, col_b2 = st.columns([5, 1])
                with col_a:
                    st.markdown(f"**{status} Aula {num} — {aula['titulo']}**")
                with col_b2:
                    label = "Revisar" if concluida else "Estudar"
                    if st.button(label, key=f"aula_{chave}_{num}"):
                        st.session_state.aula_ativa = num
                        st.session_state.quiz_ativo = False
                        st.session_state.quiz_resposta = ""
                        st.session_state.quiz_resultado = None
                        st.rerun()

            if len(concluidas) == curso['total_aulas']:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 🏆 Você concluiu o curso!")
                if st.button("🎓 GERAR MEU CERTIFICADO DO RAVENGAR", key=f"cert_{chave}"):
                    with st.spinner("O Ravengar prepara seu pergaminho..."):
                        sistema_cert = (
                            "Você é o Ravengar, guardião dos saberes ancestrais. "
                            "Escreva um certificado de conclusão solene e envolvente, como um pergaminho místico, "
                            "em texto corrido e poético. Mencione o nome do aluno, o curso concluído, "
                            "o que esse conhecimento significa e que poderes/responsabilidades esse saber confere. "
                            "Tom grandioso, místico e honroso. Em português do Brasil."
                        )
                        cert = consultar_ravengar(
                            sistema_cert,
                            f"Aluno: {st.session_state.usuario}. Curso concluído: {curso['titulo']}.",
                            chave_api
                        )
                    st.markdown(f"<div class='ravengar-card'>🎓 <strong>CERTIFICADO DO RAVENGAR</strong><br><br>{cert}</div>", unsafe_allow_html=True)

        # --- TELA: CONTEÚDO DA AULA ---
        else:
            chave = st.session_state.curso_ativo
            num = st.session_state.aula_ativa
            curso = CURSOS[chave]
            aula = curso['aulas'][num]
            concluidas = st.session_state.aulas_concluidas.get(chave, [])

            col_v2, col_t, col_p = st.columns([1, 4, 1])
            with col_v2:
                if st.button("← Aulas", key="voltar_aulas"):
                    st.session_state.aula_ativa = None
                    st.session_state.quiz_ativo = False
                    st.session_state.quiz_resultado = None
                    st.rerun()
            with col_t:
                st.markdown(f"**{curso['icone']} {curso['titulo']}**")
            with col_p:
                nums = list(curso['aulas'].keys())
                idx_atual = nums.index(num)
                if idx_atual < len(nums) - 1:
                    if st.button("Próxima →", key="proxima_aula"):
                        st.session_state.aula_ativa = nums[idx_atual + 1]
                        st.session_state.quiz_ativo = False
                        st.session_state.quiz_resultado = None
                        st.rerun()

            st.markdown(f"## Aula {num} — {aula['titulo']}")

            # Conteúdo
            st.markdown(f"""
            <div class='aula-conteudo'>
                {aula['conteudo'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Exemplo
            st.markdown(f"""
            <div class='aula-secao'>
                <strong>🎬 Exemplo Prático</strong><br><br>
                {aula['exemplo'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Aplicação
            st.markdown(f"""
            <div class='aula-secao'>
                <strong>⚙️ Como Aplicar</strong><br><br>
                {aula['aplicacao'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Exercício
            st.markdown(f"""
            <div class='aula-secao'>
                <strong>🏋️ Exercício Prático</strong><br><br>
                {aula['exercicio'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Gabarito (oculto até clicar)
            with st.expander("✅ Ver Gabarito Comentado"):
                st.markdown(aula['gabarito'])

            st.markdown("<hr>", unsafe_allow_html=True)

            # --- QUIZ DA AULA ---
            st.markdown("### 🧠 Quiz da Aula")
            st.markdown("Responda com suas próprias palavras — a IA avalia e comenta.")

            if not st.session_state.quiz_ativo:
                if st.button("🧠 INICIAR QUIZ DESTA AULA", key=f"quiz_btn_{chave}_{num}"):
                    st.session_state.quiz_ativo = True
                    st.session_state.quiz_resultado = None
                    st.rerun()
            else:
                pergunta_quiz = (
                    f"Com base no conteúdo da aula '{aula['titulo']}' do curso '{curso['titulo']}', "
                    f"faça uma pergunta desafiadora que teste se o aluno realmente compreendeu o conteúdo — "
                    f"não uma pergunta de memorização, mas de compreensão e aplicação. "
                    f"Exiba apenas a pergunta, sem resposta."
                )
                if 'quiz_pergunta_texto' not in st.session_state or st.session_state.get('quiz_pergunta_aula') != f"{chave}_{num}":
                    with st.spinner("Preparando pergunta..."):
                        st.session_state.quiz_pergunta_texto = consultar_ravengar("Você é um professor de estudos esotéricos.", pergunta_quiz, chave_api)
                        st.session_state.quiz_pergunta_aula = f"{chave}_{num}"

                st.markdown(f"<div class='aula-secao'><strong>❓ Pergunta:</strong><br><br>{st.session_state.quiz_pergunta_texto}</div>", unsafe_allow_html=True)

                st.session_state.quiz_resposta = st.text_area("Sua resposta:", height=120, key=f"quiz_resp_{chave}_{num}", value=st.session_state.quiz_resposta)

                if st.button("📤 ENVIAR RESPOSTA", key=f"quiz_enviar_{chave}_{num}"):
                    if st.session_state.quiz_resposta.strip():
                        with st.spinner("O Ravengar avalia sua resposta..."):
                            sistema_aval = (
                                f"Você é um professor de estudos esotéricos avaliando a resposta de um aluno. "
                                f"A aula era sobre: {aula['titulo']}. O conteúdo central foi: {aula['conteudo'][:500]}. "
                                f"A pergunta foi: {st.session_state.quiz_pergunta_texto}. "
                                f"Avalie a resposta do aluno de forma construtiva e aprofundada. "
                                f"Diga o que ele acertou, o que pode aprofundar, e complete com o ponto mais importante que a resposta talvez não tenha coberto. "
                                f"Tom encorajador e didático. Em português do Brasil."
                            )
                            st.session_state.quiz_resultado = consultar_ravengar(sistema_aval, f"Resposta do aluno: {st.session_state.quiz_resposta}", chave_api)
                    else:
                        st.warning("Escreva sua resposta antes de enviar.")

                if st.session_state.quiz_resultado:
                    st.markdown(f"<div class='ravengar-card'>🎓 <strong>Avaliação do Ravengar</strong><br><br>{st.session_state.quiz_resultado}</div>", unsafe_allow_html=True)

                    if num not in concluidas:
                        if st.button("✅ MARCAR AULA COMO CONCLUÍDA", key=f"concluir_{chave}_{num}"):
                            if chave not in st.session_state.aulas_concluidas:
                                st.session_state.aulas_concluidas[chave] = []
                            if num not in st.session_state.aulas_concluidas[chave]:
                                st.session_state.aulas_concluidas[chave].append(num)
                            st.success("✅ Aula concluída! Continue para a próxima.")
                            st.session_state.quiz_ativo = False
                            st.session_state.quiz_resultado = None
                            st.rerun()
                    else:
                        st.success("✅ Esta aula já foi concluída!")

# --- RODAPÉ ---
st.markdown("""
<div class='rodape-ravengar'>
    ✦ EXPLORANDO OS MISTÉRIOS DA MENTE E DO DESTINO ✦<br>
    © 2026 TENDA DO RAVENGAR
</div>
""", unsafe_allow_html=True)
