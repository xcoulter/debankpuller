import requests
import time
import json
import os
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_DURATION = 3600  # 1 hour

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def fetch_debank_balances(wallet):
    cache = load_cache()
    now = time.time()
    if wallet in cache and now - cache[wallet]['timestamp'] < CACHE_DURATION:
        return cache[wallet]['data']

    url = f"https://openapi.debank.com/v1/user/total_balance?id={wallet}"
    headers = {"AccessKey": st.secrets["debank"]["api_key"]}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None

    data = resp.json()
    result = []
    for chain in data.get("portfolio_item_list", []):
        for token in chain.get("list", []):
            result.append({
                "token": token["name"],
                "balance": token["amount"],
                "usd_value": token["price"] * token["amount"],
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            })

    cache[wallet] = {"timestamp": now, "data": result}
    save_cache(cache)
    return result

