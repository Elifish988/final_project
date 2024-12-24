import pandas as pd
from flask import Blueprint, request, jsonify
import folium
from flask import jsonify
from Analysis_data.services.servic_queries_a import get_top_deadliest_attacks_service, get_avg_casualties_by_region_service, \
    get_top_5_gnames_by_casualties_service, get_percentage_change_in_attacks_by_country_service, \
    get_most_active_groups_by_region_service
from lon_lat_service.get_location_service import get_location

bp_queries_a = Blueprint('bp_queries_a', __name__)

# קבוצת שאלות א
# ---------------

# סוגי ההתקפה הקטלניים ביותר.
@bp_queries_a.route("/get_top_deadliest_attacks", methods=["GET"])
def get_top_deadliest_attacks():
    top = request.args.get('top', 'all')
    result_df = get_top_deadliest_attacks_service(top)
    return jsonify(result_df.to_dict(orient='records'))




import requests
import folium
import pandas as pd
from flask import jsonify

@bp_queries_a.route("/get_avg_casualties_by_region", methods=["GET"])
def get_avg_casualties_by_region():
    top = request.args.get('top', 'all')
    result_df = get_avg_casualties_by_region_service(top)


    # טוען את קובץ GeoJSON מהאינטרנט
    url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
    response = requests.get(url)
    geojson_data = response.json()

    # יצירת מילון לערכי avg_casualties לפי מדינה
    casualties_dict = {data["country_txt"]: data["avg_casualties"] for data in result_df}

    # חישוב אחוזונים לחלוקה לצבעים
    casualties_values = list(casualties_dict.values())
    quintiles = pd.qcut(casualties_values, 5, labels=['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#E31A1C'])

    # מיפוי שם מדינה לצבע
    color_mapping = {list(casualties_dict.keys())[i]: quintiles[i] for i in range(len(casualties_dict))}

    # פונקציה לקביעת סגנון עבור GeoJSON
    def style_function(feature):
        country_name = feature["properties"]["name"]
        color = color_mapping.get(country_name, "#B0B0B0")  # ברירת מחדל לצבע אפור
        return {
            "fillColor": color,
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        }

    # פונקציה ליצירת tooltip עם avg_casualties
    def tooltip_function(feature):
        country_name = feature["properties"]["name"]
        casualties = casualties_dict.get(country_name, "No data")
        return f"{country_name}: {casualties}"

    # יצירת המפה
    m = folium.Map(location=[20, 0], zoom_start=2)

    # הוספת שכבת GeoJSON עם סגנון מותאם
    folium.GeoJson(
        geojson_data,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["Country:"],
            localize=True,
            labels=False,
            sticky=True
        ),
        highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.9},
        popup=folium.GeoJsonPopup(
            fields=["name"],
            aliases=["Country:"],
            localize=True
        )
    ).add_to(m)

    # המרת המפה ל-HTML string
    map_html = m._repr_html_()

    return map_html




# חמשה קבוצות עם הכי הרבה נפגעים לאורך השנים
@bp_queries_a.route("/get_top_5_gnames_by_casualties", methods=["GET"])
def get_top_5_gnames_by_casualties():
    result_df = get_top_5_gnames_by_casualties_service()
    return jsonify(result_df.to_dict(orient='records'))


# אחוז שינוי במספר הפיגועים בין שנים לפי אזור
@bp_queries_a.route("/get_percentage_change_in_attacks_by_country", methods=["GET"])
def get_percentage_change_in_attacks_by_country():
    top = request.args.get('top', 'all')
    result_df = get_percentage_change_in_attacks_by_country_service(top)
    return jsonify(result_df.to_dict(orient='records'))

# הקבוצות הפעילות ביותר באזור מסוים
@bp_queries_a.route("/get_most_active_groups_by_region", methods=["GET"])
def get_most_active_groups_by_region():
    country_txt = request.args.get('country_txt')
    result_df = get_most_active_groups_by_region_service(country_txt)
    return jsonify(result_df.to_dict(orient='records'))