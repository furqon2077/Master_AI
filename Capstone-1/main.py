import streamlit as st
from bnpl_agent import run_bnpl_agent

st.title("🦜Wellcome to the BNPL Chatbot")

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

st.markdown("""
### 🤖 BNPL Assistant Capabilities

The assistant provides two core functions:

## 1. Database Extraction

Users can retrieve essential BNPL information from the database:

- **Transaction data:** transaction ID, merchant, category, dates, status  
- **Customer info:** customer IDs linked to each transaction  
- **Financial metrics:** purchase amount, installments, due dates, late fees  
- **Risk metrics:** credit score, risk score, default flag  
- **Payment insights:** overdue, completed, and upcoming installments  

**Merchants:**  
Adidas, AliExpress, Amazon, Apple Store, BestBuy, IKEA, Nike, Target, Walmart, eBay  

**Categories:**  
Automotive, Beauty, Books, Electronics, Fashion, Grocery, Health, Home, Office, Sports  

## 2. Support Ticket Creation

If a user reports a problem (e.g., failed payment, system error, something not working),  
the assistant automatically generates a **support ticket** and returns a ticket number  
for tracking and follow-up.

This ensures issues are logged and can be reviewed by the support team.
""")