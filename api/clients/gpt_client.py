import openai
from typing import Dict, List


class ChatGPTClient:
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-4o"):
        openai.api_key = api_key
        openai.base_url = base_url
        self.model = model

    def query(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 150,
    ) -> str:
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if not hasattr(response, "choices") or len(response.choices) == 0:
            raise ValueError("Unexpected response format from API")

        return response.choices[0].message.content


def create_message(role: str, content: str) -> Dict[str, str]:
    return {"role": role, "content": content}
