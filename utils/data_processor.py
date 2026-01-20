
from collections import defaultdict
from datetime import datetime

def parse_transactions(lines):
    data = []
    for l in lines:
        parts = [p.strip() for p in l.replace(',', '').split('|')]
        if len(parts) < 8: continue
        try:
            data.append({
                'TransactionID': parts[0],
                'Date': parts[1],
                'ProductID': parts[2],
                'ProductName': parts[3],
                'Quantity': int(parts[4]),
                'UnitPrice': float(parts[5]),
                'CustomerID': parts[6],
                'Region': parts[7]
            })
        except:
            continue
    return data

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid, invalid = [], 0
    regions = set()
    amounts = []

    for t in transactions:
        try:
            if not t['TransactionID'].startswith('T'): raise ValueError
            if not t['ProductID'].startswith('P'): raise ValueError
            if not t['CustomerID'].startswith('C'): raise ValueError
            if t['Quantity'] <= 0 or t['UnitPrice'] <= 0: raise ValueError

            amount = t['Quantity'] * t['UnitPrice']
            regions.add(t['Region'])
            amounts.append(amount)

            if region and t['Region'] != region: continue
            if min_amount and amount < min_amount: continue
            if max_amount and amount > max_amount: continue

            valid.append(t)
        except:
            invalid += 1

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'filtered_by_region': len([t for t in valid if region]),
        'filtered_by_amount': len([t for t in valid if min_amount or max_amount]),
        'final_count': len(valid)
    }
    return valid, invalid, summary

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    total = calculate_total_revenue(transactions)
    stats = defaultdict(lambda: {'total_sales':0,'transaction_count':0})
    for t in transactions:
        amt = t['Quantity'] * t['UnitPrice']
        stats[t['Region']]['total_sales'] += amt
        stats[t['Region']]['transaction_count'] += 1
    for r in stats:
        stats[r]['percentage'] = round(stats[r]['total_sales']/total*100,2)
    return dict(sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    prod = defaultdict(lambda: {'qty':0,'rev':0})
    for t in transactions:
        prod[t['ProductName']]['qty'] += t['Quantity']
        prod[t['ProductName']]['rev'] += t['Quantity'] * t['UnitPrice']
    res = [(k,v['qty'],v['rev']) for k,v in prod.items()]
    return sorted(res, key=lambda x: x[1], reverse=True)[:n]
