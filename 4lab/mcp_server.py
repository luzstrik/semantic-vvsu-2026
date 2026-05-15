from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

mcp = FastMCP("fitness-tools")

@mcp.tool()
def calculate_macros(
    body_weight: float,
    body_height: float,
    years_old: int,
    target: str,
):
    """ Расчет КБЖУ. target: - cut - maintain - bulk """

    metabolic_rate = (
        10 * body_weight
        + 6.25 * body_height
        - 5 * years_old
        + 5
    )

    activity_multiplier = {
        "cut": 0.85,
        "maintain": 1.0,
        "bulk": 1.15,
    }

    final_calories = metabolic_rate * activity_multiplier.get(target, 1.0)

    protein_amount = body_weight * 1.8
    fat_amount = body_weight * 0.9

    remaining_calories = (
        final_calories
        - (protein_amount * 4)
        - (fat_amount * 9)
    )

    carb_amount = remaining_calories / 4

    return {
        "calories": int(final_calories),
        "protein": int(protein_amount),
        "fat": int(fat_amount),
        "carbs": int(carb_amount),
    }

@mcp.tool()
def search_workout(query: str):
    """
    Поиск тренировочных программ.
    """

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

        output = []

        for r in results:
            output.append({
                "title": r["title"],
                "body": r["body"]
            })

        return output
    
if __name__ == "__main__":
    mcp.run("stdio")