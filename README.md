# Master_AI
Below is a clean, professional **README.md** for your **capstone-1 BNPL Chatbot project**, including features, tech stack, setup, deployment link, and code explanation.
You can copy–paste directly into **README.md**.

---

# 🦜 BNPL Chatbot — Capstone Project 1

A Streamlit-based AI assistant for querying Buy Now Pay Later (BNPL) transaction data using natural language and safe SQL execution.

🔗 **Live Demo:**
👉 [https://masterai-pdlexpsfgguevl34adiflu.streamlit.app/](https://masterai-pdlexpsfgguevl34adiflu.streamlit.app/)

---

## 📌 Overview

The **BNPL Chatbot App** allows users to ask natural-language questions about a BNPL transactions database.
The app uses an LLM agent to:

* Convert user questions into **safe SQL queries**
* Run the SQL on a local BNPL SQLite database
* Return concise, markdown-formatted responses
* Automatically create support tickets when needed

The dataset includes merchants such as **Amazon, eBay, Walmart, Target, Best Buy, IKEA, AliExpress, Apple Store, Nike, Adidas**, and multiple categories (Electronics, Sports, Health, etc.).

The system is implemented with:

* **Streamlit** (UI)
* **OpenAI Responses API (2025 models)**
* **SQLite** (Database)
* **Function Calling Tools** (SQL & ticket creation)

---

## 🚀 Features

### 🔍 BNPL Data Querying

Ask questions like:

* “What is the average purchase amount in the Electronics category?”
* “Which merchant has the highest total spending?”
* “How many customers defaulted on payments?”

### 🔒 Safe SQL Engine

The agent can only run SQL queries after passing through a safety checker that blocks:

* `DROP`
* `DELETE`
* `TRUNCATE`
* `ALTER`

### 🛠 Support Ticket System

If the user asks questions outside the dataset scope or operational questions,
the agent may automatically create a support ticket.

### 📊 Real-Time LLM-Processed Answers

* Uses OpenAI GPT-4.1 (2025-04-14) model
* Returns final answers in clean Markdown format
* Displays results using tables, bullets, and summaries

---

## 🧱 Project Structure

```
project/
│-- streamlit_app.py
│-- bnpl_agent.py
│-- db/
│   └── bnpl.db
│-- support_tickets.txt
│-- README.md
```

---

## 📝 Database Schema

```
Table: transactions
Columns:
- transaction_id
- customer_id
- merchant
- category
- purchase_amount
- installment_count
- installment_amount
- purchase_date
- final_due_date
- status
- credit_score
- risk_score
- late_fee
- default_flag
```

---

## 🧠 How the Agent Works

### 1️⃣ User enters a natural-language question

### 2️⃣ LLM decides whether to:

* execute a safe SQL query using `bnpl_database_query()`, or
* create a support ticket using `create_support_ticket()`

### 3️⃣ SQL Execution Flow

```python
def bnpl_database_query(query):
    safe_sql_check(query)
    conn = sqlite3.connect(DATABASE)
    results = conn.execute(query).fetchall()
    conn.close()
    return results
```

### 4️⃣ Ticket Creation

```python
def create_support_ticket(issue):
    ticket_id = f"TICKET-{abs(hash(issue)) % 100000}"
```

### 5️⃣ Final LLM Response

The agent produces a clean final answer summarizing the results.

---

## 💻 Running Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd capstone-1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit

```bash
streamlit run streamlit_app.py
```

### 4. Provide an OpenAI API Key

In the sidebar of the UI:

* Enter your key (`sk-....`)
* Ask your question
* Get instant insights from the BNPL dataset

---

## 🌐 Deployment

The project is deployed using **Streamlit Cloud**:

🔗 **Live App:**
[https://masterai-pdlexpsfgguevl34adiflu.streamlit.app/](https://masterai-pdlexpsfgguevl34adiflu.streamlit.app/)

---

## 📸 App Preview

```
🦜 Welcome to the BNPL Chatbot App

You can ask questions about the BNPL transactions dataset...
[Text Input Box]
[Submit Button]
```

---

## 🔧 Technologies Used

| Category       | Tools                        |
| -------------- | ---------------------------- |
| Frontend       | Streamlit                    |
| Language Model | OpenAI GPT-4.1 Responses API |
| Database       | SQLite                       |
| Backend Logic  | Python                       |
| Deployment     | Streamlit Cloud              |

---

## 🗂 Future Improvements

* Add charts and visual analytics
* Support multiple datasets
* Advanced multi-table join agent
* Authentication and user analytics

---

## 👨‍💻 Author

**Furkan Sidikov**
Backend Developer (Java) | ITPU Master's Student
