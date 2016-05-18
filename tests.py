import unittest
import server
from model import db, example_data, connect_to_db


class TestNotLoggedIn(unittest.TestCase):
    """Flask tests to check when session is empty"""

    def setUp(self):
        """To do before every test"""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = '123'

        connect_to_db(server.app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """To do at end of test"""

        db.session.close()
        db.drop_all()

    def test_log_in_form(self):
        """test to show log in form"""

        result = self.client.get("/")
        self.assertIn('Log in:', result.data)
        self.assertNotIn('Create new', result.data)


# class TestsDatabase(unittest.TestCase):
#     """Flask tests using database"""

#     def setUp(self):
#         """To do before every test"""

#         self.client = app.test_client()
#         app.config['SECRET_KEY'] = '123'
#         app.config['TESTING'] = True

#         """connect to test database"""
#         connect_to_db(app, "postgresql:///testdb")

#         """Creates tables and adds example data to testdb"""
#         db.create_all()
#         example_data()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user'] = 1

#     def tearDown(self):
#         """To do at end of test"""

#         db.session.close()
#         db.drop_all()


if __name__ == "__main__":
    # server.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    unittest.main()
