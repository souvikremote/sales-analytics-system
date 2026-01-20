
from utils.file_handler import read_sales_data
from utils.data_processor import *
from utils.api_handler import *
from datetime import datetime

def main():
    try:
        print("SALES ANALYTICS SYSTEM")
        lines = read_sales_data('data/sales_data.txt')
        print(f"Read {len(lines)} lines")

        tx = parse_transactions(lines)
        print(f"Parsed {len(tx)} records")

        valid, invalid, summary = validate_and_filter(tx)
        print(f"Valid: {len(valid)} | Invalid: {invalid}")

        products = fetch_all_products()
        mapping = create_product_mapping(products)
        enriched = enrich_sales_data(valid, mapping)
        save_enriched_data(enriched, 'data/enriched_sales_data.txt')

       total_revenue = calculate_total_revenue(valid)
avg_order_value = total_revenue / len(valid) if valid else 0

regions = region_wise_sales(valid)
top_products = top_selling_products(valid, n=5)

# customer analysis (simple)
customer_stats = {}
for t in valid:
    cid = t["CustomerID"]
    amt = t["Quantity"] * t["UnitPrice"]
    if cid not in customer_stats:
        customer_stats[cid] = {"total_spent": 0, "order_count": 0}
    customer_stats[cid]["total_spent"] += amt
    customer_stats[cid]["order_count"] += 1

top_customers = sorted(
    customer_stats.items(),
    key=lambda x: x[1]["total_spent"],
    reverse=True
)[:5]

# API enrichment summary
enriched_success = sum(1 for t in enriched if t.get("API_Match"))
enriched_total = len(enriched)
success_rate = (enriched_success / enriched_total * 100) if enriched_total else 0

dates = sorted(set(t["Date"] for t in valid))
date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

with open("output/sales_report.txt", "w", encoding="utf-8") as r:
    r.write("SALES ANALYTICS REPORT\n")
    r.write("=" * 60 + "\n")
    r.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    r.write(f"Records Processed: {len(valid)}\n\n")

    r.write("OVERALL SUMMARY\n")
    r.write("-" * 60 + "\n")
    r.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
    r.write(f"Total Transactions: {len(valid)}\n")
    r.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
    r.write(f"Date Range: {date_range}\n\n")

    r.write("REGION-WISE PERFORMANCE\n")
    r.write("-" * 60 + "\n")
    r.write(f"{'Region':<10}{'Sales':>15}{'% Total':>10}{'Txns':>10}\n")
    for region, stats in regions.items():
        r.write(f"{region:<10}₹{stats['total_sales']:>14,.2f}{stats['percentage']:>9.2f}%{stats['transaction_count']:>10}\n")
    r.write("\n")

    r.write("TOP 5 PRODUCTS\n")
    r.write("-" * 60 + "\n")
    r.write(f"{'Rank':<6}{'Product':<25}{'Qty':>8}{'Revenue':>15}\n")
    for i, (name, qty, rev) in enumerate(top_products, 1):
        r.write(f"{i:<6}{name:<25}{qty:>8}₹{rev:>14,.2f}\n")
    r.write("\n")

    r.write("TOP 5 CUSTOMERS\n")
    r.write("-" * 60 + "\n")
    r.write(f"{'Rank':<6}{'CustomerID':<15}{'Spent':>15}{'Orders':>10}\n")
    for i, (cid, info) in enumerate(top_customers, 1):
        r.write(f"{i:<6}{cid:<15}₹{info['total_spent']:>14,.2f}{info['order_count']:>10}\n")
    r.write("\n")

    r.write("API ENRICHMENT SUMMARY\n")
    r.write("-" * 60 + "\n")
    r.write(f"Enriched Transactions: {enriched_success}/{enriched_total}\n")
    r.write(f"Success Rate: {success_rate:.2f}%\n")

        print("Process Complete")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
