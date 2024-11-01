import streamlit as st


def add_navigation():
    st.set_page_config(page_title="Nexo_admin", page_icon=":robot:", layout="wide")
    st.sidebar.header("Navigation")
    st.sidebar.page_link("main_page.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/admin.py", label="Admin", icon="🔑")
    st.sidebar.page_link("pages/chatbot.py", label="Chatbot", icon="👾")