import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI



load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

class Search:
  def __init__(self):
    for k in ("GOOGLE_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
      if not os.getenv(k):
          raise RuntimeError(f"Environment variable {k} is not set! Check your .env file.")
    
    self.embeddings = GoogleGenerativeAIEmbeddings(
          model=os.getenv("GOOGLE_EMBEDDING_MODEL", "gemini-embedding-001")
      )

    self.store = PGVector(
        embeddings=self.embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
      )

    self.llm = ChatGoogleGenerativeAI(
          model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite"),
          temperature=0,
      )
  
  def answer(self, question=None):
    results = self.store.similarity_search_with_score(question, k=10)
    context = "\n\n".join([doc.page_content for doc, _score in results])
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    response = self.llm.invoke(prompt)
    return response.content