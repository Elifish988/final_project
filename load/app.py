from  flask import Flask

from load.load_bp import bp_load

app = Flask(__name__)

app.register_blueprint(bp_load)


if __name__ == '__main__':
    app.run(debug=True)