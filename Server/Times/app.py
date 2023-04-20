from flask import Blueprint

app = Blueprint('Times', __name__)


if __name__ == "__main__":
    app.run(debug=True)
