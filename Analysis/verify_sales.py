"""Recompute summary metrics from the included sales workbook; does not rebuild Tableau."""
from pathlib import Path
import json
import pandas as pd

root = Path(__file__).resolve().parents[1]
orders = pd.read_excel(root / "Data" / "2026-Tableau-Hands-On.xlsx", sheet_name="Orders")
required = ["Row ID", "Order ID", "Customer ID", "Order Date", "Sale Amount", "Profit", "Region", "Category"]
if orders[required].isna().any().any():
    raise ValueError("Missing values in required summary fields")
if orders["Row ID"].duplicated().any():
    raise ValueError("Duplicate source row IDs")
orders["Order Date"] = pd.to_datetime(orders["Order Date"], errors="raise")
sales = float(orders["Sale Amount"].sum())
profit = float(orders["Profit"].sum())
summary = {
    "source": "Data/2026-Tableau-Hands-On.xlsx / Orders",
    "scope": "All source rows; no dashboard filters applied",
    "rows": len(orders),
    "distinct_customers": int(orders["Customer ID"].nunique()),
    "distinct_orders": int(orders["Order ID"].nunique()),
    "order_date_min": str(orders["Order Date"].min().date()),
    "order_date_max": str(orders["Order Date"].max().date()),
    "sales": sales,
    "profit": profit,
    "profit_ratio": profit / sales if sales else None,
    "warning": "Executive preview has a different, unreconciled scope. No native Tableau workbook is included."
}
output = root / "Reports"
output.mkdir(exist_ok=True)
(output / "source_metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
orders.groupby("Region")[["Sale Amount", "Profit"]].sum().to_csv(output / "regional_sales_profit.csv")
orders.assign(Year=orders["Order Date"].dt.year).groupby(["Year", "Category"])["Sale Amount"].sum().to_csv(output / "annual_category_sales.csv")
print(json.dumps(summary, indent=2))
