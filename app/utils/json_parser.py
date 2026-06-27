import json
import re


def safe_json_loads(text: str):
    """
    企业级 JSON 解析器：
    解决 LLM 输出：
    - 带解释文字
    - 带 ```json
    - 前后废话
    """

    if not text:
        raise ValueError("Empty response from LLM")

    # 1️去掉 markdown
    text = text.replace("```json", "").replace("```", "")

    # 2提取 JSON（最重要）
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON found in: {text}")

    json_str = match.group()

    # 3️⃣ 转换
    return json.loads(json_str)