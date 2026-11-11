
import pandas as pd
from pathlib import Path

# Load the raw dataset
file_path = Path(
    r"C:\Users\nn710\Downloads\LifeSignal_AI\Data\Raw\LifeSignal_AI_Personal_Finance_Raw.csv"
)

# Check whether dataset exists
if not file_path.exists():
    print("ERROR: Dataset file not found!")
    print("Expected file location:", file_path)
    raise SystemExit

# Read CSV dataset
df = pd.read_csv(file_path)

# Display first 5 transactions
print("\n--- FIRST 5 TRANSACTIONS ---")
print(df.head())

# Display dataset shape
print("\n--- DATASET SHAPE ---")
print(df.shape)

# Display column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# Display dataset information
print("\n--- DATASET INFORMATION ---")
df.info()

# Display missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# Display duplicate records
print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

# Display statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(df.describe(include="all"))

print("\n--- DATA INSPECTION COMPLETED ---")
