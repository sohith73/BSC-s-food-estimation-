from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config import LLM_SETTINGS, CATEGORIES
import json
import re

llm = ChatOpenAI(**LLM_SETTINGS)

def validate_dish_name(dish_name: str) -> bool:
    msgs = [
        SystemMessage(content=(
            "Only answer 'yes' or 'no'. User will give you a dish name. "
            "Say 'yes' if it is a valid Indian dish, 'no' otherwise."
        )),
        HumanMessage(content=dish_name)
    ]
    resp = llm(msgs).content.strip().lower()
    return resp == "yes"

def get_per100g_nutrition(dish_name: str):
    msgs = [
        SystemMessage(content=(
            "For the Indian dish named below, return four numbers "
            "(calories, protein_g, carbs_g, fat_g) per 100 grams, "
            "comma-separated only. For example: 140,6,5,9. "
            "Do NOT include any explanation or units—only the numbers."
        )),
        HumanMessage(content=dish_name)
    ]
    raw = llm(msgs).content
    first_line = None
    for line in raw.splitlines():
        line = line.strip()
        if re.match(r'^[\d\.,\s]+$', line) and line.count(',') >= 3:
            first_line = line
            break
    if first_line is None:
        first_line = raw.split('\n', 1)[0].strip()
    parts = [p.strip() for p in first_line.split(',') if p.strip()]
    parts = parts[:4]
    try:
        cals, prot, carbs, fat = map(float, parts)
    except Exception:
        cals = prot = carbs = fat = 0.0

    return cals, prot, carbs, fat


def get_main_ingredients(dish_name: str):
    msgs = [
        SystemMessage(content=(
            "List only the main solid ingredients for this dish (no juices, garnishes, "
            "or secondary items). Return a JSON array of objects with keys "
            "`ingredient` and `quantity`.  "
            "Example: `[{\"ingredient\":\"Paneer\",\"quantity\":\"0.75 cup cubes\"}, …]`"
        )),
        HumanMessage(content=dish_name)
    ]
    resp = llm(msgs).content.strip()
    try:
        data = json.loads(resp)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
    except:
        pass
    return []

def classify_category(dish_name: str) -> str:
    prompt = (
        "Which one of these categories does the dish belong to? "
        + ", ".join(CATEGORIES)
        + ".  Respond with exactly one category name."
    )
    msgs = [
        SystemMessage(content=prompt),
        HumanMessage(content=dish_name)
    ]
    resp = llm(msgs).content.strip()
    for cat in CATEGORIES:
        if cat.lower() in resp.lower():
            return cat
    return resp
