import streamlit as st
import pandas as pd
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
csv_name = "personal_finance_cleaned.csv"

# Check common locations: app folder, repository Data/Cleaned folder,
# and the parent folder (when dashboard.py is inside Python/).
possible_paths = [
    APP_DIR / "Data" / "Cleaned" / csv_name,
    APP_DIR.parent / "Data" / "Cleaned" / csv_name,
    APP_DIR / csv_name,
    APP_DIR.parent / csv_name,
]

input_file = next((path for path in possible_paths if path.exists()), None)

st.set_page_config(
    page_title="LifeSignal AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 LifeSignal AI")
st.subheader("Personal Finance Intelligence Dashboard")

if input_file is None:
    st.error(
        "Cleaned CSV file not found. Upload "
        "`personal_finance_cleaned.csv` to the repository root or "
        "`Data/Cleaned/` folder."
    )
    st.stop()

df = pd.read_csv(input_file, parse_dates=["transaction_date"])

if df.empty:
    st.warning("No transaction data available.")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

categories = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

if selected_category != "All":
    df = df[df["category"] == selected_category]

start_date = df["transaction_date"].min().date()
end_date = df["transaction_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(start_date, end_date)
)

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start, end = selected_dates
    df = df[df["transaction_date"].dt.date.between(start, end)]

# Financial calculations
income = df.loc[
    df["transaction_type"] == "Income", "amount_inr"
].sum()

expenses = df.loc[
    df["transaction_type"] == "Expense", "amount_inr"
].sum()

balance = income - expenses

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"₹{income:,.2f}")
col2.metric("Total Expenses", f"₹{expenses:,.2f}")
col3.metric("Net Balance", f"₹{balance:,.2f}")

# Monthly analysis
st.header("Monthly Financial Analysis")

df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly = df.pivot_table(
    index="month",
    columns="transaction_type",
    values="amount_inr",
    aggfunc="sum",
    fill_value=0
)

st.line_chart(monthly)

# Category analysis
st.header("Expense by Category")

expense_data = df[df["transaction_type"] == "Expense"]

category = expense_data.groupby("category")["amount_inr"].sum()

st.bar_chart(category)

# Account analysis
st.header("Account-wise Spending")

account = expense_data.groupby("account_name")["amount_inr"].sum()

st.bar_chart(account)

# Transaction details
st.header("Transaction Details")

st.dataframe(df, width="stretch")

st.success("LifeSignal AI Dashboard Loaded Successfully!")