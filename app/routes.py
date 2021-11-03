from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)
    

@books_bp.route("", methods=["GET"])
def read_books():
    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)
        

@books_bp.route("/<book_id>", methods=["GET"])
def read_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)

    if book == None:
        return make_response("", 404)
    
    return book.to_dict()


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
        form_data = request.get_json()
        book_id = int(book_id)
        book = Book.query.get(book_id)

        if book == None:
            return make_response("", 404)

        book.title = form_data["title"]
        book.description = form_data["description"]
        db.session.commit()
        return make_response(f"Book #{book.id} successfully updated")
    

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
        book_id = int(book_id)
        book = Book.query.get(book_id)

        if book == None:
            return make_response("", 404)

        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")
    
