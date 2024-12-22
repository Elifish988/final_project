from  flask import Flask

from queries.queries_a_bp import bp_queries_a
from queries.queries_b_bp import bp_queries_b

app = Flask(__name__)

app.register_blueprint(bp_queries_a)

app.register_blueprint(bp_queries_b)


if __name__ == '__main__':
    app.run(debug=True)