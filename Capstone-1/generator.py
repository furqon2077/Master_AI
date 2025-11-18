import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
n = 2000
np.random.seed(42)

# Lookup data
merchants = ["Amazon", "eBay", "Walmart", "Target", "BestBuy", "IKEA", "AliExpress", "Apple Store", "Nike", "Adidas"]
categories = ["Electronics", "Fashion", "Home", "Sports", "Beauty", "Automotive", "Grocery", "Books", "Office", "Health"]

# Generate fields
transaction_ids = [f"T{i:06d}" for i in range(1, n+1)]
customer_ids = [f"C{np.random.randint(1000, 9999)}" for _ in range(n)]
purchase_amounts = np.round(np.random.uniform(25, 5000, n), 2)
installment_counts = np.random.choice([3, 4, 6, 12, 18], n, p=[0.3, 0.25, 0.25, 0.15, 0.05])
installment_amounts = np.round(purchase_amounts / installment_counts, 2)

base_date = datetime(2023, 1, 1)
purchase_dates = [base_date + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n)]
final_due_dates = [purchase_dates[i] + timedelta(days=int(30 * int(installment_counts[i]))) for i in range(n)]

statuses = np.random.choice(["ongoing", "paid", "late", "defaulted"], n, p=[0.55, 0.25, 0.15, 0.05])

credit_scores = np.random.randint(300, 850, n)
risk_scores = np.round((850 - credit_scores) / 10 + np.random.uniform(-2, 2, n), 2)
risk_scores = np.clip(risk_scores, 0, 100)

merchant_list = np.random.choice(merchants, n)
category_list = np.random.choice(categories, n)

late_fees = np.where(statuses == "late", np.round(np.random.uniform(5, 50, n), 2), 0)
default_flags = np.where(statuses == "defaulted", 1, 0)

# Assemble dataframe
df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "customer_id": customer_ids,
    "merchant": merchant_list,
    "category": category_list,
    "purchase_amount": purchase_amounts,
    "installment_count": installment_counts,
    "installment_amount": installment_amounts,
    "purchase_date": purchase_dates,
    "final_due_date": final_due_dates,
    "status": statuses,
    "credit_score": credit_scores,
    "risk_score": risk_scores,
    "late_fee": late_fees,
    "default_flag": default_flags
})

file_path = "db/generated_transactions.csv"
df.to_csv(file_path, index=False)

file_path
