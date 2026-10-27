
import pandas as pd

# Load the retail sales dataset
file_path = "data/Online Retail.xlsx"
df = pd.read_excel(file_path)

# 1. Display the first five rows
print("\n========== FIRST FIVE ROWS ==========")
print(df.head())

# 2. Display the number of rows and columns
print("\n========== DATASET SIZE ==========")
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])

# 3. Display column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# 4. Check missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 5. Check duplicate rows
print("\n========== DUPLICATE ROWS ==========")
print("Total duplicate rows:", df.duplicated().sum())

# 6. Display data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# 7. Display basic numerical statistics
print("\n========== BASIC STATISTICS ==========")
print(df.describe())

print("\nDataset inspection completed successfully!")
