import json

with open('data/nutrition_db.json') as f:
    NUTRITION_DB = json.load(f)

def map_ingredients(ingredients):
    mapped = []
    for item in ingredients:
        name = item["ingredient"].lower()
        match = next((k for k in NUTRITION_DB if name in k or k in name), None)
        if match:
            mapped.append({"ingredient": match, "quantity": item["quantity"]})
        else:
            mapped.append({"ingredient": "Unknown", "quantity": item["quantity"]})
    return mapped
