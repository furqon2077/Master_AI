import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from bnpl_agent import run_bnpl_agent

st.title("🦜Wellcome to the BNPL Chatbot App")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def generate_response(text):
    result = run_bnpl_agent(text, openai_api_key=openai_api_key)
    st.info(result)


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What is the average purchase amount for transactions in the 'Electronics' category?",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)