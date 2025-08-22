import json
import re
from typing import Any

def coerce_json(text: str) -> Any:
    """
    Try very hard to parse JSON from LLM output.
    Strips markdown fences, finds first {...} or [...] block if needed.
    Raises ValueError if not parseable.
    """
    if text is None:
        raise ValueError("Empty response")

    # Remove code fences
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)

    # Try direct parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Try to extract the first JSON object/array block
    match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
    if match:
        snippet = match.group(1)
        return json.loads(snippet)

    # Last resort: fix common trailing commas
    cleaned2 = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned2)
