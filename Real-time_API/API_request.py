import requests
from config import newsapi_key, newsapi_url, groqapi_key, groqapi_url, opencage_url, opencage_key


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
            print("לא נמצאו מאמרים או שגיאה בפורמט התשובה.")
            break  # יוצאים אם לא נמצאו מאמרים או אם יש שגיאה

        print("תשובה מלאה מה-API:", articles)  # הדפס את התשובה המלאה כדי להבין את הפורמט

        if isinstance(articles, dict) and "articles" in articles:
            for article in articles["articles"]:
                # הדפס את סוג המאמר כדי להבין יותר את הבעיה
                print(f"סוג המאמר: {type(article)}")

                if isinstance(article, dict):
                    title = article.get("title")
                    body = article.get("body")
                    if not body:
                        continue  # דילוג על מאמרים שאין להם גוף

                    location = classify_event(body)  # מיון המיקום לפי גוף המאמר
                    if location and "location" in location:
                        geocode = geocode_location(location["location"])
                        if geocode:
                            print(f"מאמר: {title}")
                            print(f"גיאולוקציה: {geocode.get('geometry')}")
                else:
                    print(f"מדלגים על מאמר בגלל סוג בלתי צפוי: {type(article)}")
        else:
            print("שגיאה: לא נמצא מפתח 'articles' בתשובה או שהפורמט שגוי.")
            break  # יוצאים אם מפתח 'articles' לא קיים או אם הפורמט שגוי

        page += 1




# הפעלת התהליך
process_articles()
