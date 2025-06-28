import requests
from bs4 import BeautifulSoup

# Simple DuckDuckGo scrape to simulate YouTube search without needing API key
def fetch_youtube_links(query):
    search_query = query + " site:youtube.com"
    url = f"https://html.duckduckgo.com/html/?q={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "youtube.com/watch" in href:
                text = link.get_text().strip()
                if text and len(results) < 3:
                    results.append((text[:60], href))
        return results
    except:
        return []
