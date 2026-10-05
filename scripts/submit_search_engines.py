#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request
import urllib.error

BING_API_KEY = os.environ.get("BING_API_KEY", "").strip()
INDEXNOW_KEY = "6c9119e1be3a49e2851073f16d11fee7"  # Public verification key; served at /<key>.txt.
HOST = "saramjh.github.io"
BASE_URL = f"https://{HOST}"

def get_urls():
    sitemap_path = os.path.join(os.path.dirname(__file__), "..", "_site", "sitemap.xml")
    urls = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
        urls = re.findall(r"<loc>(https://[^<]+)</loc>", content)
    else:
        try:
            req = urllib.request.Request(f"{BASE_URL}/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as res:
                content = res.read().decode("utf-8")
                urls = re.findall(r"<loc>(https://[^<]+)</loc>", content)
        except Exception as e:
            print(f"[URLs] Warning: Failed to fetch live sitemap: {e}")
    
    if not urls:
        # Fallback to key landing pages and latest posts
        urls = [
            f"{BASE_URL}/",
            f"{BASE_URL}/naver-map-save-list-bulk-reorganize-guide/",
            f"{BASE_URL}/youtube-restaurant-list-naver-map-save-guide/",
            f"{BASE_URL}/kakaotalk-shorts-autoplay-adblock-guide/",
            f"{BASE_URL}/kr-macbook-external-monitor-flickering-solution/",
            f"{BASE_URL}/epson-waste-ink-pad-reset-without-key/",
            f"{BASE_URL}/rich-tester/",
            f"{BASE_URL}/scratchLottery/"
        ]
    # Unique and remove anchors or unwanted assets
    cleaned = []
    seen = set()
    for u in urls:
        u = u.strip()
        if u not in seen and not u.endswith((".png", ".jpg", ".jpeg", ".css", ".js", ".txt")):
            seen.add(u)
            cleaned.append(u)
    return cleaned

def submit_bing_api(urls):
    if not BING_API_KEY:
        print("[Bing API] No BING_API_KEY configured. Skipping.")
        return
    api_url = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={BING_API_KEY}"
    # Bing allows max 500 URLs per batch
    batch = urls[:100]
    payload = {
        "siteUrl": BASE_URL,
        "urlList": batch
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            res_body = res.read().decode("utf-8")
            print(f"[Bing API] Submitted {len(batch)} URLs successfully: {res_body}")
    except urllib.error.HTTPError as e:
        print(f"[Bing API] HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[Bing API] Error: {e}")

def submit_indexnow(urls):
    key = INDEXNOW_KEY
    batch = urls[:100]
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": batch
    }
    data = json.dumps(payload).encode("utf-8")
    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow"
    ]
    for ep in endpoints:
        req = urllib.request.Request(ep, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                print(f"[IndexNow] ({ep}) Response {res.status}: Success")
        except urllib.error.HTTPError as e:
            print(f"[IndexNow] ({ep}) HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"[IndexNow] ({ep}) Error: {e}")

if __name__ == "__main__":
    url_list = get_urls()
    print(f"Total discovered URLs: {len(url_list)}")
    submit_bing_api(url_list)
    submit_indexnow(url_list)
