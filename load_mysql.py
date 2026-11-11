import pandas as pd
from sqlalchemy import create_engine, URL, text
from getpass import getpass
from pathlib import Path

# 1. Read cleaned CSV
file_path = Path("Data/Cleaned/personal_finance_cleaned.csv")

if not file_path.exists():
    raise FileNotFoundError(f"CSV file not found: {file_path}")

df = pd.read_csv(file_path)

# 2. Rename columns to match MySQL table
df.rename(columns={
    "date": "transaction_date",
    "type": "transaction_type",
    "account": "account_name"
}, inplace=True)

# 3. Required columns
required_columns = [
    "transaction_id",
    "transaction_date",
    "description",
    "category",
    "transaction_type",
    "amount_inr",
    "payment_method",
    "account_name"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing CSV columns: {missing_columns}")

df = df[required_columns].copy()

# 4. Data type conversion
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"], errors="raise"
).dt.date

df["amount_inr"] = pd.to_numeric(
    df["amount_inr"], errors="raise"
)

# 5. Check missing values and duplicate IDs
if df[["transaction_id", "transaction_date", "amount_inr"]].isnull().any().any():
    raise ValueError("Required columns contain missing values.")

if df["transaction_id"].duplicated().any():
    raise ValueError("Duplicate transaction IDs found in CSV.")

# 6. MySQL connection
username = "root"
password = getpass("Enter MySQL password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host="localhost",
    port=3306,
    database="lifesignal_ai"
)

engine = create_engine(connection_url)

# 7. Upload data (clear old rows to avoid duplicate IDs on reruns)
with engine.begin() as connection:

    connection.execute(text("DELETE FROM transactions"))

    df.to_sql(
        name="transactions",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=100
    )

    result = connection.execute(
        text("SELECT COUNT(*) FROM transactions")
    )

    total_rows = result.scalar()

# 8. Final output
print("\n--------------------------------")
print("LIFESIGNAL AI - MYSQL DATA LOAD")
print("--------------------------------")
print("Upload successful!")
print("CSV rows:", len(df))
print("MySQL rows:", total_rows)
print("--------------------------------")

engine.dispose()
