
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

        with open('output/sales_report.txt','w') as r:
            r.write("SALES ANALYTICS REPORT\n")
            r.write(f"Generated: {datetime.now()}\n")
            r.write(f"Total Revenue: {calculate_total_revenue(valid):,.2f}\n")

        print("Process Complete")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()
