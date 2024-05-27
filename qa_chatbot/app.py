import streamlit as st
from streamlit_option_menu import option_menu
from similarity_search import search
from extract_data import create_embeddings
import chromadb

import time

import dotenv
dotenv.load_dotenv()
 
st.set_page_config(layout='wide')
 
st.title('PDF Summarizer and Chatbot')

if "uploaded_file_new" not in st.session_state:
    st.session_state["uploaded_file_new"] = None

if "uploaded_file_exist" not in st.session_state:
    st.session_state["uploaded_file_exist"] = None

if "summarized_content" not in st.session_state:
    st.session_state["summarized_content"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []
 
col1, col2 = st.columns([2,1])

with st.sidebar:
    selected = option_menu(
        menu_title="Select an Option",
        options=['Summarizer', 'Chatbot']
    )
 
if selected == "Summarizer":
    if not st.session_state["uploaded_file_new"] and not st.session_state["uploaded_file_exist"]:
        st.write('You can either upload a new file or select an exisiting one:')
        st.session_state["uploaded_file_new"] = st.file_uploader("Upload your file here")
        client = chromadb.PersistentClient(path="./chroma_db")
        created_files = [c.name for c in client.list_collections()]
        st.session_state["uploaded_file_exist"] = st.selectbox(
        "Select a file to chat",
        created_files, index=None)


    with col1:
        if st.session_state['uploaded_file_new']:
            st.write(f'Your file {st.session_state['uploaded_file_new'].name} has been uploaded successfully!')
        elif st.session_state['uploaded_file_exist']:
            st.write(f'Your file {st.session_state['uploaded_file_exist']} has been uploaded successfully!')
        if not st.session_state["summarized_content"]:
            st.write('Your summarized content will be displayed here')
        else:
            st.write(st.session_state["summarized_content"])

elif selected == 'Chatbot':
    if st.session_state['uploaded_file_new']:
            st.write(f'Your file {st.session_state['uploaded_file_new'].name} has been uploaded successfully!')
    elif st.session_state['uploaded_file_exist']:
        st.write(f'Your file {st.session_state['uploaded_file_exist']} has been uploaded successfully!')
    user_input = st.chat_input("Enter your query")
    if user_input:
        st.session_state["messages"].append({"role":"user", "content":user_input})

        create_embeddings(st.session_state["uploaded_file"])

        response = search(user_input, st.session_state["uploaded_file"])

        st.session_state["messages"].append({"role":"assistant", "content":response})

    for msg in st.session_state["messages"]:
        st.chat_message("role").write(msg["content"])