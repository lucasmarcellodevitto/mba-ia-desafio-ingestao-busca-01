# Desafio MBA Engenharia de Software com IA — Full Cycle

## Objetivo

Ingestão: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector.
Busca: Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

---

## Tecnologias Usadas

- **Python 3.+**
- **LangChain**
- **PostgreSQL + pgVector**
- **Google Gemini** — embeddings (`gemini-embedding-001`) e respostas (`gemini-2.5-flash-lite`)
- **Docker & Docker Compose**

---

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Chave de API do Google AI Studio: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## Criando uma API Key no Google Gemini

Acesse o Google AI Studio:

https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR

1 - Faça login com sua conta Google.

2 - Utilize sua conta Google para acessar o AI Studio.

3 - Navegue até a seção de chaves de API.

4 - No painel de controle, clique em "API Keys" ou "Chaves de API".

5 - Crie uma nova API Key:
5.1 - Clique em "Create API Key" ou "Criar chave de API".
5.2 - Dê um nome para a chave que a identifique facilmente.
5.3 - A chave será gerada e exibida na tela.
5.4 - Copie e armazene sua API Key:

Copie a chave gerada e cole no arquivo .env na variável GOOGLE_API_KEY.

Atenção: Certifique-se de não compartilhar suas chaves de API publicamente.

---


## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/lucasmarcellodevitto/mba-ia-desafio-ingestao-busca-01.git
cd mba-ia-desafio-ingestao-busca-01
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Abra o arquivo `.env` e preencha sua chave da Google:

```env
GOOGLE_API_KEY=sua_chave
```
---

## Execução

### Passo 1 — Suba o banco de dados

```bash
docker compose up -d
```

Aguarde o container `postgres_rag` ficar com status `healthy`:

```bash
docker ps
```

### Passo 2 — Ingira o PDF

```bash
python src/ingest.py
```

Saída esperada:

```
Starting loading process
Ending loading process
```

> **Atenção:** A cada execução do `ingest.py` a coleção é recriada do zero, evitando duplicatas.

### Passo 3 — Inicie o chat

```bash
python src/chat.py
```

Exemplo de uso:

```
////////TODO
```

---

## Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca-01/
├── docker-compose.yml       # PostgreSQL + pgVector no Docker
├── requirements.txt         # Dependências Python
├── .env.example             # Template de variáveis de ambiente
├── .env                     # Variáveis de ambiente (Criado pelo usuario e não commitado)
├── README.md                # Este arquivo
└── src/
    ├── ingest.py            # Lê o PDF e salva os vetores no banco
    ├── search.py            # Busca semântica + chamada à LLM
    └── chat.py              # Interface CLI de perguntas e respostas
    └── files/               
        └──document.pdf      # PDF ingerido
```

---

## Como funciona

```
INGESTÃO
document.pdf → PyPDFLoader → chunks (1000 chars, overlap 150)
             → GoogleGenerativeAIEmbeddings (gemini-embedding-001)
             → PGVector → PostgreSQL (coleção mba_rag)

BUSCA
pergunta do usuário → vetorização → similarity_search(k=10)
                    → 10 chunks mais relevantes → prompt com contexto
                    → ChatGoogleGenerativeAI (gemini-2.5-flash-lite)
                    → resposta no terminal
```

---

## Variáveis de Ambiente

| Variável | Descrição | Valor padrão |
|----------|-----------|--------------|
| `GOOGLE_API_KEY` | Chave da API Google AI Studio | — |
| `GOOGLE_EMBEDDING_MODEL` | Modelo de embeddings | `gemini-embedding-001` |
| `GOOGLE_LLM_MODEL` | Modelo LLM para respostas | `gemini-2.5-flash-lite` |
| `DATABASE_URL` | String de conexão PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção no pgVector | `mba_rag` |
