import streamlit as st
from streamlit_option_menu import option_menu
from similarity_search import search
from extract_data import create_embeddings
from summarizer import summarize
import chromadb
from url_summarizer import url_summarize
import requests
import BeautifulSoup
from compound_to_simple import convertor
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

if "weburl" not in st.session_state:
    st.session_state["weburl"] = None

if "url_chat" not in st.session_state:
    st.session_state["url_chat"] = None
 
col1, col2 = st.columns([1,2])

with st.sidebar:
    selected = option_menu(
        menu_title="Select an Option",
        options=['Summarizer', 'Chatbot']
    )
 
if selected == "Summarizer":
    if not st.session_state["uploaded_file_sum"]:
        st.session_state["uploaded_file_sum"] = st.file_uploader("Upload your file here")

    if not st.session_state["weburl"]:
        st.session_state["weburl"] =st.text_input("Enter Webpage URL", type="default")

    if st.session_state["uploaded_file_sum"] or st.session_state["weburl"]:
        if st.session_state["uploaded_file_sum"]:
            converted_text = convertor('file', st.session_state["uploaded_file_sum"], None)
        else:
            converted_text = convertor('url', None, st.session_state["weburl"])
        
    with col1:
        if st.session_state['uploaded_file_sum']:
            # st.write(f'Your file {st.session_state['uploaded_file_sum'].name} has been uploaded successfully!')
            st.write(f'Your file has been uploaded successfully!')
            prompt = st.text_input('Enter the level of summarization required for the given file', key='prompt')
            keywords = st.text_input('Enter the key words that needs to given importance while summarizing', key='keywords')
            submit_button = False
            if not submit_button:
                submit_button = st.button("Submit", help="Click here to summarize")
            if submit_button:
                st.session_state["summarized_content"] = summarize(prompt, keywords, converted_text)
            
        if st.session_state['weburl']:
            prompt = st.text_input('Enter the level of summarization required for the given file', key='prompt')
            keywords = st.text_input('Enter the key words that needs to given importance while summarizing', key='keywords')
            submit_button = False
            if not submit_button:
                submit_button = st.button("Submit", help="Click here to summarize")
            if submit_button:
                st.session_state["summarized_content"] = url_summarize(prompt, keywords, converted_text)
        
    if st.session_state["summarized_content"] != None:
        st.write(st.session_state["summarized_content"])

elif selected == 'Chatbot':
    if not st.session_state["uploaded_file_new_chat"] and not st.session_state["uploaded_file_exist_chat"]:
        st.write('You can either upload a new file/URL or select an exisiting one:')
        st.session_state["uploaded_file_new_chat"] = st.file_uploader("Upload your file here")
        client = chromadb.PersistentClient(path="./chroma_db")
        created_files = [c.name for c in client.list_collections()]
        st.session_state["uploaded_file_exist_chat"] = st.selectbox(
            "Select a file to chat",
            created_files, 
            index=None
        )
        st.session_state["url_chat"] = st.text_input("Enter Webpage URL", type="default")
    if st.session_state['uploaded_file_new_chat']:
            # st.write(f'Your file {st.session_state['uploaded_file_new_chat'].name} has been uploaded successfully!')
            st.write(f'Your file has been uploaded successfully!')
            st.session_state["uploaded_file_name"] = st.session_state['uploaded_file_new_chat'].name
            create_embeddings('file', st.session_state["uploaded_file_new_chat"])
            
    elif st.session_state['uploaded_file_exist_chat']:
        # st.write(f"Your file {st.session_state['uploaded_file_exist_chat']} has been uploaded successfully!")
        st.write(f"Your file has been uploaded successfully!")
        st.session_state["uploaded_file_name"] = st.session_state['uploaded_file_exist_chat']

    elif st.session_state["url_chat"]:
        st.write(f"Your URL has been uploaded successfully!")
        reqs = requests.get(st.session_state["url_chat"])
 
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')
        
        # displaying the title
        print("Title of the website is : ")
        for title in soup.find_all('title'):
            file_name = title.get_text()
            st.session_state['uploaded_file_name'] = file_name.replace('\n', '').replace('.', ' ').replace(' ', '').strip()
            break

        create_embeddings('url', st.session_state["url_chat"])

    

    user_input = st.chat_input("Enter your query")
    if user_input:
        st.session_state["messages"].append({"role":"user", "content":user_input})

        response = search(user_input, st.session_state["uploaded_file_name"])

        st.session_state["messages"].append({"role":"assistant", "content":response})

    for msg in st.session_state["messages"]:
        st.chat_message("role").write(msg["content"])