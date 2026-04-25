from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent

app = FastAPI()
agent = create_agent()

class Request(BaseModel):
    message: str

class Response(BaseModel):
    answer: str

@app.post("/generate", response_model=Response)
def generate(req: Request):
    result = agent.invoke({"input": req.message})

    return {"answer": result["output"]}
