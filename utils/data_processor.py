def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """
    transactions = []

    for line in raw_lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean ProductName (remove commas)
        product_name = product_name.replace(',', '')

        # Clean numeric fields
        quantity = quantity.replace(',', '')
        unit_price = unit_price.replace(',', '')

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            continue

        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    # Collect regions and transaction amounts for display
    regions = set()
    amounts = []

    for txn in transactions:
        try:
            qty = txn['Quantity']
            price = txn['UnitPrice']
            amount = qty * price
            regions.add(txn['Region'])
            amounts.append(amount)

            # Validation rules
            if qty <= 0 or price <= 0:
                invalid_count += 1
                continue
            if not txn['TransactionID'].startswith('T'):
                invalid_count += 1
                continue
            if not txn['ProductID'].startswith('P'):
                invalid_count += 1
                continue
            if not txn['CustomerID'].startswith('C'):
                invalid_count += 1
                continue

            valid_transactions.append(txn)

        except KeyError:
            invalid_count += 1

    print("Available regions:", sorted(regions))
    if amounts:
        print("Transaction amount range:", min(amounts), "-", max(amounts))

    # Apply region filter
    if region:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t['Region'] == region]
        filtered_by_region = before - len(valid_transactions)

    # Apply amount filters
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)
        filtered = []
        for t in valid_transactions:
            amt = t['Quantity'] * t['UnitPrice']
            if min_amount is not None and amt < min_amount:
                continue
            if max_amount is not None and amt > max_amount:
                continue
            filtered.append(t)
        valid_transactions = filtered
        filtered_by_amount = before - len(valid_transactions)

    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn['Quantity'] * txn['UnitPrice']

    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """
    region_data = {}
    overall_total = 0.0

    # Step 1: Aggregate sales and count per region
    for txn in transactions:
        region = txn['Region']
        revenue = txn['Quantity'] * txn['UnitPrice']
        overall_total += revenue

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1

    # Step 2: Calculate percentage contribution
    for region in region_data:
        percentage = (region_data[region]['total_sales'] / overall_total) * 100
        region_data[region]['percentage'] = round(percentage, 2)

    # Step 3: Sort by total_sales (descending)
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}

    # Step 1: Aggregate quantity and revenue by product
    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = quantity * txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += quantity
        product_data[product]['revenue'] += revenue

    # Step 2: Convert to list of tuples
    product_list = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]

    # Step 3: Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n products
    return product_list[:n]

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    """
    product_data = {}

    # Step 1: Aggregate quantity & revenue per product
    for txn in transactions:
        product = txn['ProductName']
        qty = txn['Quantity']
        revenue = qty * txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {'quantity': 0, 'revenue': 0.0}

        product_data[product]['quantity'] += qty
        product_data[product]['revenue'] += revenue

    # Step 2: Convert to list of tuples
    product_list = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]

    # Step 3: Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n products
    return product_list[:n]

def customer_analysis(transactions):
    

    customer_data = {}

    for txn in transactions:
        cid = txn['CustomerID']
        amount = txn['Quantity'] * txn['UnitPrice']
        product = txn['ProductName']

        if cid not in customer_data:
            customer_data[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customer_data[cid]['total_spent'] += amount
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products'].add(product)

    # Final formatting
    result = {}
    for cid, data in customer_data.items():
        result[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(
                data['total_spent'] / data['purchase_count'], 2
            ),
            'products_bought': sorted(list(data['products']))
        }

    # Sort by total_spent descending
    return dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """

    daily = {}

    for txn in transactions:
        date = txn['Date']
        amount = txn['Quantity'] * txn['UnitPrice']
        customer = txn['CustomerID']

        if date not in daily:
            daily[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily[date]['revenue'] += amount
        daily[date]['transaction_count'] += 1
        daily[date]['customers'].add(customer)

    # Convert customer sets to counts
    for date in daily:
        daily[date]['unique_customers'] = len(daily[date]['customers'])
        del daily[date]['customers']

    # Sort chronologically
    return dict(sorted(daily.items()))

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """

    daily_data = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0.0
    txn_count = 0

    for date, data in daily_data.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date
            txn_count = data['transaction_count']

    return peak_date, max_revenue, txn_count

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    """

    product_data = {}

    for txn in transactions:
        product = txn['ProductName']
        qty = txn['Quantity']
        revenue = qty * txn['UnitPrice']

        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_data[product]['quantity'] += qty
        product_data[product]['revenue'] += revenue

    low_products = []

    for product, data in product_data.items():
        if data['quantity'] < threshold:
            low_products.append(
                (product, data['quantity'], data['revenue'])
            )

    # Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
