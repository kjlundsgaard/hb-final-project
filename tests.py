import unittest
from server import app
from model import db, example_data, connect_to_db


class TestsDatabase(unittest.TestCase):
    """Flask tests using database"""

    def setUp(self):
        """To do before every test"""

        self.client = app.test_client()
        app.config['SECRET_KEY'] = '123'
        app.config['TESTING'] = True

        """connect to test database"""
        connect_to_db(app, "postgresql:///testdb")

        """Creates tables and adds example data to testdb"""
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 1

    def tearDown(self):
        """To do at end of test"""

        db.session.close()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()
