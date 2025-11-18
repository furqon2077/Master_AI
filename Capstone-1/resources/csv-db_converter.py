import pandas as pd
import sqlite3

df = pd.read_csv("generated_transactions.csv")

conn = sqlite3.connect("../db/bnpl.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)