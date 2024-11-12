import mrequests as requests
from app_keys import NEWSAPI_KEY

# Fetch news data
def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
    try:
        response = requests.get(url,headers={"User-Agent": "Zissis"})
        if response.status_code == 200:
            news_data = response.json()
            response.close()
            return news_data.get("articles", [])
        else:
            print("Failed to fetch news:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Print news to serial
def print_news():
    articles = fetch_news()
    print("\nLatest News Headlines:\n")
    for i, article in enumerate(articles[:5]):  # Limit to 5 headlines for simplicity
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        print(f"{i + 1}. {title}\n   {description}\n")

