from flask import Flask, make_response, jsonify, request, render_template, redirect
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
def remove_loan(book_id, loan_id):
    try:
        book=Book.get(id=int(book_id))
        with db_session:
            
            update_book(book_id, {"available_quantity": book.available_quantity+1})
            update_loan(loan_id, {"returned_at": datetime.now()})
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
def update_loan(id,json_request):
    try:
        with db_session:
            loan=Loan[id]
            allowed_fields = {'returned_at', 'name'}
            for key, value in json_request.items():
                if key in allowed_fields:
                    setattr(loan, key, value)
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
    
def get_book(book_id):
    try:
        with db_session:
            book = Book.get(id=book_id)
            if not book:
                return None, "Book not found"
            
            loans = [
                {
                    "name": loan.name,
                    "created_at": loan.created_at.strftime('%d-%m-%Y'),
                    "id": loan.id,
                    "returned_at": loan.returned_at
                }
                for loan in book.loans if loan.returned_at is None
            ]            
            book_data = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "published_date": book.published_date.strftime('%d-%m-%Y'),
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "status": book.status,
                "loans": loans
            }
            return book_data, None

    except Exception as e:
        return None, str(e)
    
def get_loans():
    try:
        with db_session:
            db_query = select(l for l in Loan)[:]
            result_list = []
            for loan in db_query:
                loan_data = loan.to_dict()
                loan_data["book"] = {
                    "id": loan.book.id,
                    "title": loan.book.title
                }
                result_list.append(loan_data)

            response = {"response": "Success", "data": result_list}
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
def updateBook(book_id):
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
        return render_template("loans.html",loans=response["data"])
    return make_response(jsonify(response), 400)

@app.route('/books/<int:book_id>')
@db_session
def book_loans(book_id):
    try:
        book_data, error = get_book(book_id)
        if error:
            return make_response(jsonify({"response": "Fail", "error": error}), 400)
        return render_template("book-loans.html",data=book_data)
    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)

@app.route('/books/<int:book_id>/loans/<int:loan_id>', methods=['POST'])
@db_session
def mark_loan_as_returned(book_id, loan_id):
    response=remove_loan(book_id,loan_id)
    if response["response"]=="Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


if __name__== "__main__":
    app.run(port=8080)


