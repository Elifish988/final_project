from kafka import KafkaConsumer
import json
from DB.mongo_db.config import articles_collection
from config import groqapi_key, groqapi_url
import requests

consumer = KafkaConsumer(
    'articles_topic',
    bootstrap_servers='localhost:27017',
    group_id='article_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def classify_article(body):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groqapi_key}"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helper who categorizes news articles into one of the categories (general news, historical terrorist event, contemporary terrorist event) and locations."},
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

def consume_articles():
    for message in consumer:
        article = message.value
        body = article.get("body", "")
        title = article.get("title")
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

if __name__ == "__main__":
    consume_articles()
