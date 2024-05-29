import streamlit as st
from streamlit_option_menu import option_menu
from similarity_search import search
from extract_data import create_embeddings
from summarizer import summarize
import chromadb

import dotenv
dotenv.load_dotenv()
 
st.set_page_config(layout='wide')
 
st.title('PDF Summarizer and Chatbot')

if "uploaded_file_sum" not in st.session_state:
    st.session_state["uploaded_file_sum"] = None

if "uploaded_file_new_chat" not in st.session_state:
    st.session_state["uploaded_file_new_chat"] = None

if "uploaded_file_exist_chat" not in st.session_state:
    st.session_state["uploaded_file_exist_chat"] = None

if "uploaded_file_name" not in st.session_state:
    st.session_state["uploaded_file_name"] = None

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
    if not st.session_state["uploaded_file_sum"]:
        st.session_state["uploaded_file_sum"] = st.file_uploader("Upload your file here")
        
    with col1:
        if st.session_state['uploaded_file_sum']:
            st.write(f'Your file {st.session_state['uploaded_file_sum'].name} has been uploaded successfully!')
            prompt = st.text_input('Enter the level of summarization required for the given file', key='prompt')
            keywords = st.text_input('Enter the key words that needs to given importance while summarizing', key='keywords')
            submit_button = False
            if not submit_button:
                submit_button = st.button("Submit", help="Click here to summarize")
            if submit_button:
                st.session_state["summarized_content"] = summarize(st.session_state['uploaded_file_sum'], prompt, keywords)
            
        if st.session_state["summarized_content"] != None:
            st.write(st.session_state["summarized_content"])

elif selected == 'Chatbot':
    if not st.session_state["uploaded_file_new_chat"] and not st.session_state["uploaded_file_exist_chat"]:
        st.write('You can either upload a new file or select an exisiting one:')
        st.session_state["uploaded_file_new_chat"] = st.file_uploader("Upload your file here")
        client = chromadb.PersistentClient(path="./chroma_db")
        created_files = [c.name for c in client.list_collections()]
        st.session_state["uploaded_file_exist_chat"] = st.selectbox(
            "Select a file to chat",
            created_files, 
            index=None
        )
    if st.session_state['uploaded_file_new_chat']:
            st.write(f'Your file {st.session_state['uploaded_file_new_chat'].name} has been uploaded successfully!')
            st.session_state["uploaded_file_name"] = st.session_state['uploaded_file_new_chat'].name
    elif st.session_state['uploaded_file_exist_chat']:
        st.write(f'Your file {st.session_state['uploaded_file_exist_chat']} has been uploaded successfully!')
        st.session_state["uploaded_file_name"] = st.session_state['uploaded_file_exist_chat']
    user_input = st.chat_input("Enter your query")
    if user_input:
        st.session_state["messages"].append({"role":"user", "content":user_input})

        if st.session_state['uploaded_file_new_chat']:
            create_embeddings(st.session_state["uploaded_file_new_chat"])

        response = search(user_input, st.session_state["uploaded_file_name"])

        st.session_state["messages"].append({"role":"assistant", "content":response})

    for msg in st.session_state["messages"]:
        st.chat_message("role").write(msg["content"])