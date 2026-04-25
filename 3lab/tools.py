from langchain.tools import tool
from duckduckgo_search import DDGS
import requests

# Калькулятор КБЖУ
@tool
def calorie_calculator(weight: float, height: float, age: int, goal: str) -> str:
    """
    Рассчитывает КБЖУ.
    goal: loss / maintain / gain
    """
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    
    if goal == "loss":
        calories = bmr * 0.8
    elif goal == "gain":
        calories = bmr * 1.2
    else:
        calories = bmr

    protein = weight * 2
    fat = weight * 1
    carbs = (calories - (protein*4 + fat*9)) / 4

    return f"Калории: {calories:.0f}, Б: {protein:.0f}, Ж: {fat:.0f}, У: {carbs:.0f}"

# ищем программы тренировок через duckduck
@tool
def search_workout(query: str) -> str:
    """
    Ищет программы тренировок в интернете
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        
        output = []
        for r in results:
            output.append(r["title"] + " - " + r["body"])
        
        return "\n".join(output)