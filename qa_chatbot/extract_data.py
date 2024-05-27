import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_chroma import Chroma
import chromadb
from qdrant_client import QdrantClient
import google.generativeai as genai
import dotenv
import os

def create_embeddings(file_path):
    file_name = file_path.split('/')[-1]
    print(file_name)

    client = chromadb.PersistentClient(path="./chroma_db")

    if f"{file_name}" in [c.name for c in client.list_collections()]:
        print('Collection exists')
        return
    
    # client = QdrantClient(
    #     path='./ollama_qdrant'
    # )
    # if client.collection_exists(collection_name=f"{file_name}"):
    #     return
    
    pdf_file = PyPDF2.PdfReader(file_path)
    extracted_text = ""
    for page in pdf_file.pages:
        extracted_text += ' ' + page.extract_text()

    processed_text = extracted_text.replace('\n', ' ')

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        separators=[
            " ",
            ".",
            "",
        ]
    )
    #Get API Key
    # api_key = dotenv.get_key('../.env', key_to_get='GEMINI_API_KEY')


    # if "GOOGLE_API_KEY" not in os.environ:
    #     os.environ["GOOGLE_API_KEY"] = api_key
    
    texts = text_splitter.create_documents([processed_text])

    #embeddings = GoogleGenerativeAIEmbeddings(api_key=api_key,model="models/embedding-001")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # qdrant = Qdrant.from_documents(
    #     texts,
    #     embeddings,
    #     path="./ollama_qdrant",
    #     collection_name=f"{file_name}",
    # )
    # client.close()

    print('Creating embeddings!')

    db = Chroma.from_documents(
        texts, 
        embeddings, 
        persist_directory="./chroma_db",
        collection_name=f"{file_name}"
    )

if __name__ == '__main__':
    create_embeddings('../files/first_chapter.pdf')