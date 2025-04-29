MODEL_NAME = "bsc@q4_k_m"

LLM_SETTINGS = {
    "base_url": "http://localhost:1234/v1",   # LM Studio endpoint
    "api_key": "sk-no-key-required",          
    "model": MODEL_NAME,
    "streaming": False
}

NUTRITION_CSV = "nutrition_database.csv"

CATEGORIES = [
    "Dry Rice Item","Wet Rice Item","Veg Gravy","Veg Fry",
    "Non - Veg Gravy","Non - Veg Fry","Dals","Wet Breakfast Item",
    "Dry Breakfast Item","Chutneys","Plain Flatbreads",
    "Stuffed Flatbreads","Salads","Raita","Plain Soups",
    "Mixed Soups","Hot Beverages","Beverages","Snacks","Sweets"
]
