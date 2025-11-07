# fetch_news.py
import json, os, time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

API_KEY = os.environ.get("NEWSAPI_KEY")  # set in GitHub Actions secrets
QUERY = "stocks OR market OR equities OR S&P OR Nasdaq OR Federal Reserve OR earnings"
PAGE_SIZE = 50

def get(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

def fetch_news():
    if not API_KEY:
        raise RuntimeError("Missing NEWSAPI_KEY environment variable")

    params = {
        "q": QUERY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY
    }
    url = f"https://newsapi.org/v2/everything?{urlencode(params)}"
    data = json.loads(get(url))
    articles = data.get("articles", [])

    items = []
    for a in articles:
        items.append({
            "title": a.get("title"),
            "source": a.get("source", {}).get("name"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
            "description": a.get("description")
        })

    out = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(items),
        "items": items
    }
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    top = [f"- {i['title']} ({i['source']})" for i in out["items"][:3]]
    with open("post.txt", "w", encoding="utf-8") as f:
        f.write(
            "Market Pulse: top headlines\n" +
            "\n".join(top) +
            "\n\nNot financial advice."
        )

if __name__ == "__main__":
    fetch_news()
