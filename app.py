import streamlit as st
with st.sidebar:
    st.header("📂 Upload Documents")
    st.file_uploader("Drop your PDFs or CSVs here")
st.title("Private Local Agent")
st.chat_message("assistant").write("Hello! I am ready to help. What is your question?")
st.chat_input("Type your message here...")