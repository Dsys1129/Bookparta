from flask import Flask, render_template, request, jsonify
from bson.objectid import ObjectId
import crawling

app = Flask(__name__)

from pymongo import MongoClient
import config

client = MongoClient(config.DB_URL)

db = client.dbsparta


@app.route("/") #첫화면은 로그인 화면
def home():
    return render_template("index.html")

#로그인 정보
@app.route('/', methods=['POST'])
def book_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']


    #id와 pw가 DB에 있는지 확인
    member_check = db.members.find_one({'id':id_receive, 'pw':pw_receive})

    #회원가입이 되어있을 경우
    if member_check is not None:
        return jsonify({'result': 'login success'}) #later : 로그인한 사람의 이름 넘겨주기
    else:   
        return jsonify({'result': 'login failed'})
    
#회원가입
@app.route('/join', methods=['POST'])
def book_join():
    id_receeive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    

    doc = {
        'id':id_receeive,
        'pw':pw_receive,
        'name':name_receive
    }

    #아이디 존재여부 확인
    registerd = db.members.find_one({'id':id_receeive})

    if registerd is not None:
        return jsonify({'result':'fail', 'msg':'사용중인 아이디입니다!'})
    else:
        db.members.insert_one(doc)
        return jsonify({'result':'success'})
    
@app.route("/join")
def join():
    return render_template("join.html")


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
