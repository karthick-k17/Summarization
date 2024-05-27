import streamlit as st

file = st.file_uploader('Upload your file:')
if file:
    with open(f'./tempDir/{file.name}', 'wb') as f:
        f.write(file.getbuffer())