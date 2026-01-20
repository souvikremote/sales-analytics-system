
import requests

def fetch_all_products():
    try:
        r = requests.get('https://dummyjson.com/products?limit=100', timeout=10)
        return r.json().get('products', [])
    except:
        return []

def create_product_mapping(products):
    return {p['id']: {
        'title': p['title'],
        'category': p['category'],
        'brand': p.get('brand', 'Unknown'),
        'rating': p.get('rating', 0)
    } for p in products}

def enrich_sales_data(transactions, product_mapping):
    enriched = []
    for t in transactions:
        pid = int(''.join(filter(str.isdigit, t['ProductID']))) - 100
        api = product_mapping.get(pid)
        t = t.copy()
        if api:
            t.update({
                'API_Category': api['category'],
                'API_Brand': api['brand'],
                'API_Rating': api['rating'],
                'API_Match': True
            })
        else:
            t.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })
        enriched.append(t)
    return enriched

def save_enriched_data(data, filename):
    with open(filename,'w') as f:
        headers = data[0].keys()
        f.write('|'.join(headers)+'\n')
        for d in data:
            f.write('|'.join(str(d[h]) for h in headers)+'\n')
