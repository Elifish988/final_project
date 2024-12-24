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


# ממוצע נפגעים לפי איזור
@bp_queries_a.route("/get_avg_casualties_by_region", methods=["GET"])
def get_avg_casualties_by_region():
    top = request.args.get('top', 'all')
    result_df = get_avg_casualties_by_region_service(top)

    # יצירת המפה
    m = folium.Map(location=[20, 0], zoom_start=2)

    # חישוב אחוזונים לחלוקה לחמישה גוונים
    casualties_values = [data['avg_casualties'] for data in result_df]
    quintiles = pd.qcut(casualties_values, 5, labels=['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#E31A1C'])

    # יצירת מיפוי של מדינות לפי הגוון המתאים
    country_colors = {result_df[i]['country_txt']: quintiles[i] for i in range(len(result_df))}

    # הוספת המידע למפה
    for country_data in result_df:
        location = get_location(country_data['country_txt'])
        if location:
            color = country_colors[country_data['country_txt']]
            folium.CircleMarker(
                location,
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"{country_data['country_txt']}: {country_data['avg_casualties']} casualties"
            ).add_to(m)
        else:
            print(f"Warning: No location found for {country_data['country_txt']}")

    # המרת המפה ל-HTML string
    map_html = m._repr_html_()

    # החזרת המפה כתגובה
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