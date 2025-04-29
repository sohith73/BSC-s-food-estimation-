# app.py

from flask import Flask, request, jsonify
from utils.llm_tools import (
    validate_dish_name,
    get_per100g_nutrition,
    get_main_ingredients,
    classify_category
)

app = Flask(__name__)

@app.route("/get_nutrition", methods=["POST"])
def get_nutrition():
    data = request.json or {}
    dish = data.get("dish_name", "").strip()
    if not dish:
        return jsonify({"error": "dish_name is required"}), 400
    if not validate_dish_name(dish):
        return jsonify({"error": "Not a valid dish. Please enter a valid dish name"}), 400

    cals100, prot100, carbs100, fat100 = get_per100g_nutrition(dish)

    ingredients = get_main_ingredients(dish)

    dish_type = classify_category(dish)
    nutrition_200ml = {
        "calories": round(cals100 * 2, 2),
        "protein":  round(prot100 * 2, 2),
        "carbs":    round(carbs100 * 2, 2),
        "fat":      round(fat100 * 2, 2)
    }

    return jsonify({
        "estimated_nutrition_per_200ml_katori": nutrition_200ml,
        "dish_type": dish_type,
        "ingredients_used": ingredients
    })

if __name__ == "__main__":
    app.run(debug=True)
