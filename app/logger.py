import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/run.jsonl")
LOG_FILE.parent.mkdir(exist_ok=True)


def log_interaction(
    question,
    response,
    tool_used=False,
    tool_output=None,
):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": question,
        "tool_used": tool_used,
        "tool_output": tool_output,
        "response": response,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")