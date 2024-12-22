from flask import Blueprint, request, jsonify

from queries.servic_queries_b import shared_to_targets_service, shared_attack_strategies_by_region_service, \
    groups_with_similar_target_preferences_service

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