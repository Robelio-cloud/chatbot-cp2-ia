# 🤘 RockStar Burger - Chatbot Inteligente

![image](/images/chatbot-02.png)

## 🎸 Sobre o Projeto

**RockStar Burger** é um chatbot inteligente para uma **lanchonete temática de Rock e Metal** que utiliza técnicas avançadas de Processamento de Linguagem Natural (NLP) para atender clientes de forma interativa e divertida.

### 🎯 Tipo de Estabelecimento
**Lanchonete Temática Rock/Metal** - Um ambiente que combina a paixão pelo rock com hambúrgueres gourmet, onde cada produto tem nome de música clássica do rock/metal.

## 🚀 Funcionalidades

- ✅ **Detecção de Múltiplas Intenções** em uma única frase
- ✅ **10 Categorias de Intenções** (cumprimentos, cardápio, preços, pedidos, etc.)
- ✅ **220+ Exemplos de Frases** incluindo erros de digitação
- ✅ **40 Respostas Temáticas** no estilo rock/metal
- ✅ **Interface Web Interativa** com Streamlit
- ✅ **Análise Técnica Detalhada** dos resultados
- ✅ **Sistema Híbrido** (Classificador ML + Busca por Similaridade)

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Interface web
- **NLTK** - Processamento de linguagem natural
- **Scikit-learn** - Machine Learning
- **Pandas/NumPy** - Manipulação de dados
- **TF-IDF** - Vetorização de texto
- **Logistic Regression** - Classificação
- **Cosine Similarity** - Busca por similaridade

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd chatbot-cp2-ia
```

### 2. Instale as Dependências
```bash
pip install streamlit nltk scikit-learn pandas numpy
```

### 3. Downloads do NLTK (Automático)
O sistema baixa automaticamente os recursos necessários do NLTK:
- `punkt` - Tokenização
- `stopwords` - Palavras irrelevantes (português)
- `wordnet` - Lematização

## 🏃‍♂️ Como Executar

### Método 1: Comando Direto
```bash
streamlit run app.py
```

### Método 2: Via Módulo Python
```bash
python -m streamlit run app.py
```

### 3. Acesse no Navegador
Após executar, abra seu navegador em:
- **Local**: http://localhost:8501
- **Rede**: http://[seu-ip]:8501

## 📁 Estrutura dos Arquivos

```
chatbot-cp2-ia/
├── app.py                    # Aplicação principal Streamlit
├── intents_database.json     # Base de dados das intenções
├── README.md                 # Este arquivo
└── requirements.txt          # Dependências (opcional)
```

## 🎯 Cardápio RockStar Burger

### 🔥 HITS DO METAL
- **Master of Burgers** (Metallica) - R$ 35
- **Appetite for Destruction** (Guns N' Roses) - R$ 38
- **The Trooper** (Iron Maiden) - R$ 36

### 🎸 CLÁSSICOS DO ROCK
- **Highway to Hell** (AC/DC) - R$ 33 🌶️
- **Paranoid** (Black Sabbath) - R$ 34
- **Stairway to Heaven** (Led Zeppelin) - R$ 40

### 🌱 OPÇÃO VEGANA
- **Ace of Spades** (Motörhead) - R$ 32

## 🤖 Como Usar o Chatbot

### Exemplos de Interação:

**Simples:**
- "Oi, quero ver o cardápio"
- "Quanto custa o Master of Burgers?"
- "Vocês entregam?"

**Múltiplas Intenções:**
- "Oi, quero ver o cardápio e saber os preços" *(detecta 3 intenções)*
- "Valeu pelo atendimento, tchau!" *(detecta 2 intenções)*

### Configurações Avançadas:
- **Modo Híbrido**: Usa classificador + busca por similaridade
- **Apenas Classificador**: Usa apenas machine learning
- **Apenas Retrieval**: Usa apenas busca por similaridade
- **Ajuste de Confiança**: Sliders para fine-tuning

## 📊 Análise Técnica

O sistema fornece análise detalhada:
- **Intenções Detectadas** com percentual de confiança
- **Método Utilizado** (Classificador/Retrieval/Keyword)
- **Segmento Analisado** da frase
- **Texto Normalizado** vs Original

## 🏢 Horários de Funcionamento
- **Terça a Domingo**: 18h00 - 00h00
- **Delivery**: Até 23h30
- **Segunda-feira**: Fechado (manutenção)

## 🎨 Visual Theme

Interface com tema **gótico/rock**:
- Fundo preto estrelado
- Fonte medieval (MedievalSharp)
- Cores: vermelho sangue, roxo, branco
- Emojis temáticos (🤘, 🎸, 💀, 🔥)

## 🔧 Troubleshooting

### Erro: "streamlit não reconhecido"
**Solução**: Use `python -m streamlit run app.py`

### Erro: NLTK Download
**Solução**: Execute manualmente:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Erro: Dependências
**Solução**: Reinstale:
```bash
pip install --upgrade streamlit nltk scikit-learn pandas numpy
```

## 📈 Estatísticas da Base de Dados

- **10 Intenções** diferentes
- **220+ Exemplos** de frases
- **40 Respostas** temáticas
- **Suporte a erros** de digitação
- **Múltiplas variações** linguísticas

## 🌐 Deploy em URL Pública

### 🎯 Opção 1: Streamlit Community Cloud (RECOMENDADO - GRATUITO)

1. **Suba para o GitHub:**
```bash
git init
git add .
git commit -m "Initial commit - RockStar Burger Chatbot"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/chatbot-cp2-ia.git
git push -u origin main
```

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**
3. **Conecte com GitHub** e selecione:
   - Repository: `chatbot-cp2-ia`
   - Branch: `main`
   - Main file path: `app.py`
4. **Deploy automático!** 🎉

**URL resultante:** `https://SEU_USUARIO-chatbot-cp2-ia-app-HASH.streamlit.app`

## 🔗 Aplicação publicada na Web.

A aplicação já está publicada no Streamlit Community Cloud e pode ser acessada publicamente neste link:

- https://chatbot-cp2-ia-j3ulgljqfw7mwln9pafpuj.streamlit.app/

![image](/images/chatbot-01.png)

### 🚂 Opção 2: Railway (FÁCIL - GRATUITO)

1. Acesse [railway.app](https://railway.app)
2. Conecte com GitHub
3. Selecione seu repositório
4. Deploy automático!

### ☁️ Opção 3: Google Cloud Run / Heroku

Consulte documentação específica para essas plataformas.

## 🤝 Contribuição

Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Adicione novos exemplos em `intents_database.json`
4. Teste no chatbot
5. Envie um pull request

## 📜 Licença

Este projeto é educacional e foi desenvolvido como parte do curso de Inteligência Artificial da FIAP.

---

**🤘 Keep on rockin' and enjoy your burger! 🍔**