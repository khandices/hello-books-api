from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# This built-in module provides a way to read environment variables
import os

db = SQLAlchemy()
migrate = Migrate()

# The python-dotenv package specifies to call this method, which loads the values from our .env file so that the os module is able to see them.
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    # registers the Book Model with app
    from app.models.book import Book
    from app.models.author import Author
    from app.models.genre import Genre
    from app.models.bookgenre import BookGenre

    # Registers the routes and bluepreint to the app
    from .routes import books_bp, authors_bp, genres_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(genres_bp)

    return app
