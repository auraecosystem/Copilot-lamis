from fastapi import FastAPI
from src.core.autonomous_engine import AutonomousEngine
from src.agents.planner import PlannerAgent
from src.agents.critic import CriticAgent
from src.memory.system import MemorySystem
from src.tools.runner import ToolRunner

app = FastAPI(title="Copilot-Lamis Autonomous OS")

memory = MemorySystem()

engine = AutonomousEngine(
    planner=PlannerAgent(),
    executor=None,  # injected below
    critic=CriticAgent(),
    memory=memory
)

executor = ToolRunner()
engine.executor = executor

@app.post("/goal/run")
async def run_goal(payload: dict):
    goal = payload["goal"]
    return await engine.run_goal(goal, providers={
        "llm": None,
        "tools": executor
    })
