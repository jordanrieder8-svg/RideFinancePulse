# fetch_news.py
import json, os, time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

API_KEY = os.environ.get("NEWSAPI_KEY")  # set in GitHub Actions secrets
QUERY = "stocks OR market OR equities OR S&P OR Nasdaq OR Federal Reserve OR earnings"
PAGE_SIZE = 50

def get(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    QUERY = os.environ.get("NEWS_QUERY", 
    # Comprehensive financial news filter covering:
    # Stocks, Earnings, Market Movers, Pre/Post Market, Indices, Credit, Commodities, Futures
    "stocks OR equities OR stock market OR share price OR "
    "earnings OR earnings report OR quarterly earnings OR revenue OR profit OR EPS OR "
    "market movers OR biggest movers OR top gainers OR top losers OR stock surge OR stock plunge OR "
    "pre-market OR premarket OR post-market OR after hours OR market close OR market open OR "
    "S&P 500 OR Dow Jones OR Nasdaq OR index OR indices OR market index OR "
    "market up OR market down OR percentage gain OR percentage loss OR stock rally OR market decline OR "
    "credit OR credit markets OR corporate bonds OR bond yields OR credit rating OR credit spread OR "
    "commodities OR oil prices OR gold prices OR silver OR wheat OR corn OR natural gas OR crude oil OR "
    "futures OR futures market OR commodity futures OR stock futures OR index futures"
)
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
