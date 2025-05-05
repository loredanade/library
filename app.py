from flask import Flask, make_response, jsonify, request, render_template
from pony.orm import db_session, select
from models import Book,Loan
from datetime import date, datetime


app = Flask(__name__)

def add_loan(json_request):
    try:
        name=json_request["name"]
        book_id=json_request["book_id"]
        book=Book.get(id=int(book_id))
        if book.available_quantity < 1:
            return {"response": "Fail", "error": "No books available"}
        with db_session:
            Loan(name=name, book=book)
            update_book(book_id, {"available_quantity": book.available_quantity-1})
            response={"response": "Success"}
            return response
    except Exception as e:
         return {"response": "Fail", "error": str(e)}

def update_book(id,json_request):
    try:
        with db_session:
            book=Book[id]
            allowed_fields = {'title', 'author', 'published_date', 'type', 'quantity', 'available_quantity', 'status', 'genres'}
            for key, value in json_request.items():
                if key in allowed_fields:
                    setattr(book, key, value)
            response={"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def add_book(json_request):
    try:
        title=json_request["title"]
        author=json_request["author"]
        type = json_request.get("type","")
        quantity=json_request["quantity"]
        available_quantity=json_request["quantity"]
        genres=json_request.get("genres", [])  
        try:
            published_date=datetime.strptime(json_request["published_date"], '%d-%m-%Y')
            print(published_date)
        except ValueError:
            published_date=None
        with db_session:
            Book(title=title, author=author, type=type, quantity=quantity,available_quantity=available_quantity, published_date=published_date, genres=genres)
            response={"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def get_books():
    try:
        with db_session:
            db_query=select(b for b in Book)[:]
            result_list=[]
            for q in db_query:
                result_list.append(q.to_dict())
            response= {"response": "Success", "data": result_list }
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def get_loans():
    try:
        with db_session:
            db_query=select(l for l in Loan)[:]
            result_list=[]
            for q in db_query:
                result_list.append(q.to_dict())
            response= {"response": "Success", "data": result_list }
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

@app.route('/', methods=["GET"])
@db_session
def getBooks():
    response = get_books()
    if response["response"]=="Success":
        return render_template('index.html', books=response["data"])
    return make_response(jsonify(response), 400)


@app.route('/books', methods=["POST"])
@db_session
def addBook():
    try:
        json_request=request.json
    except Exception as e:
        response={"response": str(e)}
        return make_response(jsonify(response), 400)
    response=add_book(json_request)
    if response["response"]=="Success":
         return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

@app.route("/books/<int:book_id>", methods=["PATCH"])
@db_session
def updateBookStatus(book_id):
    try:
        json_request=request.json
    except Exception as e:
        response={"response": str(e)}
        return make_response(jsonify(response), 400)
    response=update_book(book_id,json_request)
    if response["response"]=="Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)
@app.route("/loans", methods=["POST"])
@db_session
def addLoan():
    try:
        json_request=request.json
    except Exception as e:
        response={"response": str(e)}
        return make_response(jsonify(response), 400)
    response=add_loan(json_request)
    if response["response"]=="Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

@app.route("/loans", methods=["GET"])
@db_session
def getLoans():
    response = get_loans()
    if response["response"]=="Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

if __name__== "__main__":
    app.run(port=8080)


