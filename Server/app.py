from flask import Flask
from flask_cors import CORS
from Server.Airline.app import app as app1
from Server.Airport.app import app as app2
from Server.DelayReasons.app import app as app3
from Server.DelayRecovery.app import app as app4
from Server.Times.app import app as app5

app = Flask(__name__)
CORS(app)

app.register_blueprint(app1)
app.register_blueprint(app2)
app.register_blueprint(app3)
app.register_blueprint(app4)
app.register_blueprint(app5)


if __name__ == "__main__":
    app.run(debug=True)
