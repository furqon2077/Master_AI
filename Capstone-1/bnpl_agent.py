import json
import sqlite3
from openai import OpenAI
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "Capstone-1", "db", "bnpl.db")


# DATABASE = "db/bnpl.db"

database_schema_string = """
Table: transactions
Columns: transaction_id, customer_id, merchant, category,
purchase_amount, installment_count, installment_amount,
purchase_date, final_due_date, status, credit_score,
risk_score, late_fee, default_flag
"""

def safe_sql_check(query: str):
    dangerous_words = ["drop", "delete", "truncate", "alter"]
    lower_sql = query.lower()
    if any(word in lower_sql for word in dangerous_words):
        print("❌ Dangerous SQL blocked:", query)
        raise Exception("Operation blocked: Unsafe SQL detected.")



def bnpl_database_query(query):
    safe_sql_check(query)
    print("🔍 Running SQL Query:", query)
    conn = sqlite3.connect(DATABASE)
    results = conn.execute(query).fetchall()
    conn.close()
    print("➡️ SQL Result:", results)
    return results


def create_support_ticket(issue: str):
    print("📝 Creating Support Ticket:", issue)
    ticket_id = f"TICKET-{abs(hash(issue)) % 100000}"
    with open("support_tickets.txt", "a") as f:
        f.write(f"{ticket_id}: {issue}\n")
    print("📨 Ticket Created:", ticket_id)
    return {"ticket_id": ticket_id, "issue": issue}


def run_bnpl_agent(user_message: str, openai_api_key: str) -> str:

    client = OpenAI(api_key=openai_api_key)

    tools = [
        {
            "type": "function",
            "name": "bnpl_database_query_1",
            "description": "Runs a safe SQL query on the BNPL database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": f"SQL using schema:\n{database_schema_string}"}
                },
                "required": ["query"],
            },
        },
        {
            "type": "function",
            "name": "create_support_ticket",
            "description": "Creates a support ticket for human assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "Describe the user's problem."}
                },
                "required": ["issue"],
            },
        }
    ]



    response = client.responses.create(
        model="gpt-4.1-2025-04-14",
        tools=tools,
        instructions="Respond to the user's question with a clear, concise, markdown-formatted answer based on the database result. Use tables or bullets if helpful.",
        input=[{"role": "user", "content": user_message}],
    )

    tool_result = None


    for item in response.output:
        if item.type == "function_call":
            args = json.loads(item.arguments)

            if item.name == "bnpl_database_query":
                tool_result = bnpl_database_query(args["query"])

            elif item.name == "create_support_ticket":
                tool_result = create_support_ticket(args["issue"])


    messages_for_final = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": str(tool_result)}
    ]

    final = client.responses.create(
        model="gpt-4.1-2025-04-14",
        instructions="Provide a clear, final answer. If a ticket was created, mention it. Show created ticket number.",
        input=messages_for_final,
    )

    return final.output_text
