from flask import Blueprint, jsonify
from DB.postges_db.db import session
from load_b.load_servic import load_all_csv_b

bp_load_b = Blueprint('bp_load_b', __name__)



@bp_load_b.route("/load", methods=["GET"])
def get_top_deadliest_attacks():
    session.commit()
    load_all_csv_b()
    return jsonify({"message": "CSV_b files loaded successfully"})
