from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock Nutrition Database
nutrition_db = {
    "Paneer": {"calories": 265, "protein": 18, "carbs": 2, "fat": 20, "fiber": 0},
    "Butter": {"calories": 717, "protein": 0.8, "carbs": 0.1, "fat": 81, "fiber": 0},
    "Tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2},
    "Onion": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1, "fiber": 1.7},
    "Cream": {"calories": 340, "protein": 2.5, "carbs": 3.0, "fat": 35, "fiber": 0},
    "Toor Dal": {"calories": 350, "protein": 25, "carbs": 60, "fat": 1.2, "fiber": 15},
    "Turmeric": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0},
    "Ghee": {"calories": 900, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0}
}

# Measurement Mappings
measurement_mappings = {
    ("Paneer", "cup cubes"): 150,
    ("Butter", "teaspoon"): 5,
    ("Tomato", "cup puree"): 240,
    ("Onion", "cup chopped"): 150,
    ("Cream", "tablespoon"): 15,
    ("Toor Dal", "cup"): 200,
    ("Turmeric", "teaspoon"): 2,
    ("Ghee", "tablespoon"): 15
}

# Dish Type Information
dish_type_info = {
    'Wet Sabzi': {'serving_descriptor': '200ml_katori', 'serving_size_g': 180},
    'Dry Sabzi': {'serving_descriptor': 'katori', 'serving_size_g': 100},
    'Dal': {'serving_descriptor': 'bowl', 'serving_size_g': 150},
    'Non-Veg Curry': {'serving_descriptor': 'bowl', 'serving_size_g': 200},
    'Unknown': {'serving_descriptor': 'standard_serving', 'serving_size_g': 200}
}

# Dish type mapping
dish_type_mapping = {
    'masala': 'Wet Sabzi',
    'curry': 'Wet Sabzi',
    'sabzi': 'Dry Sabzi',
    'dal': 'Dal',
    'chicken': 'Non-Veg Curry',
    'mutton': 'Non-Veg Curry'
}

# Recipes
recipes = {
    'paneer butter masala': [
        {'ingredient': 'Paneer', 'quantity': 0.75, 'unit': 'cup cubes'},
        {'ingredient': 'Butter', 'quantity': 2, 'unit': 'teaspoon'},
        {'ingredient': 'Tomato', 'quantity': 0.5, 'unit': 'cup puree'},
        {'ingredient': 'Onion', 'quantity': 0.5, 'unit': 'cup chopped'},
        {'ingredient': 'Cream', 'quantity': 1, 'unit': 'tablespoon'}
    ],
    'dal tadka': [
        {'ingredient': 'Toor Dal', 'quantity': 1, 'unit': 'cup'},
        {'ingredient': 'Turmeric', 'quantity': 0.5, 'unit': 'teaspoon'},
        {'ingredient': 'Tomato', 'quantity': 0.5, 'unit': 'cup chopped'},
        {'ingredient': 'Onion', 'quantity': 0.5, 'unit': 'cup chopped'},
        {'ingredient': 'Ghee', 'quantity': 2, 'unit': 'tablespoon'}
    ],
    'chicken curry': [
        {'ingredient': 'Chicken', 'quantity': 500, 'unit': 'grams'},
        {'ingredient': 'Onion', 'quantity': 1, 'unit': 'cup chopped'},
        {'ingredient': 'Tomato', 'quantity': 1, 'unit': 'cup puree'},
        {'ingredient': 'Ghee', 'quantity': 3, 'unit': 'tablespoon'}
    ],
    'aloo gobi': [
        {'ingredient': 'Potato', 'quantity': 2, 'unit': 'cups chopped'},
        {'ingredient': 'Cauliflower', 'quantity': 2, 'unit': 'cups chopped'},
        {'ingredient': 'Turmeric', 'quantity': 0.5, 'unit': 'teaspoon'},
        {'ingredient': 'Oil', 'quantity': 2, 'unit': 'tablespoon'}
    ]
}

def normalize_ingredient_name(name):
    name = name.lower().strip()
    if name.endswith('s'):
        name = name[:-1]
    name = name.replace(' ', '')
    return name.capitalize()

def classify_dish_type(dish_name):
    dish_name_lower = dish_name.lower()
    for keyword, dish_type in dish_type_mapping.items():
        if keyword in dish_name_lower:
            return dish_type
    return 'Unknown'

def convert_to_grams(ingredient, quantity, unit):
    normalized_ingredient = normalize_ingredient_name(ingredient)
    key = (normalized_ingredient, unit)
    if key in measurement_mappings:
        return quantity * measurement_mappings[key]
    else:
        generic_units = {'teaspoon': 5, 'tablespoon': 15, 'cup': 200, 'glass': 240, 'katori': 180}
        if unit in generic_units:
            return quantity * generic_units[unit]
        else:
            return None

def estimate_nutrition(dish_name):
    recipe = recipes.get(dish_name.lower())
    if not recipe:
        return {"error": "Could not fetch recipe."}
    
    dish_type = classify_dish_type(dish_name)
    info = dish_type_info.get(dish_type, dish_type_info['Unknown'])
    serving_size_g = info['serving_size_g']
    serving_descriptor = info['serving_descriptor']
    output_key = f"estimated_nutrition_per_{serving_descriptor}"
    
    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    total_grams = 0.0
    ingredients_used = []
    
    for item in recipe:
        ingredient = item['ingredient']
        quantity = item['quantity']
        unit = item['unit']
        
        normalized_ingredient = normalize_ingredient_name(ingredient)
        if normalized_ingredient not in nutrition_db:
            continue
        
        grams = convert_to_grams(ingredient, quantity, unit)
        if grams is None:
            continue
        
        nutrition = nutrition_db[normalized_ingredient]
        total_calories += (grams * nutrition['calories']) / 100
        total_protein += (grams * nutrition['protein']) / 100
        total_carbs += (grams * nutrition['carbs']) / 100
        total_fat += (grams * nutrition['fat']) / 100
        total_grams += grams
        
        ingredients_used.append({"ingredient": normalized_ingredient, "quantity": f"{quantity} {unit}"})
    
    if total_grams == 0:
        return {"error": "No valid ingredients found."}
    
    serving_ratio = serving_size_g / total_grams
    estimated_nutrition = {
        "calories": round(total_calories * serving_ratio),
        "protein": round(total_protein * serving_ratio),
        "carbs": round(total_carbs * serving_ratio),
        "fat": round(total_fat * serving_ratio)
    }
    
    return {
        output_key: estimated_nutrition,
        "dish_type": dish_type,
        "ingredients_used": ingredients_used
    }

# Original GET endpoint (optional)
@app.route("/nutrition", methods=["GET"])
def get_nutrition():
    dish_name = request.args.get('dish')
    if not dish_name:
        return jsonify({"error": "Please provide a dish name."}), 400
    
    result = estimate_nutrition(dish_name)
    return jsonify(result)

# New POST endpoint
@app.route("/nutrition", methods=["POST"])
def post_nutrition():
    data = request.get_json()
    if not data or 'dish_name' not in data:
        return jsonify({"error": "Please provide 'dish_name' in the request body."}), 400

    dish_name = data['dish_name']
    result = estimate_nutrition(dish_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
