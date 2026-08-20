#!/usr/bin/env python3
"""FoxData Open API 客户端（官方文档：https://docs.foxdata.com/）

Base URL:  https://api.foxdata.com/apiv1/open-api
鉴权:      Header `x-openapi-key: <YOUR_LICENSE>`（FoxData 个人中心/销售获取）
分页:      响应 data.next → GET /common/next-page?taskId=&pageKey=
错误码:    401 缺key / 403 key无效 / 429 限流 / 60003 日配额 / 60005 积分不足 / 60008 无数据
"""
import json
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CREDS_FILE = BASE_DIR / "config" / "foxdata_creds.json"
BASE_URL = "https://api.foxdata.com/apiv1/open-api"


def load_key():
    if not CREDS_FILE.exists():
        return None
    data = json.loads(CREDS_FILE.read_text())
    return data.get("x_openapi_key") or data.get("license")


def verify():
    key = load_key()
    if not key:
        print("FoxData API 未配置（config/foxdata_creds.json 的 x_openapi_key），将使用 foxdata-aichat MCP 数据通道")
        return False
    print(f"FoxData API key 已配置（{key[:8]}...），可用官方数据通道")
    return True


def call_api(endpoint, body=None, method="POST", retries=2):
    key = load_key()
    if not key:
        raise RuntimeError("未配置 FoxData API key（config/foxdata_creds.json）")
    url = f"{BASE_URL}{endpoint}"
    headers = {"x-openapi-key": key, "Content-Type": "application/json"}
    for attempt in range(retries + 1):
        if method == "POST":
            r = requests.post(url, json=body or {}, headers=headers, timeout=30)
        else:
            r = requests.get(url, params=body or {}, headers=headers, timeout=30)
        if r.status_code == 429:
            time.sleep(2 * (attempt + 1))
            continue
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        data = r.json()
        code = data.get("code")
        if code == 200:
            return data.get("data", {})
        if code in (429, 60004):
            time.sleep(2 * (attempt + 1))
            continue
        raise RuntimeError(f"FoxData API 业务错误 code={code} msg={data.get('msg')}")
    raise RuntimeError("FoxData API 重试后仍失败（限流）")


def fetch_pages(endpoint, body=None, max_pages=3):
    first = call_api(endpoint, body)
    result = {"result": list(first.get("result") or []), **first}
    pages = 0
    while pages < max_pages:
        nxt = first.get("next")
        if not nxt:
            break
        page = call_api(
            "/common/next-page",
            {"taskId": nxt.get("taskId"), "pageKey": nxt.get("pageKey")},
            method="GET",
        )
        result["result"] += list(page.get("result") or [])
        first = page
        pages += 1
    return result


def app_info(app_id, region, language=None):
    body = {"appId": app_id, "region": region}
    if language:
        body["language"] = language
    return call_api("/app/app-info", body)


if __name__ == "__main__":
    verify()
