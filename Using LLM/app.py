from flask import Flask, request, jsonify
import pandas as pd
from utils.llm_tools import (
    validate_dish_name,
    get_per100g_nutrition,
    get_main_ingredients,
    classify_category
)
from config import NUTRITION_CSV

try:
    nutrition_df = pd.read_csv(NUTRITION_CSV)
    nutrition_df.set_index("food_name", inplace=True)
except Exception as e:
    print(f"Error loading nutrition CSV: {e}")
    nutrition_df = pd.DataFrame()
    
    
app = Flask(__name__)

@app.route("/get_nutrition", methods=["POST"])
def get_nutrition():
    data = request.json or {}
    dish = data.get("dish_name", "").strip()
    if not dish:
        return jsonify({"error": "dish_name is required"}), 400
    if not validate_dish_name(dish):
        return jsonify({"error": "Not a valid dish. Please enter a valid dish name"}), 400
    if dish.lower() in [name.lower() for name in nutrition_df.index]:
        matched_row = nutrition_df.loc[
            nutrition_df.index.str.lower() == dish.lower()
        ].iloc[0]
        cals100 = matched_row.get("energy_kcal", 0.0)
        prot100 = matched_row.get("protein_g", 0.0)
        carbs100 = matched_row.get("carb_g", 0.0)
        fat100 = matched_row.get("fat_g", 0.0)
        source = "csv"
    else:
        cals100, prot100, carbs100, fat100 = get_per100g_nutrition(dish)
        source = "llm"


    ingredients = get_main_ingredients(dish)

    dish_type = classify_category(dish)
    if source == "llm":
        nutrition_200ml = {
            "calories": round(cals100 * 4, 2),
            "protein":  round(prot100 * 4, 2),
            "carbs":    round(carbs100 * 4, 2),
            "fat":      round(fat100 * 4, 2)
        }
    else :   
        nutrition_200ml = {
            "calories": round(cals100 * 2, 2),
            "protein":  round(prot100 * 2, 2),
            "carbs":    round(carbs100 * 2, 2),
            "fat":      round(fat100 * 2, 2)
        }

    return jsonify({
        "source": source,
        "estimated_nutrition_per_200ml_katori": nutrition_200ml,
        "dish_type": dish_type,
        "ingredients_used": ingredients
    })

if __name__ == "__main__":
    app.run(debug=True)
