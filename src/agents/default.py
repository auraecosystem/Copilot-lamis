from src.agents.base import BaseAgent

class DefaultAgent(BaseAgent):
    async def run(self, input_text: str, providers):
        # simple reasoning pipeline
        llm = providers.get("llm")

        if not llm:
            return f"[fallback] {input_text}"

        return await llm.complete(input_text)
