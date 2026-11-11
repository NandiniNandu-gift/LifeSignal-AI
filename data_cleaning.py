
import pandas as pd
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "Data" / "Raw" / "LifeSignal_AI_Personal_Finance_Raw.csv"
output_folder = ROOT / "Data" / "Cleaned"

# Check input file
if not input_file.exists():
    raise FileNotFoundError(f"Raw dataset not found: {input_file}")

# Load raw dataset
df = pd.read_csv(input_file)

print("--- RAW DATASET ---")
print("Total rows:", len(df))

# Standardize column names for SQL and Power BI
df.columns = df.columns.str.strip().str.lower()

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Convert amount to numeric
df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")

# Clean text columns
text_columns = [
    "transaction_id",
    "description",
    "category",
    "type",
    "payment_method",
    "account"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Remove missing important values
df = df.dropna(subset=[
    "transaction_id",
    "date",
    "category",
    "type",
    "amount_inr"
])

# Remove blank transaction IDs
df = df[df["transaction_id"] != ""]

# Remove duplicate transaction IDs
df = df.drop_duplicates(subset=["transaction_id"])

# Remove negative amounts
df = df[df["amount_inr"] >= 0]

# Standardize transaction types
df["type"] = df["type"].str.title()

# Keep valid transaction types
df = df[df["type"].isin(["Income", "Expense"])]

# Sort transactions by date
df = df.sort_values("date").reset_index(drop=True)

# Rename columns to match Power BI model
df = df.rename(columns={
    "date": "transaction_date",
    "type": "transaction_type",
    "account": "account_name"
})

# Create output folder
output_folder.mkdir(parents=True, exist_ok=True)

# Save cleaned dataset
output_file = output_folder / "personal_finance_cleaned.csv"
df.to_csv(output_file, index=False)

# Final report
print("\n--- CLEANING REPORT ---")
print("Cleaned transactions:", len(df))
print("Missing values:", df.isnull().sum().sum())
print("Duplicate transaction IDs:", df["transaction_id"].duplicated().sum())
print("Date column type:", df["transaction_date"].dtype)
print("Income transactions:", (df["transaction_type"] == "Income").sum())
print("Expense transactions:", (df["transaction_type"] == "Expense").sum())
print("Saved file:", output_file)

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
