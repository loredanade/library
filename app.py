from flask import Flask, make_response, jsonify, request, render_template
from pony.orm import db_session, select
from models import Book
from datetime import date, datetime


app = Flask(__name__)

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

if __name__== "__main__":
    app.run(port=8080)


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