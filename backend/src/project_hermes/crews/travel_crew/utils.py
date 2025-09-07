import json
from pathlib import Path
from typing import Dict, Any

PROMPT_LIBRARY_PATH = Path(__file__).parent / "prompt_library.json"


class PromptLibrary:
    def __init__(self):
        with open(PROMPT_LIBRARY_PATH, "r", encoding="utf-8") as f:
            self.prompts = json.load(f)

    def get_prompt(self, key: str) -> Dict[str, Any]:
        return self.prompts[key]

    def get_prompt_text(self, key: str) -> str:
        return self.prompts[key]["prompt"]


def get_prompt_library():
    return PromptLibrary()
