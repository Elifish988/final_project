import requests
from config import newsapi_key, newsapi_url, groqapi_key, groqapi_url, opencage_url, opencage_key


# שליפת מאמרים מ-Event Registry API
def get_articles(page):
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
        "apiKey": newsapi_key,
    }
    response = requests.post(newsapi_url, json=payload)

    # בדיקה אם הבקשה הצליחה
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error: Failed to parse JSON response.")
            return None
    else:
        print(f"Error: Request failed with status code {response.status_code}")
        return None


# סיווג מאמרים בעזרת GroqAPI
def classify_event(text):
    headers = {"Authorization": f"Bearer {groqapi_key}"}
    payload = {"text": text}
    response = requests.post(groqapi_url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None


# זיהוי נקודות ציון בעזרת OpenCage API
def geocode_location(location_name):
    params = {"q": location_name, "key": opencage_key}
    response = requests.get(opencage_url, params=params)
    return response.json() if response.status_code == 200 else None


# תהליך עיבוד
def process_articles():
    page = 1
    while True:
        articles = get_articles(page)
        if not articles:
            print("No articles found or response format error.")
            break  # יציאה אם לא נמצאו מאמרים

        print(f"Articles response: {articles}")  # הדפסת התשובה כדי לראות את המבנה שלה

        if isinstance(articles, dict) and "articles" in articles:
            for article in articles["articles"]:
                # אם ה-article הוא מחרוזת ולא מילון
                if isinstance(article, dict):
                    title = article.get("title")
                    body = article.get("body")
                    if not body:
                        continue  # לדלג אם אין תוכן

                    location = classify_event(body)  # סיווג לקטגוריה
                    if location and "location" in location:
                        geocode = geocode_location(location["location"])
                        if geocode:
                            print(f"Article: {title}")
                            print(f"Geolocation: {geocode.get('geometry')}")
                else:
                    print("Found an article that is not a dictionary. Skipping.")
        else:
            print("Error: 'articles' key not found in the response or invalid response format.")
            break

        page += 1


# הפעלת התהליך
process_articles()
