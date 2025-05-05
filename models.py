from pony.orm import Database, Required, Set, PrimaryKey, Optional, Json
from datetime import date

db = Database()

class Book(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    author = Required(str)
    published_date = Required(date)
    type = Optional(str)
    quantity = Required(int)
    available_quantity = Required(int)
    created_at = Required(date, default=lambda: date.today())
    status = Required(str, default="published")
    genres=Optional(Json)
    loans = Set('Loan')

class Loan(db.Entity):
    id = PrimaryKey(int, auto=True)
    book = Required('Book')
    name = Required(str)
    created_at = Required(date, default=lambda: date.today())
    returned_at = Optional(date)


db.bind(provider='sqlite', filename='books.sqlite', create_db=True)
db.generate_mapping(create_tables=True)