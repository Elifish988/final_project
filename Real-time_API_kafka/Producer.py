from kafka import KafkaProducer
import json
import requests
import time
from config import newsapi_key, newsapi_url

producer = KafkaProducer(
    bootstrap_servers='localhost:27017',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_news_articles(page):
    payload = {
        "action": "getArticles",
        "keyword": "terror attack",
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": page,
        "articlesCount": 100,
        "articlesSortBy": "socialScore",
        "articlesSortByAsc": False,
        "dataType": ["news", "pr"],
        "forceMaxDataTimeWindow": 31,
        "resultType": "articles",
        "apiKey": newsapi_key
    }

    response = requests.post(newsapi_url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None

def produce_articles():
    page = 1
    while True:
        print(f"Fetching articles from page {page}...")
        articles_data = fetch_news_articles(page)
        if articles_data and "articles" in articles_data:
            articles = articles_data["articles"]["results"]
            for article in articles:
                producer.send('articles_topic', article)
        else:
            print("No articles found or failed to fetch.")
        page += 1
        print("Waiting for 2 minutes before fetching next batch...")
        time.sleep(120)

if __name__ == "__main__":
    produce_articles()
