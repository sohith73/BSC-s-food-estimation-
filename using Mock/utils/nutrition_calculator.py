from utils.ingredient_mapper import NUTRITION_DB

def calculate_total(ingredients_in_grams):
    total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    for item in ingredients_in_grams:
        info = NUTRITION_DB.get(item["ingredient"], {})
        grams = item["grams"]
        for key in total:
            total[key] += (grams / 100) * info.get(key, 0)
    return total

def scale_to_serving(nutrition, dish_type):
    factor = 180 / 800  # ~1 serving of wet sabzi
    return {k: round(v * factor) for k, v in nutrition.items()}
