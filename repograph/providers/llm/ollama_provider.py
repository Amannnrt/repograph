import ollama
from repograph.providers.llm.base import (
    LLMProvider,
)

class OllamaLLMProvider(LLMProvider):

    def __init__(self,model: str = "qwen2.5:1.5b",):
        self.model = model

    def generate(self,prompt: str, ) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]
