import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_chroma import Chroma
import google.generativeai as genai
import dotenv
import os

def search(query, file_name):

    print(file_name)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # qdrant = Qdrant.from_existing_collection(
    #     embeddings,
    #     path="./ollama_qdrant",
    #     collection_name="first_chapter",
    # )

    db = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=embeddings,
            collection_name=f"{file_name}"
    )

    retriever = db.as_retriever()

    #qdrant = Qdrant.from_existing_collection(
    #    embeddings,
    #    path="./local_qdrant",
    #    collection_name="my_documents",
    #)

    # found_docs = qdrant.similarity_search(query)

    # for doc in found_docs:	
    #     print(doc.page_content)
    # retriever = qdrant.as_retriever()

    found_docs = retriever.invoke(query)

    formatted_docs_list = []

    for doc in found_docs:	
        formatted_docs_list.append(doc.page_content)

    formatted_docs = " ".join(formatted_docs_list)

    print(formatted_docs)

    api_key = dotenv.get_key('../.env', key_to_get='GEMINI_API_KEY')

    genai.configure(api_key=api_key)

    #Defining model
    gen_config = genai.GenerationConfig(
        temperature=0.5,
    )

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config=gen_config,
        system_instruction=f'''Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.

    {formatted_docs}

    Question: 

    Helpful Answer:'''
    )

    #Prompt
    response = model.generate_content(f'{query}')


    return response.text
       
