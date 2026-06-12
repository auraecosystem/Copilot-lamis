from src.agents.base import BaseAgent
from src.agents.default import DefaultAgent

class AgentRegistry:
    def __init__(self):
        self.agents = {
            "default": DefaultAgent()
        }

    def get(self, name: str) -> BaseAgent:
        return self.agents.get(name, self.agents["default"])
