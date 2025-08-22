import os
from typing import Any, List
import google.generativeai as genai
import json


class GeminiConfig:
    def __init__(self, model: str = "gemini-1.5-pro"):
        self.model = model


class TaskAgentGemini:
    def __init__(self, config: GeminiConfig):
        # Configure API key (make sure GOOGLE_API_KEY is set in your env)
        api_key = os.getenv('GOOGLE_API_KEY',"AIzaSyBVX4_GBArfNSYR9NJxyxJE6mM8jNTb2GQ")
        if not api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable")
        genai.configure(api_key=api_key)

        # Create model instance
        self.model = genai.GenerativeModel(config.model)

    def _call(self, prompt: str) -> str:
        """Send prompt to Gemini and return raw text"""
        resp = self.model.generate_content(prompt)
        return resp.text.strip()

    def categorize(self, tasks: List[str], system_prompt: str, user_prompt: str) -> Any:
        prompt = system_prompt + "\n" + user_prompt
        content = self._call(prompt)
        return self._coerce_json(content)

    def prioritize(self, tasks: List[str], system_prompt: str, user_prompt: str) -> Any:
        prompt = system_prompt + "\n" + user_prompt
        content = self._call(prompt)
        return self._coerce_json(content)

    def schedule(self, prioritized_json: str, system_prompt: str, user_prompt: str) -> Any:
        prompt = system_prompt + "\n" + user_prompt
        content = self._call(prompt)
        return self._coerce_json(content)

    @staticmethod
    def _coerce_json(content: str) -> Any:
        """Try to parse Gemini output into JSON"""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to clean up common issues (e.g., trailing commas, ```json fences)
            cleaned = (
                content.strip()
                .replace("```json", "")
                .replace("```", "")
            )
            try:
                return json.loads(cleaned)
            except Exception:
                return {"raw": content}
