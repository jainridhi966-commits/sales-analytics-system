from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from report_generator import generate_sales_report
import os


def main():
    """
    Main execution function
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse & clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Filter options (display only)
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(txn["Region"] for txn in transactions))
        amounts = [txn["Quantity"] * txn["UnitPrice"] for txn in transactions]
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts)} - ₹{max(amounts)}")

        # 4. Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_count, summary = validate_and_filter(transactions)
        print(f"✓ Valid: {len(valid_txns)} | Invalid: {invalid_count}")

        # 5. Analysis (Part 2)
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_txns)
        region_wise_sales(valid_txns)
        top_selling_products(valid_txns)
        customer_analysis(valid_txns)
        daily_sales_trend(valid_txns)
        find_peak_sales_day(valid_txns)
        low_performing_products(valid_txns)
        print("✓ Analysis complete")

        # 6. Fetch API products
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrich data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_txns, product_mapping)

        success_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
        success_rate = (success_count / len(valid_txns)) * 100
        print(f"✓ Enriched {success_count}/{len(valid_txns)} transactions ({success_rate:.1f}%)")

        # 8. Enriched data already saved inside function
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_txns, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(e)


if __name__ == "__main__":
    main()
