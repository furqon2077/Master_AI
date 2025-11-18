import os
import json
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-2025-04-14"
DATABASE = "db/bnpl.db"

database_schema_string = """
Table: transactions
Columns: transaction_id, customer_id, merchant, category, purchase_amount, installment_count, installment_amount, purchase_date, final_due_date, status, credit_score, risk_score, late_fee, default_flag
"""

# ------------------------
# TOOL DEFINITIONS
# ------------------------
tools = [
    {
        "type": "function",
        "name": "bnpl_database_query_1",
        "description": "Business query: runs SQL on BNPL database.",
        "parameters": {
            "type": "string",
                    "description": f"""
                        Generate an SQL query using the schema:
                        {database_schema_string}

                        IMPORTANT RULES:
                        - Use single quotes in SQL normally, like 'Electronics'
                        - DO NOT escape quotes (no backslashes)
                        - Output only raw SQL, not JSON, not Python code
                        - Do not wrap the SQL in quotes
                    """,
                "required": ["query"],
                    }
        },


    # Second main tool -------------------------------------------------------
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

# ------------------------
# SAFETY CHECK
# ------------------------
def safe_sql_check(query: str):
    dangerous = ["drop", "delete", "truncate", "alter"]
    if any(word in query.lower() for word in dangerous):
        print("❌ Dangerous SQL blocked:", query)
        raise Exception("Operation not allowed for safety reasons.")

# ------------------------
# SQL TOOL HANDLER
# ------------------------
def bnpl_database_query_1(query):
    safe_sql_check(query)
    print("🔍 Running Query #1:", query)
    conn = sqlite3.connect(DATABASE)
    results = conn.execute(query).fetchall()
    conn.close()
    print("➡️ Result:", results)
    return results

# ------------------------
# SUPPORT TICKET TOOL
# ------------------------
def create_support_ticket(issue: str):
    print("📝 Creating support ticket for issue:", issue)
    ticket_id = f"TICKET-{abs(hash(issue)) % 100000}"
    with open("support_tickets.txt", "a") as f:
        f.write(f"{ticket_id}: {issue}\n")
    print("📨 Created support ticket:", ticket_id)
    return {"ticket_id": ticket_id, "issue": issue}

# ------------------------
# USER REQUESTS
# ------------------------

# 1️⃣ First message → will use SQL tool
user_message_1 = {
    "role": "user",
    "content": "What is the average purchase amount for transactions in the 'Electronics' category?"
}

# 2️⃣ Second message → triggers support ticket tool
user_message_2 = {
    "role": "user",
    "content": "I think something is wrong with my results. Can you create a support ticket for me?"
}

user_requests = [user_message_1, user_message_2]

# ------------------------
# MAIN EXECUTION LOOP
# ------------------------
for request in user_requests:

    print("\n===============================")
    print("🤖 Handling Request:", request["content"])
    print("===============================")

    response = client.responses.create(
        model=MODEL,
        tools=tools,
        instructions="If user requests help or seems frustrated, call create_support_ticket.",
        input=[request],
    )

    tool_result = None

    for item in response.output:
        if item.type == "function_call":
            args = json.loads(item.arguments)

            if item.name == "bnpl_database_query_1":
                tool_result = bnpl_database_query_1(args["query"])

            elif item.name == "create_support_ticket":
                tool_result = create_support_ticket(args["issue"])

    # Feed tool result back for polished answer
    messages_for_final = [
        request,
        {"role": "assistant", "content": str(tool_result)}
    ]

    final = client.responses.create(
        model=MODEL,
        instructions="Answer clearly. If user had problems, confirm support ticket creation.",
        input=messages_for_final,
    )

    print("💬 Final Answer:")
    print(final.output_text)
    print("-----------------------------------")
