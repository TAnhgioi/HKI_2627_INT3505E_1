from flask import Flask, jsonify, request

app = Flask(__name__)

_next = 2

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "year": 2000}
]


def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# LIST — GET /books
@app.route("/books", methods=["GET"])
def list_books():
    result = BOOKS.copy()

    # TÌM KIẾM
    q = request.args.get("q")

    if q:
        result = [
            b for b in result
            if q.lower() in b["title"].lower()
            or q.lower() in b["author"].lower()
        ]

    # SẮP XẾP
    sort = request.args.get("sort")

    if sort == "title":
        result.sort(key=lambda b: b["title"].lower())

    # GIỚI HẠN SỐ LƯỢNG
    limit = int(request.args.get("limit", 100))
    result = result[:limit]

    return jsonify(result), 200

# DETAIL — GET /books/<int:bid>
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find(bid)

    if not book:
        return {"error": "not found"}, 404

    return jsonify(book), 200

# CREATE — POST /books
@app.route("/books", methods=["POST"])
def create_book():
    global _next

    body = request.get_json(silent=True) or {}

    t = body.get("title")
    a = body.get("author")
    year = body.get("year")

    # Kiểm tra year
    if not isinstance(year, int) or isinstance(year, bool) or year < 1900:
        return {"error": "year must be an integer >= 1900"}, 400

    if not t or not a:
        return {"error": "need title+author"}, 400

    book = {
        "id": _next,
        "title": t,
        "author": a
    }

    _next += 1
    BOOKS.append(book)

    return jsonify(book), 201, {
        "Location": f"/books/{book['id']}"
    }

# UPDATE — PUT /books/<int:bid>
# DELETE — DELETE /books/<int:bid>
@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find(bid)

    if not book:
        return {"error": "not found"}, 404

    # PUT
    if request.method == "PUT":
        book.update(request.get_json(silent=True) or {})
        return jsonify(book), 200

    # DELETE
    BOOKS.remove(book)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)