
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "Data" / "Cleaned" / "personal_finance_cleaned.csv"
risk_file = ROOT / "Data" / "Processed" / "transaction_anomaly_flags.csv"
output_folder = ROOT / "Reports" / "figures"

# Load dataset
df = pd.read_csv(input_file, parse_dates=["transaction_date"])

output_folder.mkdir(parents=True, exist_ok=True)

# 1. Monthly Income vs Expenses
df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly = df.pivot_table(
    index="month",
    columns="transaction_type",
    values="amount_inr",
    aggfunc="sum",
    fill_value=0
)

monthly.plot(
    kind="line",
    marker="o",
    figsize=(12, 6)
)

plt.title("Monthly Income vs Expenses")
plt.xlabel("Month")
plt.ylabel("Amount (INR)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_folder / "monthly_analysis.png", dpi=300)
plt.show()
plt.close()

# 2. Category-wise Expenses
expenses = df[df["transaction_type"] == "Expense"]

category = expenses.groupby(
    "category"
)["amount_inr"].sum().sort_values(ascending=False)

category.plot(kind="bar", figsize=(11, 6))

plt.title("Category-wise Expense Analysis")
plt.xlabel("Category")
plt.ylabel("Amount (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "category_analysis.png", dpi=300)
plt.show()
plt.close()

# 3. Account-wise Spending
account = expenses.groupby(
    "account_name"
)["amount_inr"].sum().sort_values(ascending=False)

account.plot(kind="bar", figsize=(9, 5))

plt.title("Account-wise Spending Analysis")
plt.xlabel("Account")
plt.ylabel("Amount (INR)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(output_folder / "account_analysis.png", dpi=300)
plt.show()
plt.close()

# 4. AI Risk Detection
if risk_file.exists():
    risk_df = pd.read_csv(risk_file)

    risk_counts = risk_df["anomaly_status"].value_counts()

    risk_counts.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title("AI Unusual Spending Detection")
    plt.xlabel("Transaction Status")
    plt.ylabel("Number of Transactions")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_folder / "ai_risk_analysis.png", dpi=300)
    plt.show()
    plt.close()

else:
    print("AI risk file not found. Run AI risk detection first.")

print("\nALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("Charts saved in:", output_folder)
