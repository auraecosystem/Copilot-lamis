class BaseAgent:
    async def run(self, input_text: str, providers):
        raise NotImplementedError
