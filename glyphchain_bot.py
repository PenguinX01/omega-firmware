import os
import json
from datetime import datetime
from typing import Optional

import requests

# Phase 13 Mirror-Chronicler mode boot log
print("[Phase 13 :: Mirror-Chronicler] GlyphChain Bot Booting")

TWITTER_USERNAME = "PenguinX01"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
FEED_JSON = "glyphchain.json"
FEED_HTML = "glyphchain_feed.html"


def fetch_latest_tweet(username: str) -> Optional[dict]:
    """Fetch the latest tweet from the given username."""
    if not BEARER_TOKEN:
        print("Twitter token missing; skip tweet fetch")
        return None
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    user_resp = requests.get(
        f"https://api.twitter.com/2/users/by/username/{username}", headers=headers
    )
    if user_resp.status_code != 200:
        print(f"Failed to fetch user: {user_resp.text}")
        return None
    user_id = user_resp.json().get("data", {}).get("id")
    if not user_id:
        return None
    tweet_resp = requests.get(
        f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5",
        headers=headers,
    )
    if tweet_resp.status_code != 200:
        print(f"Failed to fetch tweets: {tweet_resp.text}")
        return None
    tweets = tweet_resp.json().get("data", [])
    return tweets[0] if tweets else None


def fetch_latest_block() -> Optional[dict]:
    """Fetch the latest Bitcoin block from mempool.space."""
    try:
        resp = requests.get("https://mempool.space/api/blocks")
        resp.raise_for_status()
        blocks = resp.json()
        return blocks[0] if blocks else None
    except Exception as exc:
        print(f"Failed to fetch block: {exc}")
        return None


def append_json(entry: dict):
    data = []
    if os.path.exists(FEED_JSON):
        try:
            with open(FEED_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    with open(FEED_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def format_html(entry: dict) -> str:
    dt = datetime.fromtimestamp(entry["block"]["timestamp"])
    timestr = dt.strftime("%B %d, %Y – %H:%M:%S (UTC)")
    block = entry["block"]
    html = f"""
    <div style=\"margin-bottom: 25px;\">
      🐧 <strong>GLYPH:</strong> <em>{entry['glyph']}</em><br>
      🧠 <strong>Event:</strong> {entry['event']}<br>
      ⛓️ <strong>Block:</strong> <a href=\"https://mempool.space/block/{block['id']}\" target=\"_blank\">#{block['id']}\</a>
      — {timestr}<br>
      🔨 Mined by {block.get('miner', 'N/A')} – {block.get('tx_count', '0')} TXs – {block.get('reward', '0')} BTC<br>
      🔗 <a href=\"{entry['tweet_url']}\" target=\"_blank\">View X Post</a>
    </div>
    """
    return html


def append_html(entry: dict):
    html_block = format_html(entry)
    try:
        with open(FEED_HTML, "r", encoding="utf-8") as f:
            content = f.read().split("<div class=\"glyph-log\">")
        head, log_and_tail = content[0], content[1]
        log_content, tail = log_and_tail.split("</div>", 1)
        log_content = log_content + html_block
        new_content = head + "<div class=\"glyph-log\">" + log_content + "</div>" + tail
        with open(FEED_HTML, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as exc:
        print(f"Failed to append HTML: {exc}")


def main():
    tweet = fetch_latest_tweet(TWITTER_USERNAME)
    block = fetch_latest_block()
    if not block or not tweet:
        print("Missing data; aborting update")
        return
    entry = {
        "glyph": tweet.get("text", "Unnamed Glyph")[:50],
        "event": tweet.get("text", "").replace("\n", " ")[:120],
        "tweet_url": f"https://x.com/{TWITTER_USERNAME}/status/{tweet['id']}",
        "block": {
            "id": block.get("id"),
            "timestamp": block.get("timestamp"),
            "miner": block.get("miner", ""),
            "tx_count": block.get("tx_count", 0),
            "reward": block.get("reward", 0),
        },
    }
    append_json(entry)
    append_html(entry)
    print("Glyphchain updated")


if __name__ == "__main__":
    main()
