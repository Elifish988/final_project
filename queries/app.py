from  flask import Flask

from queries.queries_a_bp import bp_queries

app = Flask(__name__)

app.register_blueprint(bp_queries)


if __name__ == '__main__':
    app.run(debug=True)