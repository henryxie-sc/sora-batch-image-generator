import asyncio
import json
import logging
import re
import ssl
from typing import Any, Dict, List

import aiohttp

from .images import image_to_base64


def _setup_ssl_context(allow_insecure_ssl: bool = False):
    try:
        ctx = ssl.create_default_context()
        if allow_insecure_ssl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return ctx
    except Exception as e:
        logging.warning(f"SSL配置失败, 将禁用验证: {e}")
        return False


def _build_content(prompt: str, image_data: List[Dict[str, Any]], app_path) -> List[Dict[str, Any]]:
    content: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]
    for img in image_data or []:
        if img.get("path"):
            base64_url = image_to_base64(app_path / img["path"]) if (app_path / img["path"]).exists() else None
            if base64_url:
                content.append({"type": "image_url", "image_url": {"url": base64_url}})
        elif img.get("url"):
            content.append({"type": "image_url", "image_url": {"url": img["url"]}})
    return content


def _build_payload(model_type: str, content: List[Dict[str, Any]]) -> Dict[str, Any]:
    if model_type == "nano-banana":
        return {
            "model": "gemini-2.5-flash-image-preview",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": content},
            ],
        }
    return {
        "model": "sora_image",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content},
        ],
    }


def _platform_url(platform: str) -> str:
    if platform == "云雾":
        return "https://yunwu.ai/v1/chat/completions"
    if platform == "apicore":
        return "https://api.apicore.ai/v1/chat/completions"
    return "https://vip.apiyi.com/v1/chat/completions"


async def generate_image_async(
    *,
    prompt: str,
    image_data: List[Dict[str, Any]] | None,
    api_platform: str,
    model_type: str,
    api_key: str,
    allow_insecure_ssl: bool,
    retry_count: int,
    app_path,
) -> str:
    """Call remote API to generate image and return an URL or base64 data URL."""
    if not api_key:
        raise ValueError("API密钥不能为空")

    api_url = _platform_url(api_platform)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    content = _build_content(prompt, image_data or [], app_path)
    payload = _build_payload(model_type, content)

    timeout = aiohttp.ClientTimeout(total=600)
    connector = aiohttp.TCPConnector(ssl=_setup_ssl_context(allow_insecure_ssl))

    attempt = 0
    while attempt <= retry_count:
        try:
            # jitter backoff
            if attempt > 0:
                delay = min(8, 0.5 * (2 ** (attempt - 1)))
                await asyncio.sleep(delay)

            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.post(api_url, headers=headers, data=json.dumps(payload)) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        raise ValueError(f"HTTP {resp.status}: {text[:200]}")
                    data = await resp.json()

            # Try to read content field variations
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content")
            )

            if isinstance(content, str):
                if model_type != "nano-banana":
                    m = re.search(r"\[点击下载\]\((.*?)\)", content) or re.search(r"!\[图片\]\((.*?)\)", content)
                    if m:
                        return m.group(1)
                # Some providers may still return base64 in string
                m2 = re.search(r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+", content)
                if m2:
                    return m2.group(0)
                raise ValueError("响应中没有找到图片数据")

            if isinstance(content, list):
                # nano-banana / Gemini-style
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        url = part.get("image_url", {}).get("url")
                        if url:
                            return url
                raise ValueError("响应中没有找到图片数据(list)")

            # Fallback: scan entire JSON for data URL
            text = json.dumps(data, ensure_ascii=False)
            m3 = re.search(r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+", text)
            if m3:
                return m3.group(0)

            raise ValueError("响应格式无法解析")

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            attempt += 1
            if attempt > retry_count:
                raise
            logging.warning(f"请求失败，重试({attempt}/{retry_count}): {e}")

