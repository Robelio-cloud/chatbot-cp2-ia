import streamlit as st
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime

# --- Estilização Gótica e Rock'n'Roll ---
# NOTA: A injeção de CSS com unsafe_allow_html é um recurso poderoso, mas deve ser usado com cuidado.
st.markdown("""
    <style>
        /* Importa uma fonte gótica do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

        /* Fundo preto com estrelas brancas */
        .stApp {
            background-color: #000000;
            background-image:
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px),
                radial-gradient(rgba(255,255,255,.4), rgba(255,255,255,.1) 2px, transparent 30px);
            background-size: 550px 550px, 350px 350px, 250px 250px, 150px 150px;
            background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;
            color: #FFFFFF;
        }

        /* Título Principal */
        .rockstar-title {
            font-family: 'MedievalSharp', cursive;
            font-size: 4.5em;
            color: #E50000; /* Vermelho Sangue */
            font-weight: bold;
            text-align: center;
            text-shadow: 2px 2px 4px #000000;
            margin-bottom: 0.2em;
        }
        
        /* Personalizar botão primary para cor roxa escura */
        .stButton > button[kind="primary"] {
            background-color: #4B0082 !important; /* Roxo Indigo */
            border: 2px solid #E50000 !important;
            color: white !important;
            font-weight: bold;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #8B008B !important; /* Magenta Escuro */
            border-color: #FF4500 !important;
        }
        
        /* Container das respostas do chatbot */
        .chatbot-response {
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #E50000;
            margin: 10px 0;
            word-wrap: break-word;
        }
        
        /* Muda a cor dos cabeçalhos (h1, h2, h3) */
        h1, h2, h3 {
            color: #E50000 !important;
        }
        
        /* Muda a cor do texto do slider */
        .stSlider [data-baseweb="slider"] {
             color: #FFFFFF !important;
        }

    </style>
    <div class="rockstar-title">RockStar Burger</div>
""", unsafe_allow_html=True)
# --- Fim do bloco visual ---

# Dataset temático de intents para RockStar Burger
intents = {
    "greeting": {
        "examples": [
            "e aí", "fala", "hey", "hello", "oi", "olá", "bom dia", "boa tarde", "boa noite",
            "salve", "eae", "oi boa tarde", "ola", "cumprimentando vocês", "oii", "oie",
            "fla", "flw", "eai", "oi pessoal", "oiii", "opa", "opaaa", "salveee",
            "heey", "helo", "hellooo", "bom diaa", "boaa tarde", "boaaa noite"
        ],
        "responses": [
            "E aí, rockstar! 🤘 Bem-vindo ao RockStar Burger! Pronto pra detonar na fome?",
            "Fala, lenda! 💀 Chega mais, a casa do rock tá aberta. O que você manda hoje?",
            "Salve! Bem-vindo ao nosso palco. Qual o seu pedido pra começar o show?",
            "Hey! Que a força do metal esteja com você! Como posso te ajudar?"
        ]
    },
    
    "goodbye": {
        "examples": [
            "falou", "adeus", "bye", "flw", "tchau", "até mais", "até logo",
            "valeu tchau", "xau", "obrigado tchau", "nos vemos", "falow", "adeos",
            "bai", "baye", "tiau", "tchauu", "até maiss", "ate mais", "xauu",
            "obrigado tchao", "nos vemoss", "fui", "fuii", "to indo", "vou indo"
        ],
        "responses": [
            "Falou! Keep on rockin' e volte sempre! 🤘",
            "Até a próxima! Obrigado por escolher o RockStar Burger!",
            "Valeu, rockstar! A gente se vê no próximo show!",
            "Tchau! Foi um prazer atender uma lenda como você!"
        ]
    },
    
    "thanks": {
        "examples": [
            "valeu", "brigado", "mt obrigado", "obrigada", "muito grato", "grato", "agradeco",
            "obrigado", "muito obrigado", "vlw", "agradecido", "thanks", "valeuu", "brigadu",
            "mt obrigadu", "obrigadaa", "muito gratu", "gratu", "agradeso", "obrigadu",
            "mto obrigado", "valw", "agradecidu", "tankss", "thank you", "grato demais"
        ],
        "responses": [
            "É nóis! 🤘 Tamo junto sempre que precisar.",
            "De nada! O rock agradece a sua presença!",
            "Disponha! É pra isso que estamos aqui!",
            "Tranquilo! Precisando, é só chamar no palco!"
        ]
    },
    
    "purchase": {
        "examples": [
            "quero pedir", "posso fazer um pedido?", "quero um burger", "me vê um hambúrguer",
            "quero comprar um hambúrguer", "gostaria de fazer um pedido", "quero comprar",
            "tô com fome", "to com fome", "pedir comida", "kero pedir", "posso faser um pedido?",
            "kero um burger", "me ve um hamburger", "quero compra um hamburger", "gostaria de faser um pedido",
            "kero comprar", "to com fomi", "tou com fome", "pedi comida", "fazer pedido", "vou pedir"
        ],
        "responses": [
            "Show! Nossos hits são de peso! Se liga no setlist:\n• **Master of Burgers (Metallica)** - R$ 35\n• **Appetite for Destruction (Guns N' Roses)** - R$ 38\n• **Highway to Hell (AC/DC)** - R$ 33\n• **Ace of Spades (Motörhead)** - Vegano - R$ 32\n\nQual vai ser a pedida?",
            "Volume no máximo! 🎸 Nossos clássicos incluem:\n• **The Trooper (Iron Maiden)** - R$ 36\n• **Paranoid (Black Sabbath)** - R$ 34\n• **Stairway to Heaven (Led Zeppelin)** - R$ 40\n\nQual desses hinos vai matar sua fome?",
            "Bora pro rock! 🤘 Temos essas opções devastadoras:\n• **Master of Burgers** - O clássico do Metallica - R$ 35\n• **Highway to Hell** - Levemente apimentado - R$ 33\n• **Stairway to Heaven** - Nosso burger lendário - R$ 40\n\nO que você escolhe?",
            "Prepara o palco! 🎸 Nossos sucessos incluem:\n• **Appetite for Destruction** - Explosivo como o Guns - R$ 38\n• **The Trooper** - Batalha épica do Iron Maiden - R$ 36\n• **Ace of Spades** - Opção vegana do Motörhead - R$ 32\n\nQual vai ser?"
        ]
    },
    
    "menu": {
        "examples": [
            "que hambúrgueres vocês têm", "quais os lanches disponíveis", "mostrem o menu",
            "qual o cardápio", "o que vocês vendem", "cardapio completo",
            "lista de hamburguer", "ver menu", "que lanches tem", "ke hamburgueres voces tem",
            "kais os lanches disponiveis", "mostrem o meno", "kual o cardapio", "o ke voces vendem",
            "cardapiu completo", "lista de hamburger", "ve menu", "ke lanches tem", "opcoes de lanche",
            "menu completo", "cardápio de hoje", "o que tem no cardápio", "ver opções"
        ],
        "responses": [
            "Aqui está o nosso setlist completo! 🤘\n\n**HITS DO METAL:**\n• **Master of Burgers (Metallica)** - R$ 35\n• **Appetite for Destruction (Guns N' Roses)** - R$ 38\n• **The Trooper (Iron Maiden)** - R$ 36\n\n**CLÁSSICOS DO ROCK:**\n• **Highway to Hell (AC/DC)** - R$ 33 (levemente apimentado! 🔥)\n• **Paranoid (Black Sabbath)** - R$ 34\n• **Stairway to Heaven (Led Zeppelin)** - R$ 40\n\n**OPÇÃO VEGANA:**\n• **Ace of Spades (Motörhead)** - R$ 32\n\nTemos também acompanhamentos e bebidas pra completar o show!",
            "Bora conhecer nosso arsenal! 🎸\n\n**OS PESADOS:**\n• Master of Burgers - O poder do Metallica - R$ 35\n• Appetite for Destruction - Explosão Guns N' Roses - R$ 38\n• The Trooper - Batalha Iron Maiden - R$ 36\n\n**OS CLÁSSICOS:**\n• Highway to Hell - Com fogo AC/DC - R$ 33\n• Paranoid - Loucura Black Sabbath - R$ 34\n• Stairway to Heaven - Lenda Led Zeppelin - R$ 40\n\n**VEGANO ROCK:**\n• Ace of Spades - Motörhead verde - R$ 32",
            "Nosso cardápio é puro rock! 🤘\n\n• **Master of Burgers** (Metallica) - R$ 35\n• **Appetite for Destruction** (Guns N' Roses) - R$ 38\n• **The Trooper** (Iron Maiden) - R$ 36\n• **Highway to Hell** (AC/DC) - R$ 33\n• **Paranoid** (Black Sabbath) - R$ 34\n• **Stairway to Heaven** (Led Zeppelin) - R$ 40\n• **Ace of Spades** (Motörhead - Vegano) - R$ 32\n\nTodos feitos com ingredientes de primeira!",
            "Se liga na nossa discografia gastronômica! 🎵\n\n**METAL SUPREMO:** Master of Burgers (R$ 35), Appetite for Destruction (R$ 38), The Trooper (R$ 36)\n\n**ROCK CLÁSSICO:** Highway to Hell (R$ 33), Paranoid (R$ 34), Stairway to Heaven (R$ 40)\n\n**ALTERNATIVO:** Ace of Spades Vegano (R$ 32)\n\nQual vai ser sua escolha?"
        ]
    },
    
    "prices": {
        "examples": [
            "valores dos hambúrgueres", "preço do burger", "quanto é o hambúrguer", "valor do lanche",
            "quanto custa", "qual o preço", "precos", "custa quanto", "valor do Master of Burgers",
            "valores dos hamburgueres", "preco do burger", "kuanto e o hamburguer", "valor do lanchi",
            "kuanto kusta", "kual o preco", "prekos", "kusta kuanto", "valor do Master of Burgers",
            "preço dos lanches", "quanto custa cada um", "tabela de preços", "valores", "preços dos burgers",
            "quanto sai", "valor de cada", "preço individual"
        ],
        "responses": [
            "Se liga na tabela de preços dos nossos hits:\n• **Master of Burgers**: R$ 35\n• **Appetite for Destruction**: R$ 38\n• **The Trooper**: R$ 36\n• **Highway to Hell**: R$ 33\n• **Paranoid**: R$ 34\n• **Stairway to Heaven**: R$ 40\n• **Ace of Spades (Vegano)**: R$ 32",
            "Valores pra detonar na fome:\n• **Clássicos (R$ 32-34)**: Ace of Spades, Highway to Hell, Paranoid.\n• **Hinos do Metal (R$ 35-38)**: Master of Burgers, The Trooper, Appetite for Destruction.\n• **Lendário (R$ 40)**: Stairway to Heaven, nosso burger mais épico!",
            "Nossos preços são justos como um bom riff! 🎸\n\nDo mais em conta ao premium:\nR$ 32 - Ace of Spades (Vegano)\nR$ 33 - Highway to Hell\nR$ 34 - Paranoid\nR$ 35 - Master of Burgers\nR$ 36 - The Trooper\nR$ 38 - Appetite for Destruction\nR$ 40 - Stairway to Heaven",
            "Aqui está a nossa tabela rock! 🤘\n\n💰 **ENTRADA VIP (R$ 32-34):** Ace of Spades, Highway to Hell, Paranoid\n💰 **PISTA (R$ 35-36):** Master of Burgers, The Trooper\n💰 **CAMAROTE (R$ 38-40):** Appetite for Destruction, Stairway to Heaven"
        ]
    },
    
    "delivery_time": {
        "examples": [
            "tempo de entrega", "demora quanto", "quando fica pronto", "quanto tempo para entregar",
            "demora pra chegar", "quanto tempo demora", "prazo de entrega", "quando vai chegar",
            "tempo de intrega", "dimora quanto", "kuando fica pronto", "kuanto tempo para entregar",
            "dimora pra chegar", "kuanto tempo dimora", "praso de entrega", "kuando vai chegar",
            "demora muito", "leva quanto tempo", "em quanto tempo fica pronto", "prazo",
            "tempo pra ficar pronto", "delivery demora", "entrega rápida", "quanto tempo leva"
        ],
        "responses": [
            "Nossa cozinha é rápida como um solo de guitarra! 🎸 O preparo leva de 15-20 minutos. Para delivery, some mais uns 20-30 minutos, dependendo de onde for o seu show.",
            "Sem demora! Seu lanche fica pronto em uns 20 minutos aqui na casa. Se for pra levar, o tempo total é de uns 40-50 minutos pra chegar voando até você.",
            "Velocidade do rock! 🤘 Preparo: 15-20 min. Delivery: + 20-30 min (varia pela distância). Total máximo: uns 50 minutos para o show chegar na sua casa!",
            "Rápido como uma batida dupla! 🥁 15-20 min na cozinha + 20-30 min de entrega. Você vai estar saboreando nosso rock em menos de 1 hora!"
        ]
    },
    
    "complaint": {
        "examples": [
            "hambúrguer veio frio", "pedido errado", "demora muito", "atendimento ruim",
            "quero reclamar", "não gostei", "reclamacao", "problema com pedido", "insatisfeito",
            "hamburguer veio friu", "pedidu errado", "dimora muito", "atendimento ruim",
            "kero reclamar", "nao gostei", "reclamacau", "problema com pedidu", "insatisfeitu",
            "comida fria", "pedido atrasado", "erro no pedido", "ruim", "horrivel",
            "demorou demais", "qualidade ruim", "não recomendo", "decepção"
        ],
        "responses": [
            "Opa, falha nossa! 😟 Isso não é nada rock'n'roll. Me conta o que rolou pra gente consertar essa distorção agora mesmo.",
            "Putz! Pedimos desculpas. Nossa missão é fazer um show perfeito. Por favor, diga qual foi o problema e vamos resolver na hora.",
            "Que mancada! 😈 Sentimos muito por isso. Sua satisfação é o nosso maior hit. Vamos corrigir isso. O que aconteceu?",
            "Desafinação total! 🎸 Isso não condiz com o nosso padrão rock. Conta pra gente o que houve que a gente resolve esse problema na velocidade da luz!"
        ]
    },
    
    "hours": {
        "examples": [
            "horário de funcionamento", "vocês abrem hoje", "até que horas funciona", "quando fecha",
            "que horas abrem", "aberto agora", "funcionamento", "horarios", "aberto domingo",
            "horario de funcinamento", "voces abrem oje", "ate ke horas funciona", "kuando fecha",
            "ke horas abrem", "abertu agora", "funcionamentu", "horarios", "abertu domingo",
            "que horas abre", "horário hoje", "funciona que horas", "fecha que horas",
            "aberto segunda", "horário de hoje", "que dias abrem", "segunda abre"
        ],
        "responses": [
            "O show nunca para! 🤘 Funcionamos de Terça a Domingo, das 18h até a meia-noite (00h). Na Segunda, a gente descansa pra afinar os instrumentos.",
            "Nosso palco abre de Terça a Domingo! O som começa às 18h e só para à meia-noite. Delivery vai até 23h30.",
            "Horários do rock: 🎸\n• Terça a Domingo: 18h00 - 00h00\n• Delivery até: 23h30\n• Segunda: Fechado (dia de descanso da banda)",
            "Palco aberto! 🎵\nTerça-feira a Domingo das 18h às 00h. Delivery rola até 23h30. Segunda é nosso dia off pra manução dos equipamentos!"
        ]
    },
    
    "fallback": {
        "examples": [
            "não entendi", "o que", "como assim", "???", "hein", "nao entendi", "o ke",
            "como asim", "???", "ein", "que", "oi?", "como", "não sei", "perdao",
            "repete", "não compreendi", "explica", "?", "nao sei", "repeti",
            "nao compreendi", "esplica", "fala dnv", "nao captei"
        ],
        "responses": [
            "Desculpe, essa parte do som ficou meio distorcida. 😵‍💫 Posso te ajudar com o cardápio, pedidos, preços, horários ou reclamações.",
            "Não captei essa mensagem, rockstar. Tente de novo. Quer saber sobre nossos lanches, fazer um pedido ou ver os horários?",
            "Hmm, acho que perdi essa parte do riff. Pode reformular sua pergunta? Estou aqui pra falar dos nossos burgers lendários!",
            "Som meio embolado aí! 🎸 Vamos tentar de novo? Posso te ajudar com menu, pedidos, preços, delivery, horários ou resolver algum problema."
        ]
    }
}

# Transformar em dataframe (utterance, intent)
rows = []
for intent, v in intents.items():
    for ex in v["examples"]:
        rows.append({"text": ex, "intent": intent})

df = pd.DataFrame(rows)

# Downloads (apenas na primeira execução) com verificações e fallbacks.
# Tentamos baixar os recursos necessários; se falhar (por exemplo, sem internet),
# o app usa alternativas robustas para não travar em produção.
resource_checks = [
    ('punkt', 'tokenizers/punkt'),
    ('stopwords', 'corpora/stopwords'),
    ('wordnet', 'corpora/wordnet'),
    ('omw-1.4', 'corpora/omw-1.4')
]

have_punkt = False
have_stopwords = False
have_wordnet = False

for name, path in resource_checks:
    try:
        nltk.data.find(path)
        if name == 'punkt':
            have_punkt = True
        if name == 'stopwords':
            have_stopwords = True
        if name in ('wordnet', 'omw-1.4'):
            have_wordnet = True
    except LookupError:
        try:
            # quiet=True evita muita saída no deploy
            nltk.download(name, quiet=True)
            # Re-check
            nltk.data.find(path)
            if name == 'punkt':
                have_punkt = True
            if name == 'stopwords':
                have_stopwords = True
            if name in ('wordnet', 'omw-1.4'):
                have_wordnet = True
        except Exception:
            # Se não for possível baixar, seguimos com fallback
            pass

# Stopwords (fallback vazio / pequeno conjunto se não houver recursos)
if have_stopwords:
    try:
        stop_words = set(stopwords.words('portuguese'))
    except Exception:
        stop_words = set()
else:
    # Um pequeno conjunto de stopwords em português como fallback
    stop_words = set([
        'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma',
        'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele'
    ])

# Lemmatizer (só será usado se wordnet estiver disponível)
lemmatizer = None
if have_wordnet:
    try:
        lemmatizer = WordNetLemmatizer()
    except Exception:
        lemmatizer = None


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    # Tenta usar o tokenizador do NLTK (punkt). Se não estiver disponível,
    # faz um tokenizador simples baseado em regex para evitar crash no deploy.
    try:
        # se punkt não foi encontrado, nltk.word_tokenize lançará LookupError
        tokens = nltk.word_tokenize(text)
    except LookupError:
        tokens = re.findall(r"\b[\w']+\b", text, flags=re.UNICODE)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stop_words]
    # Aplica lematização apenas se o lemmatizer estiver disponível
    if lemmatizer is not None:
        try:
            tokens = [lemmatizer.lemmatize(t) for t in tokens]
        except Exception:
            # Se algo der errado na lematização, mantemos os tokens originais
            pass
    return ' '.join(tokens)

df['text_norm'] = df['text'].apply(normalize_text)

# Criar vetorizadores
tfidf_vect = TfidfVectorizer()
X_tfidf = tfidf_vect.fit_transform(df['text_norm'])

# Treinar classificador
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_tfidf, df['intent'])


def retrieve_response(query, vect=tfidf_vect, utter_vecs=X_tfidf, df=df, threshold=0.6):
    q = normalize_text(query)
    qv = vect.transform([q])
    sims = cosine_similarity(qv, utter_vecs).flatten()
    idx_sorted = np.argsort(-sims)
    if sims[idx_sorted[0]] >= threshold:
        chosen_idx = idx_sorted[0]
        intent = df.iloc[chosen_idx]['intent']
        resp = np.random.choice(intents[intent]['responses'])
        return resp, intent, sims[idx_sorted[0]]
    else:
        return np.random.choice(intents['fallback']['responses']), 'fallback', sims[idx_sorted[0]]

def detect_multiple_intents(query, threshold_clf=0.3, threshold_retrieve=0.3):
    """Detecta múltiplas intenções em uma única frase"""
    import re
    
    # Primeiro, tenta detectar intenções na frase completa
    detected_intents = []
    
    # Verifica greeting no início da frase
    greeting_words = ['oi', 'olá', 'hello', 'hey', 'e aí', 'fala', 'salve', 'bom dia', 'boa tarde', 'boa noite']
    query_lower = query.lower()
    for greeting in greeting_words:
        if query_lower.startswith(greeting) or f' {greeting} ' in query_lower:
            detected_intents.append({
                'intent': 'greeting',
                'confidence': 0.95,
                'method': 'keyword_detection',
                'segment': greeting
            })
            break
    
    # Verifica goodbye no final da frase
    goodbye_words = ['tchau', 'falou', 'bye', 'adeus', 'até mais', 'até logo', 'valeu tchau', 'xau']
    for goodbye in goodbye_words:
        if query_lower.endswith(goodbye) or f' {goodbye}' in query_lower:
            if not any(d['intent'] == 'goodbye' for d in detected_intents):
                detected_intents.append({
                    'intent': 'goodbye',
                    'confidence': 0.95,
                    'method': 'keyword_detection',
                    'segment': goodbye
                })
            break
    
    # Verifica thanks em qualquer lugar
    thanks_words = ['obrigado', 'obrigada', 'valeu', 'brigado', 'grato', 'agradeco', 'thanks']
    for thanks in thanks_words:
        if thanks in query_lower:
            if not any(d['intent'] == 'thanks' for d in detected_intents):
                detected_intents.append({
                    'intent': 'thanks',
                    'confidence': 0.90,
                    'method': 'keyword_detection',
                    'segment': thanks
                })
            break
    
    # Divide a frase em segmentos para detectar outras intenções
    segments = re.split(r'[,.;!?]|\be\b|\stambém\b|\sainda\b|\se\b|\squero\b|\sgostaria\b', query.lower())
    segments = [seg.strip() for seg in segments if seg.strip()]
    
    # Se não há segmentos múltiplos, usa a frase completa
    if len(segments) <= 1:
        segments = [query]
    
    for segment in segments:
        if len(segment.split()) < 2:  # Ignora segmentos muito pequenos
            continue
            
        # Testa classificador
        q_norm = normalize_text(segment)
        if not q_norm:  # Se não há texto normalizado, pula
            continue
            
        qv = tfidf_vect.transform([q_norm])
        probs = clf.predict_proba(qv)[0]
        
        # Pega as top 3 intenções mais prováveis
        top_indices = np.argsort(-probs)[:3]
        
        for idx in top_indices:
            intent = clf.classes_[idx]
            prob = probs[idx]
            
            # Verifica se já foi detectada por keyword
            already_detected = any(d['intent'] == intent for d in detected_intents)
            
            if prob >= threshold_clf and not already_detected:
                detected_intents.append({
                    'intent': intent,
                    'confidence': prob,
                    'method': 'classifier',
                    'segment': segment
                })
                break
        
        # Se não encontrou pelo classificador, tenta retrieval
        if not any(d['segment'] == segment for d in detected_intents if d['method'] in ['classifier', 'retrieval']):
            _, intent_ret, sim = retrieve_response(segment, threshold=threshold_retrieve)
            if intent_ret != 'fallback':
                already_detected = any(d['intent'] == intent_ret for d in detected_intents)
                if not already_detected:
                    detected_intents.append({
                        'intent': intent_ret,
                        'confidence': sim,
                        'method': 'retrieval',
                        'segment': segment
                    })
    
    # Se não detectou nada, usa fallback
    if not detected_intents:
        detected_intents.append({
            'intent': 'fallback',
            'confidence': 0.0,
            'method': 'fallback',
            'segment': query
        })
    
    # Ordena por confiança (maior primeiro)
    detected_intents.sort(key=lambda x: x['confidence'], reverse=True)
    
    return detected_intents

def generate_multi_intent_response(detected_intents):
    """Gera resposta baseada em múltiplas intenções detectadas"""
    if len(detected_intents) == 1:
        intent_data = detected_intents[0]
        resp = np.random.choice(intents[intent_data['intent']]['responses'])
        return resp, intent_data
    
    # Para múltiplas intenções, cria uma resposta combinada
    response_parts = []
    primary_intent = detected_intents[0]  # A primeira será considerada principal
    
    for intent_data in detected_intents:
        intent = intent_data['intent']
        if intent == 'greeting':
            response_parts.append("Salve, rockstar! 🤘")
        elif intent == 'menu':
            response_parts.append("Aqui está nosso setlist:\n• Master of Burgers (R$ 35)\n• Appetite for Destruction (R$ 38)\n• Highway to Hell (R$ 33)\n• The Trooper (R$ 36)\n• Paranoid (R$ 34)\n• Stairway to Heaven (R$ 40)\n• Ace of Spades Vegano (R$ 32)")
        elif intent == 'prices':
            response_parts.append("Nossos preços vão de R$ 32 (Ace of Spades) até R$ 40 (Stairway to Heaven).")
        elif intent == 'purchase':
            response_parts.append("Qual burger vai ser? Todos são hits garantidos!")
        elif intent == 'delivery_time':
            response_parts.append("Preparo: 15-20 min + Delivery: 20-30 min.")
        elif intent == 'hours':
            response_parts.append("Funcionamos Terça a Domingo, 18h às 00h.")
        elif intent == 'thanks':
            response_parts.append("Valeu! 🤘")
        elif intent == 'goodbye':
            response_parts.append("Até a próxima! Keep rockin'!")
    
    combined_response = "\n\n".join(response_parts)
    
    if not combined_response:
        combined_response = np.random.choice(intents['fallback']['responses'])
    
    return combined_response, primary_intent

def combined_respond(query, threshold_clf=0.6, threshold_retrieve=0.4):
    # Detecta múltiplas intenções
    detected_intents = detect_multiple_intents(query, threshold_clf * 0.5, threshold_retrieve)
    
    # Gera resposta baseada nas intenções detectadas
    response, primary_intent = generate_multi_intent_response(detected_intents)
    
    return response, detected_intents, primary_intent

# Interface do Streamlit
st.title('💀 Chatbot RockStar Burger 🤘')

# Sidebar com informações
# NOTA: A API do Streamlit posiciona a sidebar sempre à esquerda.
st.sidebar.markdown("""
### ✝️ Funcionalidades do Palco ✝️
- **Intenções suportadas:**
  - 😇 Cumprimentos e Despedidas
  - 🛒 Pedidos de Burgers
  - 🐍 Cardápio e Preços
  - 🐺 Horários de Funcionamento
  - 🦇 Tempo de Entrega
  - ☮️ Agradecimentos
  - 😈 Reclamações
  
- **Tecnologias:**
  - TF-IDF Vectorization
  - Logistic Regression Classifier
  - Cosine Similarity Retrieval
""")

# Configurações avançadas
st.sidebar.markdown("### ⚙️ Ajuste o Som")
mode = st.sidebar.selectbox(
    'Modo de Operação:',  
    ['🔄 Híbrido (Recomendado)', '🎯 Apenas Classificador', '🔍 Apenas Retrieval'],
    help="Escolha como o chatbot deve processar as mensagens"
)

# Sliders de confiança na vertical
st.sidebar.markdown("### 🎚️ Níveis de Confiança")
if mode == '🔄 Híbrido (Recomendado)':
    threshold_clf = st.sidebar.slider('Confiança Classificador 🧠', 0.0, 1.0, 0.6, 0.05)
    threshold_ret = st.sidebar.slider('Confiança Similaridade 🔍', 0.0, 1.0, 0.4, 0.05)
elif mode == '🎯 Apenas Classificador':
    threshold_clf = st.sidebar.slider('Confiança Classificador 🧠', 0.0, 1.0, 0.5, 0.05)
    threshold_ret = 0.0
else:  # Retrieval only
    threshold_clf = 1.0
    threshold_ret = st.sidebar.slider('Confiança Similaridade 🔍', 0.0, 1.0, 0.6, 0.05)

# Input do usuário
st.markdown("### 💬 Mande seu recado para a banda")

user_input = st.text_area(
    "Digite sua mensagem:",  
    height=100,
    placeholder="Ex: E aí! Quero um Master of Burgers. Quanto tempo demora?"
)

# Botão de envio
if st.button("🎸 Enviar Mensagem", type="primary"):
    if user_input:
        with st.spinner('Afinando os instrumentos... 🎸'):
            if mode == '🔄 Híbrido (Recomendado)':
                response, detected_intents, primary_intent = combined_respond(user_input, threshold_clf, threshold_ret)
            elif mode == '🎯 Apenas Classificador':
                response, detected_intents, primary_intent = combined_respond(user_input, threshold_clf, 0.0)
            else:  # Retrieval only
                resp, intent, confidence = retrieve_response(user_input, threshold=threshold_ret)
                source = 'retrieval' if intent != 'fallback' else 'fallback'
                # Converte para o novo formato
                detected_intents = [{
                    'intent': intent,
                    'confidence': confidence,
                    'method': source,
                    'segment': user_input
                }]
                primary_intent = detected_intents[0]
                response = resp
        
        # Exibição dos resultados
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**👤 Você disse:**")
        with col2:
            st.info(user_input)
            
        st.markdown("**🤖 RockStar Burger responde:**")
        st.markdown(f'<div class="chatbot-response">{response}</div>', unsafe_allow_html=True)
        
        # Análise técnica
        st.markdown("### 📊 Backstage (Análise Técnica)")
        
        # Mostra todas as intenções detectadas
        st.markdown("**🎯 Intenções Detectadas:**")
        
        if len(detected_intents) == 1:
            # Uma única intenção
            intent_data = detected_intents[0]
            intent_display = intent_data['intent'].replace('_', ' ').title()
            confidence_pct = intent_data['confidence'] * 100
            confidence_color = "🟢" if confidence_pct >= 70 else "🟡" if confidence_pct >= 50 else "🔴"
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**{intent_display}**")
                st.info(f"**{confidence_color} {confidence_pct:.1f}%**")
            
            with col2:
                source_emoji = {
                    'classifier': '🧠 Classificador ML',
                    'retrieval': '🔍 Busca por Similaridade',
                    'fallback': '❓ Resposta Padrão'
                }
                method_name = source_emoji.get(intent_data['method'], intent_data['method'])
                st.warning(f"**{method_name}**")
        else:
            # Múltiplas intenções
            st.info(f"**🔍 {len(detected_intents)} intenções detectadas na sua mensagem:**")
            
            for i, intent_data in enumerate(detected_intents, 1):
                intent_display = intent_data['intent'].replace('_', ' ').title()
                confidence_pct = intent_data['confidence'] * 100
                confidence_color = "🟢" if confidence_pct >= 70 else "🟡" if confidence_pct >= 50 else "🔴"
                
                method_emoji = {
                    'classifier': '🧠',
                    'retrieval': '🔍',
                    'fallback': '❓'
                }
                
                with st.expander(f"{i}. {intent_display} {confidence_color} {confidence_pct:.1f}%"):
                    st.write(f"**Segmento analisado:** '{intent_data['segment']}'")
                    st.write(f"**Método:** {method_emoji.get(intent_data['method'], '')} {intent_data['method'].title()}")
                    st.write(f"**Confiança:** {confidence_pct:.1f}%")
        
        # Texto normalizado
        st.markdown("### 🔤 Processamento de Texto")
        normalized = normalize_text(user_input)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📝 Texto Original:**")
            st.code(user_input, language="text")
        with col2:
            st.markdown("**🔤 Texto Normalizado:**")
            st.code(normalized, language="text")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-family: "Courier New", monospace; color: #CCCCCC;'>
    <small>
    🤘 <strong>RockStar Burger</strong> - O sabor do rock na sua fome 🤘<br>
    Chatbot desenvolvido com Python, Streamlit & N.L.P.
    </small>
</div>
""", unsafe_allow_html=True)