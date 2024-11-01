import streamlit as st

# Redirect langsung ke halaman Home
st.experimental_set_query_params(page="1_Home")
st.experimental_rerun()