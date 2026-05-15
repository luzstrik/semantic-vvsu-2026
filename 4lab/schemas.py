from pydantic import BaseModel
from typing import Optional, List

class MacroResponse(BaseModel):
    calories: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None
    carbs: Optional[int] = None

class WorkoutDay(BaseModel):
    day: str
    exercises: List[str]

class AgentResponse(BaseModel):
    type: str
    answer: str

    macros: Optional[MacroResponse] = None
    workout: Optional[List[WorkoutDay]] = None