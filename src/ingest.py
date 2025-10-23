import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from pathlib import Path

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

api_key_gemini = os.getenv("GOOGLE_API_KEY")

def ingest_pdf(pdf_path, provider="gemini"):
    """
    Reads a PDF, splits text, creates embeddings (OpenAI/Gemini), and ingests into Postgres.
    
    Args:
        pdf_path (str): Path to the PDF file
        pgvector_url (str): Connection string for PGVector/Postgres
        use_openai (bool): Whether to create OpenAI embeddings
        use_gemini (bool): Whether to create Gemini embeddings

    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    
    # --- Step 1: Load PDF ---
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # --- Step 2: Split text into chunks ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)

    # --- Step 3: Choose the embeddings model ---
    if provider == "gemini":
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    # 4. Vetorizar todos os chunks antes de armazenar
    texts = [doc.page_content for doc in split_docs]

    # 5. Criar vetorstore PGVector conectado ao Postgres
    vectorstore = PGVector(
        connection=os.getenv("DATABASE_URL"),
        embeddings=embeddings_model,
    )

    for i, text in enumerate(texts, start=1):

        vectorstore.add_texts([text])
        print(f"Inserted chunk {i}/{len(texts)}")

        time.sleep(1)

    
    print("✅ Embeddings gerados com sucesso!")



if __name__ == "__main__":
    pdf_path = Path(__file__).parent.parent / 'document.pdf'

    search_fn = ingest_pdf(pdf_path=str(pdf_path))

