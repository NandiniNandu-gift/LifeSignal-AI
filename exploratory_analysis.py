
import pandas as pd
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "Data" / "Cleaned" / "personal_finance_cleaned.csv"
output_folder = ROOT / "Data" / "Processed"

# Load cleaned dataset
df = pd.read_csv(input_file, parse_dates=["transaction_date"])

output_folder.mkdir(parents=True, exist_ok=True)

# Financial summary
print("\n--- FINANCIAL SUMMARY ---")

total_income = df.loc[
    df["transaction_type"] == "Income", "amount_inr"
].sum()

total_expenses = df.loc[
    df["transaction_type"] == "Expense", "amount_inr"
].sum()

balance = total_income - total_expenses

print("Total Transactions:", len(df))
print("Total Income: ₹", total_income)
print("Total Expenses: ₹", total_expenses)
print("Net Balance: ₹", balance)

# Transaction type summary
print("\n--- TRANSACTION TYPE SUMMARY ---")

type_summary = df.groupby(
    "transaction_type"
)["amount_inr"].agg(["sum", "count", "mean"])

type_summary.to_csv(output_folder / "transaction_type_summary.csv")
print(type_summary)

# Monthly analysis
df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly_summary = df.pivot_table(
    index="month",
    columns="transaction_type",
    values="amount_inr",
    aggfunc="sum",
    fill_value=0
)

monthly_summary["Net_Balance"] = (
    monthly_summary.get("Income", 0)
    - monthly_summary.get("Expense", 0)
)

monthly_summary.to_csv(output_folder / "monthly_summary.csv")

print("\n--- MONTHLY SUMMARY ---")
print(monthly_summary)

# Category analysis
category_summary = df.groupby(
    ["transaction_type", "category"]
)["amount_inr"].agg(["sum", "count", "mean"]).reset_index()

category_summary = category_summary.sort_values(
    "sum", ascending=False
)

category_summary.to_csv(
    output_folder / "category_summary.csv", index=False
)

print("\n--- CATEGORY SUMMARY ---")
print(category_summary)

# Payment method analysis
payment_summary = df.groupby(
    "payment_method"
)["amount_inr"].agg(["sum", "count"]).reset_index()

payment_summary = payment_summary.sort_values(
    "sum", ascending=False
)

payment_summary.to_csv(
    output_folder / "payment_summary.csv", index=False
)

print("\n--- PAYMENT METHOD SUMMARY ---")
print(payment_summary)

# Account analysis
account_summary = df.pivot_table(
    index="account_name",
    columns="transaction_type",
    values="amount_inr",
    aggfunc="sum",
    fill_value=0
)

account_summary.to_csv(output_folder / "account_summary.csv")

print("\n--- ACCOUNT SUMMARY ---")
print(account_summary)

print("\nEDA COMPLETED SUCCESSFULLY!")
print("Output folder:", output_folder)
