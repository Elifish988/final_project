from flask import Blueprint, request, jsonify

from queries.servic_queries_b import  shared_to_targets_service

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