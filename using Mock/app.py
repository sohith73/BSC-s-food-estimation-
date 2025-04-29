from flask import Flask, request, jsonify
from utils import (
    recipe_fetcher, ingredient_mapper,
    unit_converter, nutrition_calculator,
    food_classifier, fallback
)

app = Flask(__name__)

@app.route('/estimate_nutrition', methods=['POST'])
def estimate():
    dish_name = request.json.get("dish_name")

    try:
        ingredients = recipe_fetcher.fetch_ingredients(dish_name)
        mapped = ingredient_mapper.map_ingredients(ingredients)
        grams = unit_converter.convert_to_grams(mapped)
        nutrition = nutrition_calculator.calculate_total(grams)
        dish_type = food_classifier.classify(dish_name)
        per_serving = nutrition_calculator.scale_to_serving(nutrition, dish_type)

        return jsonify({
            "estimated_nutrition_per_200ml_katori": per_serving,
            "dish_type": dish_type,
            "ingredients_used": ingredients
        })

    except Exception as e:
        return jsonify(fallback.handle_exception(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
