import re
import requests
from pydantic import BaseModel, Field
from openai import AsyncOpenAI


class InferenceSettings(BaseModel):
    inf_url: str
    api_key: str | None = Field(default="EMPTY")
    health: str | None = Field(default="/health")


class InferenceEngine:
    def __init__(self, hf_slug: str, settings: InferenceSettings) -> None:
        self.hf_slug = hf_slug
        self.inf_url = settings.inf_url

        if settings.health:
            self.health = settings.health

        self.client = AsyncOpenAI(
            base_url=settings.inf_url,
            api_key=settings.api_key,
        )

    async def health_check(self) -> bool | None:
        if not self.health:
            return None
        
        pattern = r"(http://[^/]*).*"
        stripped_url = re.sub(pattern, r"\1", self.inf_url)

        try: 
            response = requests.get(f"{stripped_url}{self.health}")
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            return False
        
    async def generate(self, 
                       prompt: str):

        response_dict = {
            "model": self.hf_slug,
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 1.0,
        }
        print(self.inf_url)
        response = await self.client.completions.create(**response_dict) # library call
        return self._extract_text(response)

    def _extract_text(self, response):
        if(hasattr(response, "choices") and 
           response.choices != None and 
           len(response.choices) > 0):
            choice = response.choices[0]

            if(hasattr(choice, "text") and 
               choice.text != None):
                return choice.text
