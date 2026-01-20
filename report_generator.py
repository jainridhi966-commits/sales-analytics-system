from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- BASIC CALCULATIONS ----------
    total_transactions = len(transactions)
    total_revenue = sum(txn["Quantity"] * txn["UnitPrice"] for txn in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(txn["Date"] for txn in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # ---------- REGION-WISE PERFORMANCE ----------
    region_data = {}
    for txn in transactions:
        region = txn["Region"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        if region not in region_data:
            region_data[region] = {"sales": 0, "count": 0}

        region_data[region]["sales"] += amount
        region_data[region]["count"] += 1

    region_rows = []
    for region, data in region_data.items():
        percentage = (data["sales"] / total_revenue) * 100 if total_revenue else 0
        region_rows.append((region, data["sales"], percentage, data["count"]))

    region_rows.sort(key=lambda x: x[1], reverse=True)

    # ---------- TOP 5 PRODUCTS ----------
    product_data = {}
    for txn in transactions:
        name = txn["ProductName"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += txn["Quantity"]
        product_data[name]["revenue"] += revenue

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:5]

    # ---------- TOP 5 CUSTOMERS ----------
    customer_data = {}
    for txn in transactions:
        cid = txn["CustomerID"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        if cid not in customer_data:
            customer_data[cid] = {"spent": 0, "count": 0}

        customer_data[cid]["spent"] += amount
        customer_data[cid]["count"] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY SALES TREND ----------
    daily_data = {}
    for txn in transactions:
        date = txn["Date"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        if date not in daily_data:
            daily_data[date] = {"revenue": 0, "count": 0, "customers": set()}

        daily_data[date]["revenue"] += amount
        daily_data[date]["count"] += 1
        daily_data[date]["customers"].add(txn["CustomerID"])

    # ---------- API ENRICHMENT SUMMARY ----------
    enriched_success = [txn for txn in enriched_transactions if txn.get("API_Match")]
    enriched_failed = [txn for txn in enriched_transactions if not txn.get("API_Match")]

    success_rate = (len(enriched_success) / len(enriched_transactions) * 100) if enriched_transactions else 0

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:

        f.write("=" * 44 + "\n")
        f.write("        SALES ANALYTICS REPORT\n")
        f.write(f"      Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"      Records Processed: {total_transactions}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write("Region    Sales        % of Total   Transactions\n")
        for r, sales, pct, cnt in region_rows:
            f.write(f"{r:<9} ₹{sales:,.0f}     {pct:>6.2f}%       {cnt}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  Product Name        Qty Sold   Revenue\n")
        for i, (name, data) in enumerate(top_products, 1):
            f.write(f"{i:<5} {name:<18} {data['qty']:<9} ₹{data['revenue']:,.0f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  Customer ID   Total Spent   Orders\n")
        for i, (cid, data) in enumerate(top_customers, 1):
            f.write(f"{i:<5} {cid:<12} ₹{data['spent']:,.0f}   {data['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write("Date         Revenue     Transactions  Unique Customers\n")
        for date in sorted(daily_data):
            d = daily_data[date]
            f.write(f"{date}  ₹{d['revenue']:,.0f}     {d['count']:<13} {len(d['customers'])}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Products Enriched: {len(enriched_success)}\n")
        f.write(f"Success Rate:            {success_rate:.2f}%\n")
        f.write("Failed Enrichments:\n")
        for txn in enriched_failed:
            f.write(f"- {txn['ProductName']}\n")
