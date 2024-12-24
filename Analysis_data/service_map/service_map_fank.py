import requests
import folium
import pandas as pd

def get_avg_casualties_by_region_servie_map(result_df):
    url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"
    response = requests.get(url)
    geojson_data = response.json()
    casualties_dict = {data["country_txt"]: data["avg_casualties"] for data in result_df}
    casualties_values = list(casualties_dict.values())
    quintiles = pd.qcut(casualties_values, 5, labels=['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#E31A1C'])
    color_mapping = {list(casualties_dict.keys())[i]: quintiles[i] for i in range(len(casualties_dict))}

    def style_function(feature):
        country_name = feature["properties"]["name"]
        color = color_mapping.get(country_name, "#B0B0B0")
        return {
            "fillColor": color,
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        }

    m = folium.Map(location=[20, 0], zoom_start=2)
    for feature in geojson_data['features']:
        country_name = feature['properties']['name']
        casualties = casualties_dict.get(country_name, "No data")
        tooltip_text = f"{country_name}: {casualties}"

        folium.GeoJson(
            feature,
            style_function=style_function,
            tooltip=folium.Tooltip(tooltip_text)
        ).add_to(m)
    map_html = m._repr_html_()
    return map_html