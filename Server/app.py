from flask import Flask
from flask_cors import CORS
from Airline.app import app as app1
from Airport.app import app as app2
from DelayReasons.app import app as app3
from DelayRecovery.app import app as app4
from Times.app import app as app5
from prediction.app import app as app6

app = Flask(__name__)
CORS(app)

app.register_blueprint(app1)
app.register_blueprint(app2)
app.register_blueprint(app3)
app.register_blueprint(app4)
app.register_blueprint(app5)
app.register_blueprint(app6)

if __name__ == "__main__":
    app.run(debug=True)
