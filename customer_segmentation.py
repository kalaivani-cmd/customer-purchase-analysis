
import pandas as pd
from pathlib import Path

# 1. Locate the project folder
BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "cleaned_retail_sales.csv"
OUTPUT_FILE = BASE_DIR / "data" / "customer_segments.csv"

# 2. Load the cleaned dataset
df = pd.read_csv(DATA_FILE)

# 3. Convert the invoice date to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 4. Remove records without a customer ID
customer_df = df.dropna(subset=["CustomerID"]).copy()

# Convert customer IDs to integers for consistent identification
customer_df["CustomerID"] = customer_df["CustomerID"].astype(int)

# 5. Define the analysis date
# One day after the latest transaction in the dataset
analysis_date = customer_df["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

# 6. Calculate RFM values
rfm = customer_df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda dates:
             (analysis_date - dates.max().normalize()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("SalesAmount", "sum")
).reset_index()

# 7. Calculate RFM scores
# Higher recency score = more recent purchase
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Higher frequency score = more purchases
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Higher monetary score = more spending
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# 8. Create a combined RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# 9. Assign simple customer segments
def assign_segment(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Best Customers"

    elif row["R_Score"] >= 3 and row["F_Score"] >= 4:
        return "Loyal Customers"

    elif row["R_Score"] >= 4 and row["F_Score"] <= 2:
        return "New or Promising Customers"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At-Risk Customers"

    else:
        return "Other Customers"

rfm["CustomerSegment"] = rfm.apply(assign_segment, axis=1)

# 10. Save the customer segmentation results
rfm.to_csv(OUTPUT_FILE, index=False)

# 11. Display the results
print("\n========== RFM CUSTOMER ANALYSIS ==========")

print("\nTotal customers analyzed:", len(rfm))

print("\nCustomer segments:")
print(rfm["CustomerSegment"].value_counts().to_string())

print("\nTop 10 customers by spending:")
print(
    rfm.sort_values("Monetary", ascending=False)[
        ["CustomerID", "Recency", "Frequency", "Monetary", "CustomerSegment"]
    ].head(10).to_string(index=False)
)

print("\nCustomer segmentation saved to:")
print(OUTPUT_FILE)

print("\nRFM analysis completed successfully!")
