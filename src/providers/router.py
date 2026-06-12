from src.providers.openai_provider import OpenAIProvider

class ProviderRouter:
    def __init__(self):
        self.providers = {
            "llm": OpenAIProvider()
        }

    def get(self, name: str):
        return self.providers.get(name)
