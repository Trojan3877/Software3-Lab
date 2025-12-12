from fastapi import FastAPI
from pydantic import BaseModel
from src.llm_agent import run_agent

app = FastAPI(
    title="Software3-Lab AI Control Plane",
    description="LLM-powered Model Control Plane (MCP) for orchestrating ML workflows",
    version="1.0.0"
)

class AgentRequest(BaseModel):
    task: str

@app.post("/agent/run")
def run_mcp_agent(request: AgentRequest):
    """
    Executes the LLM-powered MCP agent.
    """
    result = run_agent(custom_task=request.task)
    return {
        "status": "success",
        "agent_output": result
    }