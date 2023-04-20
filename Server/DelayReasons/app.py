from flask import Blueprint

app = Blueprint('Delay reasons', __name__)


if __name__ == "__main__":
    app.run(debug=True)
