from pony.orm import Database, Required, Set, PrimaryKey
from datetime import date

db = Database()

class Book(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    author = Required(str)
    published_day = Required(date)
    description = Required(str)
    quantity = Required(int)
    available_quantity = Required(int)
    loans = Set('Reservation')

class Loan(db.Entity):
    id = PrimaryKey(int, auto=True)
    book = Required('Book')
    borrowed_at = Required(date)
    returned_at = Required(date)

db.bind(provider='sqlite', filename='books.sqlite', create_db=True)
db.generate_mapping(create_tables=True)