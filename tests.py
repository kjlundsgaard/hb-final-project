import unittest
from server import app, bcrypt
from model import db, connect_to_db, User, Group, List, UserGroup, Restaurant, RestaurantList, Fave


def example_data():
    """Create example data for the test database."""
    password = bcrypt.generate_password_hash('mypassword')

    user = User(email='user@gmail.com', password=password, fname='First', lname='Last')
    group = Group(group_name='Friends')
    user_group = UserGroup(user_id=1, group_id=1)
    category = List(list_name='Dinner', group_id=1)
    restaurant = Restaurant(restaurant_name='Taco Bell', yelp_rating=2.5, latitude=37.774136, longitude=-122.424819, address='200 Duboce Ave', categories='Mexican, Fast food', neighborhoods='Mission')
    restaurant_list = RestaurantList(restaurant_id=1, list_id=1)
    fave = Fave(restaurant_id=1, user_id=1)
    db.session.add_all([user, group, restaurant])
    db.session.commit()
    db.session.add_all([user_group, category, fave])
    db.session.commit()
    db.session.add(restaurant_list)
    db.session.commit()


class TestNotLoggedIn(unittest.TestCase):
    """Flask tests to check when session is empty"""

    def setUp(self):
        """To do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = '123'

        connect_to_db(app, "postgresql:///testdb")
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

    def test_log_in_submit(self):
        """tests log in submits with correct password"""

        result = self.client.post("/login",
                                  data={'email': 'user@gmail.com', 'password': 'mypassword'},
                                  follow_redirects=True)
        self.assertIn('My groups:', result.data)
        self.assertNotIn('Log in:', result.data)

    def test_log_in_redirect_to_signup(self):
        """tests that log in redirects to sign up route when no such user"""

        result = self.client.post("/login",
                                  data={'email': 'user2@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn('First Name', result.data)
        self.assertNotIn('Log in:', result.data)

    def test_log_in_fail_on_incorrect_pw(self):
        """tests that login fails on incorrect password"""

        result = self.client.post("/login",
                                  data={'email': 'user@gmail.com', 'password': 'password2'},
                                  follow_redirects=True)
        self.assertIn('Log in:', result.data)
        self.assertNotIn('My groups:', result.data)


class TestSession(unittest.TestCase):
    """Flask tests when user is logged in"""

    def setUp(self):
        """To do before every test"""

        self.client = app.test_client()
        app.config['SECRET_KEY'] = '123'
        app.config['TESTING'] = True

        # connect to test database
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

    def test_homepage_logged_in(self):
        """test to show homepage displays when user is logged in"""

        result = self.client.get("/")
        self.assertIn('My groups:', result.data)
        self.assertNotIn('Log in:', result.data)

if __name__ == "__main__":
    # server.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    unittest.main()
