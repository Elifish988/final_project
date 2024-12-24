import requests
import json
import time

from config import groqapi_url, groqapi_key

# Define the schema in Python as a dictionary
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "news_classification",
        "schema": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "Current terrorism event",
                        "Past terrorism event",
                        "Other news event"
                    ]
                },
                "location": {
                    "type": "string",
                    "description": "The location where the event occurred"
                }
            },
            "required": ["classification", "location"],
            "additionalProperties": False
        },
        "strict": True
    }
}

# Function to send the request to classify articles
def classify_news_article(article_content):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groqapi_key}"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are an assistant classifying news articles into categories and locations."},
            {"role": "user", "content": f"This is a news article: {article_content}"}
        ],
        "model": "grok-2-1212",
        "stream": False,
        "temperature": 0,
        "response_format": response_format
    }

    # Send the request
    response = requests.post(groqapi_url, headers=headers, json=payload)

    # Check for successful response
    if response.status_code == 200:
        try:
            response_json = response.json()
            print("Raw API Response:", json.dumps(response_json, indent=4))  # הדפסת התגובה הגולמית

            # Extract the content which is a stringified JSON and parse it
            content = response_json['choices'][0]['message']['content']
            parsed_response = json.loads(content)  # פריסת ה-JSON בתוך ה-content

            # Return the classification and location
            classification = parsed_response.get("classification", "Unknown")
            location = parsed_response.get("location", "Unknown")
            return {"classification": classification, "location": location}
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return {"classification": "Unknown", "location": "Unknown"}
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return {"classification": "Unknown", "location": "Unknown"}

# Function to extract and classify articles
def extract_and_classify_articles(articles):
    results = articles.get("articles", {}).get("results", [])
    for result in results:
        dt = result.get("dateTime")
        title = result.get("title")
        body = result.get("body", "")
        first_200_words = " ".join(body.split()[:200])

        # Print the extracted data
        print(f"Date and Time: {dt}")
        print(f"Title: {title}")
        print(f"Snippet: {first_200_words}")

        # Classify the article using the classification function
        classification_response = classify_news_article(body)
        if classification_response:
            classification = classification_response.get("classification", "Unknown")
            location = classification_response.get("location", "Unknown")
            print(f"Classification: {classification}")
            print(f"Location: {location}")
        else:
            print("Failed to classify the article.")

        print("-" * 50)

# Function to simulate fetching articles (replace with your API call)
def fetch_articles():
    # Simulated data for testing
    return {
        "articles": {
            "results": [
                {
                    "uri": "2024-12-583281968",
                    "lang": "eng",
                    "dateTime": "2024-12-22T16:40:27Z",
                    "title": "German Mother Mourns Loss of 9-Year-Old Son in Christmas Market Attack",
                    "body": "Germany continues to reel from a terror attack committed by Taleb A., a Saudi man who was granted German citizenship...",
                },
                {
                    "uri": "2024-12-583281969",
                    "lang": "eng",
                    "dateTime": "2024-12-22T16:45:00Z",
                    "title": "Explosion in Central Paris Injures Several People",
                    "body": "An explosion rocked central Paris today, leaving several people injured. Authorities are investigating the cause...",
                }
            ]
        }
    }

# Main loop to fetch and classify articles every two minutes
def main_loop():
    while True:
        print("Fetching articles...")
        articles = fetch_articles()
        extract_and_classify_articles(articles)
        print("Waiting for 2 minutes before fetching again...")
        time.sleep(120)

# Run the main loop
if __name__ == "__main__":
    main_loop()
