
def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc, errors='ignore') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                return lines[1:]
        except FileNotFoundError:
            print("File not found.")
            return []
        except:
            continue
    return []
