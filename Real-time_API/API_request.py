import requests
import json
import time

from DB.mongo_db.config import articles_collection
from config import newsapi_key, newsapi_url, groqapi_key, groqapi_url



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


def classify_article(body):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groqapi_key}"
    }

    payload = {
        "messages": [
            {"role": "system",
             "content": "You are a helper who categorizes news articles into one of the categories (general news, historical terrorist event, contemporary terrorist event) and locations."},
            {"role": "user", "content": f"This is a news article: {body}"}
        ],
        "model": "grok-2-1212",
        "stream": False,
        "temperature": 0
    }

    response = requests.post(groqapi_url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']

            classification = None
            location = None

            if "Category:" in content:
                classification = content.split("Category:")[1].split("\n")[0].strip()
            if "Location:" in content:
                location = content.split("Location:")[1].split("\n")[0].strip()

            return classification if classification else "Unknown", location if location else "Unknown"
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {response.text}")
            return "Unknown", "Unknown"
        except KeyError as e:
            print(f"KeyError: Missing expected key in response - {e}")
            return "Unknown", "Unknown"
    else:
        print(f"Failed to classify article. Status code: {response.status_code}")
        print(f"Error details: {response.text}")
        return "Unknown", "Unknown"


def process_article(article):
    title = article.get("title")
    body = article.get("body", "")
    url = article.get("url")
    date = article.get("dateTime")

    classification, location = classify_article(body)

    article_data = {
        "title": title,
        "dateTime": date,
        "url": url,
        "body": body,
        "classification": classification,
        "location": location
    }

    articles_collection.insert_one(article_data)

    print(f"Article '{title}' saved to MongoDB.")
    print("-" * 50)


def process_articles():
    page = 1
    while True:
        print(f"Fetching articles from page {page}...")
        articles_data = fetch_news_articles(page)
        if articles_data and "articles" in articles_data:
            articles = articles_data["articles"]["results"]
            for article in articles:
                process_article(article)
        else:
            print("No articles found or failed to fetch.")
        page += 1
        print("Waiting for 2 minutes before fetching next batch...")
        time.sleep(120)


if __name__ == "__main__":
    process_articles()
