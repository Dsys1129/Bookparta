from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import config

client = MongoClient(config.DB_URL)

db = client.config.DB_DATABASE


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
