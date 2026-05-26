import httpx
import os
import time


API_KEY = os.environ.get("BLTCY_API_KEY", "")
BASE_URL = "https://api.bltcy.ai/v1"
MODEL = "claude-haiku-4-5"
MAX_RETRIES = 3


def _call_api(headers: dict, prompt: str) -> str:
    for attempt in range(MAX_RETRIES):
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
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt
                print(f"    重试 {attempt+1}/{MAX_RETRIES-1}，等待 {wait}s... ({e})")
                time.sleep(wait)
            else:
                raise


def summarize_batch(items: list[dict]) -> list[dict]:
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
        title = item.get("title", "")
        prompt = f"请用中文写一句话摘要（不超过80字），直接输出摘要，不加任何前缀：\n\n来源：{source}\n标题：{title}\n内容：{raw}"

        try:
            summary = _call_api(headers, prompt)
            item["summary"] = summary
            print(f"  [{i+1}/{len(items)}] {title[:25]}... ✓")
        except Exception as e:
            print(f"  [{i+1}/{len(items)}] 摘要失败: {e}")
            item["summary"] = title  # 降级用标题

        if i < len(items) - 1:
            time.sleep(0.3)

    return items
