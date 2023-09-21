import streamlit as st

if "llama_KEY" not in st.session_state:
    st.session_state["llama_KEY"] = ""

st.set_page_config(page_title="QA Settings", layout="wide")

st.title("QA Settings")

llama_key = st.text_input("API Key", value=st.session_state["llama_KEY"], max_chars=None, key=None, type='password')

saved = st.button("Save")

if saved:
    st.session_state["llama_KEY"] = llama_key
    