from fastapi import FastAPI, WebSocket
from src.agents.registry import AgentRegistry
from src.providers.router import ProviderRouter

app = FastAPI(title="Copilot-Lamis AI Runtime")

agents = AgentRegistry()
providers = ProviderRouter()

@app.get("/")
def home():
    return {"status": "Copilot-Lamis running", "mode": "AI Runtime"}

@app.post("/agent/run")
async def run_agent(payload: dict):
    agent = agents.get(payload.get("agent", "default"))
    result = await agent.run(payload.get("input", ""), providers)
    return {"result": result}

@app.websocket("/ws")
async def websocket_ai(ws: WebSocket):
    await ws.accept()

    while True:
        msg = await ws.receive_text()
        agent = agents.get("default")

        response = await agent.run(msg, providers)
        await ws.send_text(response)
