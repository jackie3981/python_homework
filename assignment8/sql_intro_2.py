"""
This script summarizes order data from the lesson.db SQLite database,
calculates total revenue per product, and exports the summary to CSV.
"""

import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/lesson.db")

sql = """
        SELECT li.line_item_id,
            li.quantity,
            p.product_id,
            p.product_name,
            p.price
        FROM line_items li
        JOIN products p
        ON li.product_id = p.product_id;
"""

try:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(sql, conn)
except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)

if df.empty:
    print("No data found for the query.")
    exit(0)

df['total'] = df['quantity'] * df['price']

grouped = df.groupby("product_id").agg(
    times_ordered=("line_item_id", "count"),
    total_revenue=("total", "sum"),
    product_name=("product_name", "first")
)

sorted_df = grouped.sort_values(by="product_name")
print(sorted_df.head())

output_path = os.path.join(BASE_DIR, "order_summary.csv")
sorted_df.to_csv(output_path)
