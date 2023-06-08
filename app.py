from flask import Flask, render_template, request, jsonify
from bson.objectid import ObjectId
import crawling

app = Flask(__name__)

from pymongo import MongoClient
import config

client = MongoClient(config.DB_URL)

db = client.dbsparta


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/books", methods=["POST"])
def add_books():
    url_receive = request.form["url"]

    # url 파싱
    crawling_data = crawling.crawling_book(url_receive)
    book_doc = {
        "title": crawling_data["title"],
        "author": crawling_data["author"],
        "description": crawling_data["desc"],
        "image": crawling_data["image"],
        "reviews": [],
    }
    db.books.insert_one(book_doc)
    return jsonify({"status": "201"})


@app.route("/books/<bookId>")
def get_book(bookId):
    book = db.books.find_one({"_id": ObjectId(bookId)})
    book["_id"] = str(book["_id"])
    return jsonify({"book": book})


@app.route("/books")
def get_books():
    # Object형인 id를 serialization 할 수 없어 str로 변경 후 json으로 반환
    all_books = list(db.books.find({}, {"reviews": False}))
    for book in all_books:
        book["_id"] = str(book["_id"])
    return jsonify({"books": all_books})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
