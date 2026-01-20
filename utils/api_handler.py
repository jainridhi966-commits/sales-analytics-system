import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except Exception:
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is not None:
            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

    return product_mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            numeric_id = int(txn["ProductID"][1:])
            product_info = product_mapping.get(numeric_id)

            if product_info:
                enriched_txn["API_Category"] = product_info["category"]
                enriched_txn["API_Brand"] = product_info["brand"]
                enriched_txn["API_Rating"] = product_info["rating"]
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    save_enriched_data(enriched_transactions)
    return enriched_transactions

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(header)

            for txn in enriched_transactions:
                line = (
                    f"{txn['TransactionID']}|{txn['Date']}|{txn['ProductID']}|"
                    f"{txn['ProductName']}|{txn['Quantity']}|{txn['UnitPrice']}|"
                    f"{txn['CustomerID']}|{txn['Region']}|"
                    f"{txn.get('API_Category')}|{txn.get('API_Brand')}|"
                    f"{txn.get('API_Rating')}|{txn.get('API_Match')}\n"
                )
                file.write(line)
    except Exception:
        pass
