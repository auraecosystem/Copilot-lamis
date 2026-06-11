# script.py - Copilot-Lamis utility runner

import asyncio
from src.agents.registry import AgentRegistry
from src.providers.router import ProviderRouter

agents = AgentRegistry()
providers = ProviderRouter()

async def run():
    print("Copilot-Lamis Script Runner Started")

    while True:
        user_input = input("\n>> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        agent = agents.get("default")
        result = await agent.run(user_input, providers)

        print(f"\nAI: {result}")

if __name__ == "__main__":
    asyncio.run(run())
