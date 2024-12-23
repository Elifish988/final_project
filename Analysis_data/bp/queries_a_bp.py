from flask import Blueprint, request, jsonify

from Analysis_data.services.servic_queries_a import get_top_deadliest_attacks_service, get_avg_casualties_by_region_service, \
    get_top_5_gnames_by_casualties_service, get_percentage_change_in_attacks_by_country_service, \
    get_most_active_groups_by_region_service

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
    return jsonify(result_df.to_dict(orient='records'))



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