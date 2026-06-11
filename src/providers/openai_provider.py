import os

class OpenAIProvider:
    async def complete(self, prompt: str):
        # lightweight mock (replace with real OpenAI / local model later)
        return f"[AI RESPONSE] {prompt[::-1]}"
