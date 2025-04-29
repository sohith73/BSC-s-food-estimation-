import json

with open('data/household_units.json') as f:
    UNIT_DB = json.load(f)

def convert_to_grams(mapped):
    results = []
    for item in mapped:
        unit_entry = UNIT_DB.get(item["ingredient"], {"grams_per_unit": 100})
        quantity = parse_quantity(item["quantity"])
        grams = quantity * unit_entry["grams_per_unit"]
        results.append({"ingredient": item["ingredient"], "grams": grams})
    return results

def parse_quantity(qty_str):
    try:
        parts = qty_str.split()
        value = float(parts[0])
        return value
    except:
        return 1.0
