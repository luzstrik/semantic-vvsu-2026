import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from langchain_mcp_adapters.client import MultiServerMCPClient

from schemas import AgentResponse
from skill import load_skills

load_dotenv()


SYSTEM_PROMPT = """
Ты — fitness AI agent.

Ты работаешь только с:
1. КБЖУ
2. Программами тренировок

Ты ОБЯЗАН использовать MCP tools.

Никогда не придумывай расчеты вручную.

Верни ответ строго по schema.

Дополнительные skills:
{skills}
"""


async def create_agent(user_input: str):

    skills_prompt = load_skills(user_input)

    api_key = os.getenv("GROQ_API_KEY")

    client = MultiServerMCPClient(
        {
            "fitness": {
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools)

    structured_llm = llm_with_tools.with_structured_output(
        AgentResponse
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            "{input}",
        ),
    ])

    partial_prompt = prompt.partial(
        skills=skills_prompt,
    )

    chain = (
        partial_prompt
        | structured_llm
    )

    return chain


async def run_agent(user_input: str):

    agent = await create_agent(user_input)

    result = await agent.ainvoke({
        "input": user_input
    })

    return result