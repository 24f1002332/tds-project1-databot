import json
import re

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY
from app.prompts import SYSTEM_PROMPT
from tools import run_python

client = genai.Client(api_key=GEMINI_API_KEY)


def extract_json(text: str):
    """
    Extract the first JSON object from model output.
    """

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")

    if start == -1:
        return {"answer": text}

    depth = 0

    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1

            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except Exception:
                    break

    return {"answer": text}


def ask_gemini(messages, log_url):
    """
    messages:
        [
            {"role":"user","content":"..."},
            {"role":"model","content":"..."},
            ...
        ]
    """

    history = []

    history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=SYSTEM_PROMPT)],
        )
    )

    for m in messages:
        role = "user" if m["role"] == "user" else "model"

        history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=m["content"])],
            )
        )

    tools = [run_python]

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=history,
        config=types.GenerateContentConfig(
            tools=tools,
            temperature=0,
        ),
    )

    text = response.text.strip()

    data = extract_json(text)

    if not isinstance(data, dict):
        data = {"answer": data}

    if "answer" not in data:
        data = {"answer": data}

    data["log_url"] = log_url

    return data