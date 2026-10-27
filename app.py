
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Purchase Behaviour Analysis",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cleaned_retail_sales.csv"
SEGMENT_FILE = BASE_DIR / "data" / "customer_segments.csv"


@st.cache_data
def load_data():
    sales = pd.read_csv(DATA_FILE)
    sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"])
    sales["CustomerID"] = sales["CustomerID"].astype("Int64")

    segments = pd.read_csv(SEGMENT_FILE)
    segments["CustomerID"] = segments["CustomerID"].astype("Int64")

    return sales, segments


try:
    df, segments = load_data()
except FileNotFoundError as error:
    st.error(f"Required data file not found: {error.filename}")
    st.info(
        "Run clean_data.py and customer_segmentation.py "
        "before starting the dashboard."
    )
    st.stop()

# --------------------------------------------------
# 3. SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

countries = sorted(df["Country"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Select countries",
    countries,
    default=countries
)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select purchase date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.warning("Please select both a start date and an end date.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("The start date cannot be after the end date.")
    st.stop()

# Apply filters
filtered_df = df[
    df["Country"].isin(selected_countries)
    & (df["InvoiceDate"].dt.date >= start_date)
    & (df["InvoiceDate"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No sales records match your selected filters.")
    st.stop()

# --------------------------------------------------
# 4. DASHBOARD TITLE
# --------------------------------------------------

st.title("🛍️ Customer Purchase Behaviour Analysis")

st.markdown(
    "### Retail Sales Analytics Dashboard"
)

st.write(
    "Explore sales performance, product demand, "
    "and customer purchasing patterns."
)

st.divider()

# --------------------------------------------------
# 5. KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_revenue = filtered_df["SalesAmount"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_invoices = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()

average_order_value = (
    filtered_df.groupby("InvoiceNo")["SalesAmount"].sum().mean()
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Products Sold", f"{total_quantity:,.0f}")
col3.metric("Transactions", f"{total_invoices:,}")
col4.metric("Unique Customers", f"{total_customers:,}")
col5.metric("Average Order Value", f"£{average_order_value:,.2f}")

st.caption(
    "Revenue is calculated from positive-quantity sales lines "
    "in the selected date range and countries. Customer counts "
    "exclude records with missing CustomerID."
)

st.divider()

# --------------------------------------------------
# 6. MONTHLY SALES TREND
# --------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

filtered_df["YearMonth"] = (
    filtered_df["InvoiceDate"].dt.to_period("M").astype(str)
)

monthly_sales = (
    filtered_df.groupby("YearMonth")["SalesAmount"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£)")
ax.set_title("Monthly Revenue Trend")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 7. TOP PRODUCTS
# --------------------------------------------------

st.subheader("🏆 Top 10 Products by Quantity Sold")

top_products = (
    filtered_df.groupby("Description")["Quantity"]
    .sum()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 5))

top_products.plot(kind="barh", ax=ax)

ax.set_xlabel("Quantity Sold")
ax.set_ylabel("Product")
ax.set_title("Best-Selling Products")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 8. REVENUE BY COUNTRY
# --------------------------------------------------

st.subheader("🌍 Revenue by Country")

country_sales = (
    filtered_df.groupby("Country")["SalesAmount"]
    .sum()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 5))

country_sales.plot(kind="barh", ax=ax)

ax.set_xlabel("Revenue (£)")
ax.set_ylabel("Country")
ax.set_title("Top 10 Countries by Revenue")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 9. CUSTOMER SEGMENTATION
# --------------------------------------------------

st.subheader("👥 Customer Segmentation")

# Use only customers represented in the selected sales data
selected_customer_ids = (
    filtered_df["CustomerID"].dropna().unique()
)

filtered_segments = segments[
    segments["CustomerID"].isin(selected_customer_ids)
].copy()

if filtered_segments.empty:
    st.info("No identified customers are available for segmentation.")
else:
    segment_counts = (
        filtered_segments["CustomerSegment"]
        .value_counts()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("Customers by Segment")
        st.bar_chart(segment_counts)

    with col2:
        st.write("Customer Segment Summary")
        st.dataframe(
            segment_counts.rename("Number of Customers"),
            use_container_width=True
        )

# --------------------------------------------------
# 10. CUSTOMER SPENDING TABLE
# --------------------------------------------------

st.subheader("💰 Top 10 Customers by Spending")

customer_spending = (
    filtered_df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["SalesAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

customer_spending.columns = ["Customer ID", "Total Spending (£)"]

st.dataframe(
    customer_spending,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# 11. DOWNLOAD FILTERED DATA
# --------------------------------------------------

st.subheader("📥 Download Analysis Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data (CSV)",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
