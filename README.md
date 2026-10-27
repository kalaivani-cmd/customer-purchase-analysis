# Customer Purchase Behaviour Analysis Using Retail Sales Data

## Project Overview

This project analyzes retail transaction data to understand customer purchasing behaviour, identify top-performing products, explore sales trends, and segment customers based on their purchasing patterns.

An interactive dashboard developed using Streamlit presents important sales metrics, visualizations, and customer segmentation results.

## Objectives

- Analyze retail sales and customer purchasing behaviour.
- Clean and preprocess retail transaction data.
- Calculate total revenue, products sold, transaction counts, and average order value.
- Identify top-performing products and countries.
- Analyze monthly sales trends.
- Perform customer segmentation using RFM analysis.
- Build an interactive dashboard using Streamlit.
- Allow users to filter sales data by country and date.
- Provide downloadable customer segmentation results.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook
- OpenPyXL
- Git and GitHub

## Dataset

The project uses the UCI Online Retail dataset.

The dataset contains information about invoices, products, quantities, prices, transaction dates, customer IDs, and countries.

Dataset source: https://archive.ics.uci.edu/dataset/352/online+retail

The original Excel dataset is not included in this repository. Download it from the source above and place `Online Retail.xlsx` inside the `data` folder before running the data preparation scripts.

## Features

- Interactive sales dashboard
- Key sales performance indicators
- Top-selling products analysis
- Country-wise revenue analysis
- Monthly sales visualization
- RFM-based customer segmentation
- Country and date filters
- CSV download functionality

## Customer Segmentation

RFM analysis uses three measurements:

- **Recency:** How recently a customer made a purchase.
- **Frequency:** How often a customer made purchases.
- **Monetary:** How much a customer spent.

These measurements help group customers according to their purchasing behaviour.

## Project Structure

```text
customer-purchase-analysis/
├── data/
├── notebooks/
├── screenshots/
├── visualizations/
├── test_dataset.py
├── clean_data.py
├── analyze_sales.py
├── visualize_sales.py
├── customer_segmentation.py
├── app.py
├── .gitignore
└── README.md
```

## Installation and Execution

### 1. Clone the repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd customer-purchase-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the required libraries

```bash
pip install pandas numpy matplotlib seaborn jupyter streamlit openpyxl
```

### 5. Download and prepare the dataset

Download the UCI Online Retail dataset and place `Online Retail.xlsx` inside the `data` folder.

Run these scripts in order:

```bash
python clean_data.py
python analyze_sales.py
python visualize_sales.py
python customer_segmentation.py
```

### 6. Run the dashboard

```bash
python -m streamlit run app.py
```

Open the local address displayed in your terminal, usually `http://localhost:8501`.

## Output

The project generates:

- Cleaned retail sales data
- Sales summary metrics
- Product and country visualizations
- Monthly sales charts
- Customer segmentation results
- An interactive Streamlit dashboard

## Future Enhancements

- Implement sales forecasting using machine learning.
- Improve analysis of cancelled invoices and product returns.
- Develop more advanced customer segmentation models.
- Deploy the dashboard online.

## Author

**Name:** Kalaivani V

**Department:** Artificial Intelligence and Data Science

**Project Title:** Customer Purchase Behaviour Analysis Using Retail Sales Data