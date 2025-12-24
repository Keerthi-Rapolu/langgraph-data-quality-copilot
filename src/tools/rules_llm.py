from __future__ import annotations

import json
from langchain_ollama import ChatOllama

def generate_rules_from_profile(profile: dict, model: str = "qwen2.5:7b") -> list[dict]:
    """
    Uses LLM to generate data quality rules from profiling output.
    """
    llm = ChatOllama(
        model=model,
        base_url="http://localhost:11434",
        temperature=0
    )

    prompt = f"""
You are a data quality expert.

Given this table profile, generate data quality rules.
Return rules as JSON list with fields:
- name
- type (not_null, unique, range, allowed_values)
- column
- min (optional)
- max (optional)
- allowed (optional)

Profile:
{json.dumps(profile, indent=2, default=str)}
"""

    response = llm.invoke(prompt)

    # Ollama returns text; expect JSON
    try:
        return json.loads(response.content)
    except Exception:
        return []
