def fetch_ingredients(dish_name):
    dummy_recipes = {
        "Paneer Butter Masala": [
            {"ingredient": "Paneer", "quantity": "0.75 cup"},
            {"ingredient": "Butter", "quantity": "2 tsp"},
            {"ingredient": "Tomato", "quantity": "0.5 cup puree"},
            {"ingredient": "Onion", "quantity": "0.5 cup"},
            {"ingredient": "Cream", "quantity": "1 tbsp"}
        ]
    }
    return dummy_recipes.get(dish_name, [])
