from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

BOOKS = []
next_id = 1

#GET 
@app.route("/books")
def listBooks():
    return jsonify({
        "data": BOOKS,
        "total": len(BOOKS)
    }), 200

#POST
@app.route("/books", methods = ["POST"])
def post():
    global next_id
    p = request.get_json(silent = True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()

    if not t or not a:
        return jsonify("title and author required"), 422
    #create book
    book = {
        "id": next_id,
        "title": t,
        "author": a,
    }

    BOOKS.append(book)
    next_id += 1

    #tra ve book vua tao
    resp = make_response(jsonify(book), 201)

    #header location tro toi tai nguyen vua tao
    resp.headers["Location"] = f"books/{book['id']}"

    return resp

if __name__ == "__main__":
    app.run(debug = True)