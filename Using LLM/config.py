# config.py

MODEL_NAME = "dolphin-2.2.1-mistral-7b"

LLM_SETTINGS = {
    "base_url": "http://localhost:1234/v1",   # LM Studio endpoint
    "api_key": "sk-no-key-required",          # no key needed locally
    "model": MODEL_NAME,
    "streaming": False
}

# The 20 categories you provided
CATEGORIES = [
    "Dry Rice Item","Wet Rice Item","Veg Gravy","Veg Fry",
    "Non - Veg Gravy","Non - Veg Fry","Dals","Wet Breakfast Item",
    "Dry Breakfast Item","Chutneys","Plain Flatbreads",
    "Stuffed Flatbreads","Salads","Raita","Plain Soups",
    "Mixed Soups","Hot Beverages","Beverages","Snacks","Sweets"
]
