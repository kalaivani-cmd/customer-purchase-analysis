
import pandas as pd
from pathlib import Path

# 1. Locate and load the cleaned dataset
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data" / "cleaned_retail_sales.csv"

df = pd.read_csv(FILE_PATH)

# Convert the invoice date into a date format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 2. Calculate overall sales metrics
total_revenue = df["SalesAmount"].sum()
total_products_sold = df["Quantity"].sum()
total_transactions = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()

# Calculate average order value
order_sales = df.groupby("InvoiceNo")["SalesAmount"].sum()
average_order_value = order_sales.mean()

# 3. Display the overall metrics
print("\n========== RETAIL SALES SUMMARY ==========")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Products Sold: {total_products_sold:,.0f}")
print(f"Total Transactions: {total_transactions:,}")
print(f"Total Unique Customers: {total_customers:,}")
print(f"Average Order Value: {average_order_value:,.2f}")

# 4. Find the top 10 products by quantity sold
top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY QUANTITY ==========")
print(top_products.to_string())

# 5. Find the top 10 countries by revenue
top_countries = (
    df.groupby("Country")["SalesAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 COUNTRIES BY REVENUE ==========")
print(top_countries.to_string())

# 6. Find the top 10 products by revenue
top_revenue_products = (
    df.groupby("Description")["SalesAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(top_revenue_products.to_string())

# 7. Save summary results
summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Products Sold",
        "Total Transactions",
        "Total Unique Customers",
        "Average Order Value",
    ],
    "Value": [
        total_revenue,
        total_products_sold,
        total_transactions,
        total_customers,
        average_order_value,
    ],
})

OUTPUT_FILE = BASE_DIR / "data" / "sales_summary.csv"
summary.to_csv(OUTPUT_FILE, index=False)

print("\nSales summary saved to:", OUTPUT_FILE)
print("\nSales analysis completed successfully!")
