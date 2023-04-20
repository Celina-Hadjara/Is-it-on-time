from flask import Blueprint

app = Blueprint('Delay recovery', __name__)


if __name__ == "__main__":
    app.run(debug=True)
