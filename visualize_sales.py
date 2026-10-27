
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cleaned_retail_sales.csv"
OUTPUT_DIR = BASE_DIR / "visualizations"

# Create the output folder if it does not exist
OUTPUT_DIR.mkdir(exist_ok=True)

# Load cleaned data
df = pd.read_csv(DATA_FILE)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Calculate customer spending
customer_spending = (
    df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["SalesAmount"]
    .sum()
    .sort_values(ascending=False)
)

# Calculate monthly revenue
monthly_sales = (
    df.groupby("YearMonth")["SalesAmount"]
    .sum()
    .sort_index()
)

# ---------------------------------------
# CHART 1: Top 10 products by quantity sold
# ---------------------------------------
top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_products.plot(kind="barh")
plt.title("Top 10 Best-Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_products.png", dpi=300)
plt.show()
plt.close()

# ---------------------------------------
# CHART 2: Top 10 countries by revenue
# ---------------------------------------
top_countries = (
    df.groupby("Country")["SalesAmount"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_countries.plot(kind="barh")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_countries.png", dpi=300)
plt.show()
plt.close()

# ---------------------------------------
# CHART 3: Monthly revenue trend
# ---------------------------------------
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Retail Sales Trend")
plt.xlabel("Year and Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_sales.png", dpi=300)
plt.show()
plt.close()

# ---------------------------------------
# CHART 4: Top 10 customers by spending
# ---------------------------------------
top_customers = customer_spending.nlargest(10).sort_values()

plt.figure(figsize=(10, 6))
top_customers.plot(kind="barh")
plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Total Spending")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_customers.png", dpi=300)
plt.show()
plt.close()

print("\nAll four visualizations were created successfully!")
print("Charts are saved in:", OUTPUT_DIR)
