from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/datacenter")
def get_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False, port=5000)
