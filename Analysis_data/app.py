from  flask import Flask

from Analysis_data.bp.queries_a_bp import bp_queries_a
from Analysis_data.bp.queries_b_bp import bp_queries_b

app = Flask(__name__)

app.register_blueprint(bp_queries_a)

app.register_blueprint(bp_queries_b)


if __name__ == '__main__':
    app.run(debug=True)