
import pandas as pd
from pathlib import Path

# 1. Define file paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "Online Retail.xlsx"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_retail_sales.csv"

# 2. Load the original dataset
print("Loading retail sales dataset...")
df = pd.read_excel(INPUT_FILE)

# 3. Display the original dataset size
print("\n--- ORIGINAL DATASET ---")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

# 4. Remove exact duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("\nDuplicate rows removed:", duplicates)

# 5. Convert important columns to appropriate data types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# 6. Remove rows missing essential transaction information
essential_columns = [
    "InvoiceNo",
    "InvoiceDate",
    "Description",
    "Quantity",
    "UnitPrice",
]

before = len(df)

df = df.dropna(subset=essential_columns)

print("Rows removed due to missing essential information:", before - len(df))

# 7. Remove rows with invalid quantities or prices
before = len(df)

df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

print("Rows removed due to non-positive quantity or price:", before - len(df))

# 8. Calculate the sales amount for each transaction line
df["SalesAmount"] = df["Quantity"] * df["UnitPrice"]

# 9. Add useful date-related columns
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

# 10. Save the cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

# 11. Display the final results
print("\n--- CLEANED DATASET ---")
print("Remaining rows:", len(df))
print("Remaining columns:", len(df.columns))
print("Missing customer IDs:", df["CustomerID"].isna().sum())
print("Total sales amount:", round(df["SalesAmount"].sum(), 2))

print("\nFirst five cleaned records:")
print(df.head())

print("\nCleaned dataset saved to:")
print(OUTPUT_FILE)

print("\nData cleaning completed successfully!")
