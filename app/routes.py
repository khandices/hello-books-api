from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

def is_input_valid(model_id):
    try:
        int(model_id)
    except:
        return make_response(f"{model_id} is not an int!", 400)


def is_parameter_found(model, parameter_id):
    if is_input_valid(parameter_id):
        return is_input_valid(parameter_id)
    elif model.query.get(parameter_id) is None:
        return make_response(f"Book '{parameter_id}' was not found!", 404)


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book '{new_book.title}' successfully created!", 201)
    

#  BOOKS ENDPOINTS

@books_bp.route("", methods=["GET"])
def read_books():
    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)
        

@books_bp.route("/<book_id>", methods=["GET"])
def read_book(book_id):
    valid_data = is_parameter_found(Book, book_id)
    if valid_data:
        return valid_data

    book_id = int(book_id)
    book = Book.query.get(book_id)
    return book.to_dict()


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
        valid_data = is_parameter_found(Book, book_id)
        if valid_data:
            return valid_data
        form_data = request.get_json()
        book_id = int(book_id)
        book = Book.query.get(book_id)

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()
        return make_response(f"Book #{book.id} successfully updated")
    

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
        valid_data = is_parameter_found(Book, book_id)
        if valid_data:
            return valid_data
        book_id = int(book_id)
        book = Book.query.get(book_id)

        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")
    

# AUTHORS ENDPOINTS

@authors_bp.route("", methods=["GET"])
def read_authors():
    authors = Author.query.all()
    authors_response = []
    for author in authors:
        authors_response.append(author.to_dict())
    return jsonify(authors_response)


@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(f"Author '{new_author.name}' successfully created!", 201)
