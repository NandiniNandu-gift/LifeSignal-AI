
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

# Project paths
ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "Data" / "Cleaned" / "personal_finance_cleaned.csv"
output_folder = ROOT / "Data" / "Processed"

# Load cleaned dataset
df = pd.read_csv(input_file, parse_dates=["transaction_date"])

# Analyze expenses only
expenses = df[df["transaction_type"] == "Expense"].copy()

# Feature engineering
features = pd.DataFrame()

features["amount"] = expenses["amount_inr"]
features["day"] = expenses["transaction_date"].dt.day
features["month"] = expenses["transaction_date"].dt.month
features["category"] = expenses["category"].astype("category").cat.codes

# Train AI model
model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

# Predict unusual spending
predictions = model.fit_predict(features)

expenses["anomaly_flag"] = (predictions == -1).astype(int)

expenses["anomaly_status"] = expenses["anomaly_flag"].map({
    0: "Normal",
    1: "Review"
})

# Calculate category spending risk
category_average = expenses.groupby("category")["amount_inr"].transform("mean")

expenses["spending_risk"] = (
    expenses["amount_inr"] > category_average * 2
).map({
    True: "High",
    False: "Normal"
})

# Generate saving suggestions
def saving_suggestion(row):
    if row["anomaly_flag"] == 1:
        return "Review this unusual transaction"
    elif row["spending_risk"] == "High":
        return "Reduce spending in this category"
    else:
        return "Spending is within normal range"

expenses["saving_suggestion"] = expenses.apply(
    saving_suggestion, axis=1
)

# Save AI results
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "transaction_anomaly_flags.csv"

expenses.to_csv(output_file, index=False)

# AI report
print("\n--- AI RISK ANALYSIS REPORT ---")

print("Total Expense Transactions:", len(expenses))

print("Unusual Transactions:", expenses["anomaly_flag"].sum())

print(
    "High Spending Transactions:",
    (expenses["spending_risk"] == "High").sum()
)

print("\n--- FLAGGED TRANSACTIONS ---")

print(
    expenses[expenses["anomaly_flag"] == 1][
        [
            "transaction_date",
            "description",
            "category",
            "amount_inr",
            "anomaly_status",
            "saving_suggestion"
        ]
    ].to_string(index=False)
)

print("\nAI RISK ANALYSIS COMPLETED SUCCESSFULLY!")
print("Saved file:", output_file)
