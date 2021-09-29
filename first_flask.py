from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    """List all routs that are available"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


def hello_world():
    return "hello world!"






app.run(debug=True)