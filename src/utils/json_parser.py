import json
import re


def extract_json(text: str):
    """
    从大模型返回结果中提取 JSON
    """

    text = text.strip()

    # ```json ... ```
    match = re.search(r"```json\s*(.*?)\s*```", text, re.S)

    if match:
        text = match.group(1)

    return json.loads(text)