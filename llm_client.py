import os
import requests
from abc import ABC, abstractmethod

# ---------- Base Interface ----------

class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, messages):
        pass

# ---------- OpenAI ----------

class OpenAILLMClient(BaseLLMClient):
    def __init__(self, model="gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def chat(self, messages):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content

# ---------- DeepSeek (OpenAI-compatible) ----------

class DeepSeekLLMClient(BaseLLMClient):
    def __init__(self, model="deepseek-chat"):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
        self.model = model

    def chat(self, messages):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content

# ---------- Ollama (Local) ----------

class OllamaLLMClient(BaseLLMClient):
    def __init__(self, model="llama3"):
        self.model = model

    def chat(self, messages):
        prompt = "\n".join(m["content"] for m in messages)

        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        return resp.json()["response"]

# ---------- Hugging Face ----------

class HuggingFaceLLMClient(BaseLLMClient):
    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.2"):
        self.model = model
        self.api_token = os.getenv("HF_TOKEN")

    def chat(self, messages):
        prompt = "\n".join(m["content"] for m in messages)

        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model}",
            headers=headers,
            json={"inputs": prompt}
        )

        return resp.json()[0]["generated_text"]


# ---------- Fallback Wrapper ----------

class FallbackLLMClient(BaseLLMClient):
    def __init__(self, clients):
        self.clients = clients

    def chat(self, messages):
        last_error = None

        for client in self.clients:
            try:
                return client.chat(messages)
            except Exception as e:
                print(f"[WARN] LLM failed ({client.__class__.__name__}): {e}")
                last_error = e

        raise RuntimeError("All LLM backends failed") from last_error

# ---------- Factory ----------

def create_llm_client(name: str) -> BaseLLMClient:
    name = name.lower()

    if name == "openai":
        return OpenAILLMClient()
    elif name == "deepseek":
        return DeepSeekLLMClient()
    elif name == "ollama":
        return OllamaLLMClient()
    elif name in ("hf", "huggingface"):
        return HuggingFaceLLMClient()
    else:
        raise ValueError(f"Unknown LLM backend: {name}")
