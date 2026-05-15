from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from agent import run_agent
from schemas import AgentResponse

app = FastAPI()

class Request(BaseModel):
    message: str

@app.post("/generate", response_model=AgentResponse)
async def generate(req: Request):
    result = await run_agent(req.message)
    return result

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True, 
        host="localhost",
        port=8000
    )