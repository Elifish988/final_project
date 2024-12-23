from  flask import Flask
from load_b.load_bp import bp_load_b

app = Flask(__name__)

app.register_blueprint(bp_load_b)


if __name__ == '__main__':
    app.run(debug=True)