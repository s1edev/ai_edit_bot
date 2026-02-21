"""Image and AI service functions."""

import aiohttp
import asyncio
import base64
import logging
import ssl
from typing import Optional

logger = logging.getLogger(__name__)


def create_ssl_context() -> ssl.SSLContext:
    """Create SSL context that trusts system CA certificates."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context


async def upload_image_to_imgbb(file_id: str, bot_token: str, imgbb_api_key: str, timeout: int = 30) -> Optional[dict]:
    timeout_config = aiohttp.ClientTimeout(total=timeout, connect=10)
    connector = aiohttp.TCPConnector(ssl=create_ssl_context())

    async with aiohttp.ClientSession(connector=connector, timeout=timeout_config, trust_env=True) as session:
        # Get file path
        file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        resp = await session.get(file_info_url)
        if resp.status != 200:
            return None
        data = await resp.json()
        if not data.get("ok"):
            return None
        file_path = data["result"]["file_path"]

        # Download file
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        resp = await session.get(file_url)
        if resp.status != 200:
            return None
        file_bytes = await resp.read()

        # Upload to ImgBB
        payload = {"key": imgbb_api_key, "image": base64.b64encode(file_bytes).decode()}
        resp = await session.post("https://api.imgbb.com/1/upload", data=payload)
        if resp.status != 200:
            return None
        result = await resp.json()
        if not result.get("success"):
            return None
        return {"url": result["data"]["url"], "delete_url": result["data"].get("delete_url")}


async def edit_image_nano_banana(api_key: str, image_url: str, prompt: str, size: str = "auto", poll_interval: float = 1.5, max_attempts: int = 40) -> Optional[str]:
    connector = aiohttp.TCPConnector(ssl=create_ssl_context())
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        # Start generation
        resp = await session.post(
            "https://api.polza.ai/api/v1/images/generations",
            headers=headers,
            json={"model": "nano-banana", "filesUrl": [image_url], "prompt": prompt, "size": size}
        )
        if resp.status not in (200, 201):
            return None
        request_id = (await resp.json()).get("requestId")
        if not request_id:
            return None

        # Poll for result
        for _ in range(max_attempts):
            resp = await session.get(f"https://api.polza.ai/api/v1/images/{request_id}", headers={"Authorization": f"Bearer {api_key}"})
            if resp.status != 200:
                return None
            data = await resp.json()
            if data.get("status") == "COMPLETED":
                return data.get("url")
            if data.get("status") == "FAILED":
                return None
            await asyncio.sleep(poll_interval)
        return None


async def delete_image_from_imgbb(delete_url: str, timeout: int = 30) -> bool:
    timeout_config = aiohttp.ClientTimeout(total=timeout, connect=10)
    connector = aiohttp.TCPConnector(ssl=create_ssl_context())
    async with aiohttp.ClientSession(connector=connector, timeout=timeout_config, trust_env=True) as session:
        resp = await session.get(delete_url)
        return resp.status == 200


async def process_image_with_ai(image_url: str, user_prompt: str, polza_api_key: str) -> Optional[str]:
    return await edit_image_nano_banana(api_key=polza_api_key, image_url=image_url, prompt=user_prompt, max_attempts=100)
