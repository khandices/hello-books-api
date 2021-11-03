import pytest
from app import create_app
from app import db
from app.models.book import Book



@pytest.fixture
# When we run our tests, this line will run and create an app object. It's using the same create_app function defined in our app/__init__.py file!
def app():

    # Here, we're passing in a dictionary to represent a "test config" object. The current implementation of create_app() in app/__init__.py uses this argument only to check if it's truthy(which this is!).
    app = create_app({"TESTING": True})

    # This syntax designates that the following code should have an application context. This lets various functionality in Flask determine what the current running app is . This is particularly important when accessing the database associated with the app.
    with app.app_context():
        db.create_all()
        # This fixture suspends here, returning the app for use in tests or other fixtures. The lines after this yield statement will run after the test using the app has been completed.
        yield app
    # After the test runs, this code specifies that we should drop all of the tables, deleting any data that was created during the test.
    with app.app_context():
        db.drop_all()


@pytest.fixture
# This fixture is named client. It will request the existing app fixture to run, first.
def client(app):
    # The responsibility of this fixture is to make a test client, which is an object able to simulate a client making HTTP requests.
    return app.test_client()


@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                      description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                         description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()
