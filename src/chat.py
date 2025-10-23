import os
from dotenv import load_dotenv
from search import search_prompt
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

def get_embeddings(provider): 
    if provider == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2
        )
    else:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        llm = ChatOpenAI(
            model_name="gpt-5-nano",
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    return embeddings, llm

def chat(embeddings, llm, vectorstore):

    print("Chat iniciado. Digite 'sair' para encerrar.\n")

    while True:
        query = input("Pergunta: ").strip()
        if query == "":
            print("Por favor, insira uma pergunta válida.\n")
            continue
        if query.lower() in ("sair", "exit", "quit"):
            print("Até mais!")
            break

        # Vetorizar a pergunta e Buscar os 10 resultados mais relevantes (k=10) no banco vetorial.
        vector = embeddings.embed_query(query)
        docs = vectorstore.similarity_search_by_vector(vector, k=10)

        # # Concatena os conteúdos para formar o contexto
        context = "\n\n".join([doc.page_content for doc in docs])

        # Montar o prompt
        prompt_template = search_prompt(context, query)

        # Chamar a LLM.
        answer = llm.invoke(prompt_template)
        # Retornar a resposta ao usuário.
        print(f"\nResposta: {answer.content}\n")


def main():
    embeddings, llm = get_embeddings(provider="gemini")

    # Conecta com o vetor armazenado no PostgreSQL (usa PGVECTOR_DB_URL do ambiente)
    vectorstore =PGVector(
        connection="postgresql://postgres:postgres@localhost:5432/rag",
        embeddings=embeddings,
    )

    chat(embeddings, llm, vectorstore)

if __name__ == "__main__":
    main()


