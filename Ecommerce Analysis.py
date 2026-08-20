import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("ecommerce_sales_analytics_5000.csv")

# Initial inspection
print("Shape:", df.shape)
print(df.head())
print(df.info())
print(df.describe())

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "quantity",
    "unit_price",
    "discount",
    "delivery_days",
    "customer_rating",
    "revenue"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean text columns
text_columns = [
    "product_category",
    "region",
    "payment_method"
]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Check missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Remove rows with missing critical values
critical_columns = [
    "order_id",
    "order_date",
    "customer_id",
    "product_category",
    "region",
    "quantity",
    "unit_price",
    "revenue"
]

df = df.dropna(subset=critical_columns)

# Validate quantity
df = df[df["quantity"] > 0]

# Validate unit price
df = df[df["unit_price"] > 0]

# Validate discount
df = df[
    (df["discount"] >= 0) &
    (df["discount"] <= 1)
]

# Validate delivery days
df = df[df["delivery_days"] >= 0]

# Validate customer rating
df = df[
    (df["customer_rating"] >= 1) &
    (df["customer_rating"] <= 5)
]

# Validate revenue
df = df[df["revenue"] >= 0]

# Create gross sales
df["gross_sales"] = (
    df["quantity"] * df["unit_price"]
)

# Create discount amount
df["discount_amount"] = (
    df["gross_sales"] * df["discount"]
)

# Create calculated revenue
df["calculated_revenue"] = (
    df["gross_sales"] -
    df["discount_amount"]
)

# Create time-based columns
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month_name()
df["month_number"] = df["order_date"].dt.month
df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
df["day_of_week"] = df["order_date"].dt.day_name()

# Revenue difference check
df["revenue_difference"] = (
    df["revenue"] - df["calculated_revenue"]
)

# Final checks
print("\nFinal shape:", df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows after cleaning:")
print(df.duplicated().sum())

print("\nFinal columns:")
print(df.columns.tolist())

print("\nCleaned dataset preview:")
print(df.head())

# Basic EDA
print("\nTotal Revenue:", df["revenue"].sum())
print("Total Orders:", df["order_id"].nunique())
print("Total Customers:", df["customer_id"].nunique())
print("Total Quantity:", df["quantity"].sum())

average_order_value = (
    df["revenue"].sum() /
    df["order_id"].nunique()
)

print("Average Order Value:", average_order_value)

# Revenue by category
category_analysis = (
    df.groupby("product_category")
    .agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("quantity", "sum"),
        average_rating=("customer_rating", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("\nRevenue by Category:")
print(category_analysis)

# Revenue by region
region_analysis = (
    df.groupby("region")
    .agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("quantity", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)

print("\nRevenue by Region:")
print(region_analysis)

# Revenue by payment method
payment_analysis = (
    df.groupby("payment_method")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Payment Method:")
print(payment_analysis)

# Top 10 customers
top_customers = (
    df.groupby("customer_id")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers:")
print(top_customers)

# Monthly revenue
monthly_analysis = (
    df.groupby(
        ["year", "month_number", "month"]
    )["revenue"]
    .sum()
    .reset_index()
    .sort_values(["year", "month_number"])
)

print("\nMonthly Revenue:")
print(monthly_analysis)

# Save cleaned dataset
df.to_csv(
    "ecommerce_sales_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")