from flask import Blueprint, jsonify

from DB.postges_db.db import Base, engine, session
from load.load_servic import load_all_csv

bp_load = Blueprint('bp_load', __name__)



@bp_load.route("/load", methods=["GET"])
def get_top_deadliest_attacks():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session.commit()
    load_all_csv()
    return jsonify({"message": "CSV files loaded successfully"})
