import unittest
from server import app, bcrypt
from model import db, connect_to_db, User, Group, List, UserGroup, Restaurant, RestaurantList, Fave


def example_data():
    """Create example data for the test database."""
    password = bcrypt.generate_password_hash('mypassword')

    user = User(email='user@gmail.com', password=password, fname='First', lname='Last')
    user2 = User(email='newuser@gmail.com', password=password, fname='Otherfirst', lname='Otherlast')
    group = Group(group_name='Buds')
    group2 = Group(group_name='Enemies')
    user_group = UserGroup(user_id=1, group_id=1)
    user_group2 = UserGroup(user_id=2, group_id=2)
    category = List(list_name='Dinner', group_id=1)
    restaurant = Restaurant(restaurant_name='Taco Bell', yelp_rating=2.5, latitude=37.774136, longitude=-122.424819, address='200 Duboce Ave', categories='Mexican, Fast food', neighborhoods='Mission')
    restaurant_list = RestaurantList(restaurant_id=1, list_id=1)
    fave = Fave(restaurant_id=1, user_id=1)
    db.session.add_all([user, group, restaurant, user2, group2])
    db.session.commit()
    db.session.add_all([user_group, user_group2, category, fave])
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

    def test_sign_up_submit_no_such_user(self):
        """tests sign up form submission"""

        result = self.client.post("/signup",
                                  data={'email': 'user2@gmail.com', 'password': 'password2', 'fname': 'User', 'lname': 'User'},
                                  follow_redirects=True)
        self.assertIn('My groups:', result.data)
        self.assertNotIn('Log in:', result.data)

    def test_sign_up_user_in_db(self):
        """test sign up submit with user already in db"""

        result = self.client.post("/signup",
                                  data={'email': 'user@gmail.com', 'password': 'mypassword', 'fname': 'IncorrectFirst', 'lname': 'IncorrectLast'},
                                  follow_redirects=True)
        self.assertIn('First', result.data)
        self.assertNotIn('IncorrectFirst', result.data)

    def test_sign_up_user_in_db_incorrect_pw(self):
        """tests sign up with preexisting email and incorrect pw"""

        result = self.client.post("/signup",
                                  data={'email': 'user@gmail.com', 'password': 'wrongpassword', 'fname': 'IncorrectFirst', 'lname': 'IncorrectLast'},
                                  follow_redirects=True)
        self.assertIn('Log in:', result.data)
        self.assertNotIn('First', result.data)

    def test_log_out(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn('Log in:', result.data)
        self.assertNotIn('First', result.data)

    def test_group_view_not_available(self):
        result = self.client.get("/groups/1")
        self.assertIn('You are not a member of this group', result.data)
        self.assertNotIn('Friends', result.data)


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

    def test_group_view(self):
        """test to show user's groups"""

        result = self.client.get("/groups/1")
        self.assertIn('Buds', result.data)
        self.assertNotIn('You are not a member of this group', result.data)

    def test_group_view_non_member(self):
        """test to show logged in user cannot see group details of group they're not in"""

        result = self.client.get("groups/2")
        self.assertNotIn('Enemies', result.data)
        self.assertIn('You are not a member of this group', result.data)

    def test_group_invite_existing_user(self):
        """testing user invite to group"""

        result = self.client.post("/invite",
                                  data={'invite': 'newuser@gmail.com', 'group_id': '1'},
                                  follow_redirects=True)

        self.assertIn('Added', result.data)
        self.assertNotIn('No such', result.data)

    def test_group_invite_nonexisting_user(self):
        """testing user invite to group with nonexistant user"""

        result = self.client.post("/invite",
                                  data={'invite': 'nosuchuser@gmail.com', 'group_id': '1'},
                                  follow_redirects=True)

        self.assertIn('No such', result.data)
        self.assertNotIn('Added', result.data)

    def test_group_invite_user_already_in_group(self):
        """tests invite when user is already member of group"""

        result = self.client.post("/invite",
                                  data={'invite': 'user@gmail.com', 'group_id': '1'},
                                  follow_redirects=True)

        self.assertIn('User is already', result.data)
        self.assertNotIn('Added', result.data)
        self.assertNotIn('No such', result.data)



if __name__ == "__main__":
    # server.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    unittest.main()
