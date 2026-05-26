import httpx
import os
import time


API_KEY = os.environ.get("BLTCY_API_KEY", "")
BASE_URL = "https://api.bltcy.ai/v1"
MODEL = "claude-haiku-4-5"


def summarize_batch(items: list[dict]) -> list[dict]:
    """批量为每条内容生成中文摘要"""
    if not API_KEY:
        print("[摘要] 未设置 BLTCY_API_KEY，跳过摘要生成")
        for item in items:
            item["summary"] = item.get("title", "")
        return items

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    for i, item in enumerate(items):
        raw = item.get("raw", item.get("title", ""))[:500]
        source = item.get("source", "")
        prompt = f"""请用中文为以下内容写一句话摘要（不超过80字），直接输出摘要内容，不要加任何前缀：

来源：{source}
内容：{raw}"""

        try:
            resp = httpx.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                    "temperature": 0.3,
                },
                timeout=30,
            )
            resp.raise_for_status()
            summary = resp.json()["choices"][0]["message"]["content"].strip()
            item["summary"] = summary
            print(f"  [{i+1}/{len(items)}] {item['title'][:30]}... → 摘要完成")
        except Exception as e:
            print(f"  [{i+1}/{len(items)}] 摘要失败: {e}")
            item["summary"] = item.get("title", "")

        if i < len(items) - 1:
            time.sleep(0.5)

    return items
