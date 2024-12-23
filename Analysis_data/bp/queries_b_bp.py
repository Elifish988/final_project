from flask import Blueprint, request, jsonify

from Analysis_data.services.servic_queries_b import shared_to_targets_service, shared_attack_strategies_by_region_service, \
    groups_with_similar_target_preferences_service, get_high_intergroup_activity_areas_service, \
    get_groups_with_same_targets_by_year_and_country_service

bp_queries_b = Blueprint('bp_queries_b', __name__)

# קבוצת שאלות ב
# ---------------

# זיהוי קבוצות עם מטרות משותפות באותו אזור
@bp_queries_b.route("/shared_to_targets", methods=["GET"])
def shared_to_targets():
    region = request.args.get('region')
    country = request.args.get('country')

    data = shared_to_targets_service(region, country)
    return jsonify(data)


# זיהוי אזורים עם אסטרטגיות תקיפה משותפות בין קבוצות
@bp_queries_b.route("/shared_attack_strategies_by_region", methods=["GET"])
def shared_attack_strategies_by_region():
    data = shared_attack_strategies_by_region_service()
    return jsonify(data)

# איתור קבוצות עם העדפות דומות למטרות
# בעלות תיעדוף של לפחות 10 פעמים בשנה
@bp_queries_b.route("/groups_with_similar_target_preferences", methods=["GET"])
def groups_with_similar_target_preferences():
    data = groups_with_similar_target_preferences_service()
    return jsonify(data)


# זיהוי אזורים עם פעילות בין-קבוצתית גבוהה.

@bp_queries_b.route("/get_high_intergroup_activity", methods=["GET"])
def get_high_intergroup_activity():
    filtered_areas = get_high_intergroup_activity_areas_service()
    return jsonify(filtered_areas)

# זיהוי קשרים בין קבוצות עם מטרות משותפות באותו זמן
@bp_queries_b.route("/get_groups_with_same_target_same_year_by_country", methods=["GET"])
def get_groups_with_same_target_same_year_by_country():
    filtered_areas = get_groups_with_same_targets_by_year_and_country_service()
    return jsonify(filtered_areas)