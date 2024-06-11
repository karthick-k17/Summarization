import streamlit as st

file = st.file_uploader('Upload your file')
st.write(file.name)