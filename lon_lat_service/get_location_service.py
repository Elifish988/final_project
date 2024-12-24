from config import opencage_key
import requests

def get_location(name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={name}&key={opencage_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data["results"]:
            location = data["results"][0]["geometry"]
            lon = location["lng"]
            lat = location["lat"]
            return lat, lon  # מחזיר את הערכים כנפרדים
        else:
            print(f"No geolocation data found for {name}.")
            return None, None  # במקרה שאין מיקום
    else:
        print(f"Error fetching geolocation data: {response.status_code}")
        return None, None  # במקרה של בעיה בשאילתה
print(get_location("India"))