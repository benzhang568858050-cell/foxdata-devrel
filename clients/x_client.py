#!/usr/bin/env python3
"""X (Twitter) 客户端 —— 基于 twikit（cookies 网页端方案，免费，无官方 API 费用）。

凭据：config/x_cookies.json（Cookie-Editor 导出）或 config/x_creds.json（账号密码登录）
发布：发帖 + 图文（最多 4 图），自动检查 280 权重限制（中文×2 其他×1，安全线 270）
"""
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


def text_weight(text):
    """X 权重：中文字符×2，其他×1"""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in text)


def load_cookies():
    if COOKIES_FILE.exists():
        return json.loads(COOKIES_FILE.read_text())
    return None


def get_client():
    from twikit import Client

    client = Client(language="en-US")

    cookies = load_cookies()
    if cookies:
        client.set_cookies(cookies)
    else:
        creds = json.loads(CREDS_FILE.read_text()) if CREDS_FILE.exists() else None
        if not creds:
            raise RuntimeError(
                "未配置 X 凭据：请把 Cookie-Editor 导出的 cookies 写入 config/x_cookies.json，"
                "或填写 config/x_creds.json（auth_info_1/password/totp_secret）"
            )
        client.login(
            auth_info_1=creds.get("auth_info_1", ""),
            auth_info_2=creds.get("auth_info_2"),
            password=creds.get("password", ""),
            totp_secret=creds.get("totp_secret"),
        )
        client.save_cookies(str(COOKIES_FILE))
    return client


def verify():
    """校验登录态并输出当前用户。"""
    client = get_client()
    me = client.user_id  # 触发登录态校验
    print(f"X 登录 OK：user_id={me}")
    return str(me)


def post_tweet(text, image_paths=None):
    """发布一条帖子（支持最多 4 张配图）。返回 {tweet_id, url}。"""
    client = get_client()
    text = text.strip()
    if not text:
        raise ValueError("文案为空")
    w = text_weight(text)
    if w > MAX_WEIGHT:
        raise ValueError(f"X 权重超限：{w} > {MAX_WEIGHT}（中文×2，建议压缩）")

    media_ids = []
    if image_paths:
        for p in image_paths[:4]:
            mid = client.upload_media(source=str(p), wait_for_completion=True)
            media_ids.append(mid)

    tweet = client.create_tweet(text=text, media_ids=media_ids or None)
    tid = str(tweet.id)
    return {"tweet_id": tid, "url": f"https://x.com/i/status/{tid}"}


if __name__ == "__main__":
    verify()
