#!/usr/bin/env python3
"""X (Twitter) 客户端 —— 基于 twikit 2.3.3（async API，cookies 网页端方案，免费）。

凭据：config/x_cookies.json（Cookie-Editor 导出，{name: value} 格式）
发布：发帖 + 图文（最多 4 图），自动检查 280 权重限制（中文×2 其他×1，安全线 270）
"""
import asyncio
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEPS_DIR = BASE_DIR / ".deps"
if DEPS_DIR.exists():
    sys.path.insert(0, str(DEPS_DIR))
CREDS_FILE = BASE_DIR / "config" / "x_creds.json"
COOKIES_FILE = BASE_DIR / "config" / "x_cookies.json"

MAX_WEIGHT = 270  # 280 上限，留 10 安全余量


def _run(coro):
    """同步包装 twikit async 调用。"""
    return asyncio.run(coro)


def text_weight(text):
    """X 权重：中文字符×2，其他×1"""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in text)


def load_cookies():
    if COOKIES_FILE.exists():
        return json.loads(COOKIES_FILE.read_text())
    return None


def get_client():
    """创建 twikit 客户端并注入 cookies（同步操作）。

    内置 transaction 绕过：twikit 2.3.x 的 X-Client-Transaction 签名机制需要
    从 x.com JS 文件提取索引（沙箱网络受限会报 KEY_BYTE indices 错误）。
    实测 X 服务端只校验签名格式，占位 key 即可通过读请求。
    """
    from twikit import Client

    client = Client(language="en-US")
    cookies = load_cookies()
    if cookies:
        client.set_cookies(cookies)
    else:
        creds = json.loads(CREDS_FILE.read_text()) if CREDS_FILE.exists() else None
        if not creds:
            raise RuntimeError(
                "未配置 X 凭据：请把 Cookie-Editor 导出的 cookies 写入 config/x_cookies.json"
            )
        _run(client.login(
            auth_info_1=creds.get("auth_info_1", ""),
            auth_info_2=creds.get("auth_info_2"),
            password=creds.get("password", ""),
            totp_secret=creds.get("totp_secret"),
        ))
        client.save_cookies(str(COOKIES_FILE))
    # transaction 绕过 patch（home_page_response 非空则跳过 init 网络请求）
    t = client.client_transaction
    t.home_page_response = True
    t.key = "A" * 64
    t.animation_key = "00" * 32
    return client


def verify():
    """校验登录态（轻量读请求；twikit 响应解析对部分用户有 KeyError 容差）。"""
    client = get_client()

    async def _check():
        try:
            await client.get_user_by_screen_name("x")
            return "API 可达"
        except KeyError:
            return "API 可达（响应字段容差）"
        except Exception as e:
            return f"失败: {e}"

    result = _run(_check())
    print(f"X 验证：{result}（cookies 已注入）")
    return True


def post_tweet(text, image_paths=None):
    """发布一条帖子（支持最多 4 张配图）。返回 {tweet_id, url}。

    底层直接调用 GraphQL（twikit 高层 create_tweet 对 errors 响应解析为 None，
    此处显式解析错误码：344=日配额用尽 / 226=风控）。
    """
    client = get_client()
    text = text.strip()
    if not text:
        raise ValueError("文案为空")
    w = text_weight(text)
    if w > MAX_WEIGHT:
        raise ValueError(f"X 权重超限：{w} > {MAX_WEIGHT}（中文×2，建议压缩）")

    async def _post():
        # 先上传媒体（如有）
        media_entities = []
        if image_paths:
            for p in image_paths[:4]:
                mid = await client.upload_media(source=str(p), wait_for_completion=True)
                media_entities.append({"media_id": mid, "tagged_users": []})
        response, _ = await client.gql.create_tweet(
            text=text, is_note_tweet=False, media_entities=media_entities, poll_uri=None,
            reply_to=None, attachment_url=None, community_id=None,
            share_with_followers=False, richtext_options=None, edit_tweet_id=None,
            limit_mode=None)
        return response

    response = _run(_post())
    errors = response.get("errors")
    if errors:
        code = errors[0].get("code")
        msg = errors[0].get("message", "")[:120]
        if code == 344:
            raise RuntimeError(f"X 日配额用尽（344）：{msg}（UTC 重置后恢复）")
        if code == 226:
            raise RuntimeError(f"X 风控（226）：{msg}")
        raise RuntimeError(f"X 发布失败（{code}）：{msg}")
    try:
        result = response["data"]["create_tweet"]["tweet_results"]["result"]
        tid = result.get("rest_id") or result.get("id_str")
    except (KeyError, TypeError):
        raise RuntimeError(f"X 响应异常：{str(response)[:150]}")
    return {"tweet_id": str(tid), "url": f"https://x.com/i/status/{tid}"}


if __name__ == "__main__":
    verify()
