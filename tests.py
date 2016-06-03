import unittest
from server import app
from model import db, connect_to_db, User, Group, List, UserGroup, Restaurant, RestaurantList, Fave
import yelp
import uber


def example_data():
    """Create example data for the test database."""
    # password = bcrypt.generate_password_hash('mypassword')

    user = User(email='user@gmail.com', password='password', fname='First', lname='Last')
    user2 = User(email='newuser@gmail.com', password='password', fname='Otherfirst', lname='Otherlast')
    group = Group(group_name='Buds')
    group2 = Group(group_name='Enemies')
    user_group = UserGroup(user_id=1, group_id=1)
    user_group2 = UserGroup(user_id=2, group_id=2)
    category = List(list_name='Dinner', group_id=1)
    category2 = List(list_name='Lunch', group_id=2)
    restaurant = Restaurant(restaurant_name='Taco Bell', yelp_rating=2.5, latitude=37.774136, longitude=-122.424819, address='200 Duboce Ave', categories='Mexican, Fast food', neighborhoods='Mission')
    restaurant2 = Restaurant(restaurant_name='La Taqueria', yelp_rating=5, latitude=37.750977, longitude=-122.418073, address='24th and Mission', categories='Mexican, Burrito', neighborhoods='Mission')
    restaurant_list = RestaurantList(restaurant_id=1, list_id=1)
    restaurant_list2 = RestaurantList(restaurant_id=2, list_id=1, visited=True)
    fave = Fave(restaurant_id=1, user_id=1)
    db.session.add_all([user, group, restaurant, restaurant2, user2, group2])
    db.session.commit()
    db.session.add_all([user_group, user_group2, category, category2, fave])
    db.session.commit()
    db.session.add(restaurant_list, restaurant_list2)
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
        self.assertNotIn('Dashboard', result.data)

    def test_log_in_submit(self):
        """tests log in submits with correct password"""

        result = self.client.post("/login",
                                  data={'email': 'user@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn('Your groups:', result.data)
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
        self.assertIn('Your groups:', result.data)
        self.assertNotIn('Log in:', result.data)

    def test_sign_up_user_in_db(self):
        """test sign up submit with user already in db"""

        result = self.client.post("/signup",
                                  data={'email': 'user@gmail.com', 'password': 'password', 'fname': 'IncorrectFirst', 'lname': 'IncorrectLast'},
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
        """tests log out route"""

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn('Log in:', result.data)
        self.assertNotIn('First', result.data)

    def test_list_view_not_available(self):
        """tests list view is not available without session"""

        result = self.client.get("/lists/1")
        self.assertIn('You are not a member of this group', result.data)
        self.assertNotIn('Dinner', result.data)


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
        self.assertIn('Your groups:', result.data)
        self.assertIn('Buds', result.data)
        self.assertNotIn('Log in:', result.data)

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

    def test_create_new_group(self):
        """tests creation of new group"""

        result = self.client.post('/new-group',
                                  data={'group': 'Acquaintences'},
                                  follow_redirects=True)
        self.assertIn('Acquaintences', result.data)
        self.assertNotIn('You are not a member of this group', result.data)

    def test_create_new_list(self):
        """tests creation of new list"""

        result = self.client.post('/new-list',
                                  data={'list': 'Brunch', 'group_id': 1},
                                  follow_redirects=True)
        self.assertIn('Brunch', result.data)
        self.assertNotIn('You are not a member of this group', result.data)
        self.assertNotIn('Log in:', result.data)

    def test_list_view(self):
        """tests to show logged in user can see their list"""

        result = self.client.get('/lists/1')
        self.assertIn('Dinner', result.data)
        self.assertNotIn('You are not a member', result.data)

    def test_list_view_non_member(self):
        """tests to show user cannot see list view for this list"""

        result = self.client.get('/lists/2')
        self.assertIn('You are not', result.data)
        self.assertNotIn('Lunch', result.data)

    def test_add_restaurant(self):
        """tests to show adding restaurant"""

        result = self.client.post('/add-restaurant.json',
                                  data={'item_id': 5,
                                        'restaurant_name': 'Eddys',
                                        'yelp_rating': 4,
                                        'latitude': 0,
                                        'longitude': 0,
                                        'list_id': 2,
                                        'address': '123 Divisadero',
                                        'categories': 'Breakfast,breakfast',
                                        'neighborhoods': 'Haight',
                                        'link': 'yelp.com'})
        self.assertEqual(result.status_code, 200)

    def test_delete_restaurant(self):
        """tests delete restaurant"""

        result = self.client.post('/delete-restaurant.json',
                                  data={'restaurant_id': 1,
                                        'list_id': 1})

        self.assertEqual(result.status_code, 200)

    def test_delete_category(self):
        """tests delete category"""

        result = self.client.post('/delete-list.json',
                                  data={'list_id': 1})

        self.assertEqual(result.status_code, 200)

    def test_leave_group(self):
        """tests user leaving group"""

        result = self.client.post('/leave-group',
                                  data={'group_id': 1})

        self.assertEqual(result.status_code, 200)

    def test_like_restaurant(self):
        """tests user liking restaurant"""

        result = self.client.post('/star-restaurant.json',
                                  data={'restaurant_id': 1})

        self.assertEqual(result.status_code, 200)

    def test_mark_visited(self):
        """tests marking restaurant as visited"""

        result = self.client.post('/mark-visited.json',
                                  data={'rest_id': 1,
                                        'list_id': 1})
        self.assertEqual(result.status_code, 200)

    def test_return_categories(self):
        """tests that categories are returned for chart.js"""

        result = self.client.get('/categories.json')
        self.assertEqual(result.status_code, 200)


class TestAPI(unittest.TestCase):
    """Flask tests using API response"""

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

    def _mock_search_restaurant(location, term):
        """mock yelp API results"""
        return [{'name': 'El Farolito',
                 'rating': 4.0,
                 'latitude': 37.774136,
                 'longitude': -122.424819,
                 'categories': ['Restaurant', 'restaurant'],
                 'neighborhoods': ['Mission'],
                 'address': ['2222 Mission Street'],
                 'url': 'yelp.com'}]

    yelp.get_results = _mock_search_restaurant

    def _mock_uber_results(start_lat, start_lng, end_lat, end_lng):
        """mock uber API results"""
        return [{'prices': {'car': 'uberx',
                            'price_estimate': 6,
                            'distance': 5,
                            'duration': 3}}]

    def tearDown(self):
        """To do at end of test"""

        db.session.close()
        db.drop_all()

    def test_yelp_search(self):
        """tests route using yelp API"""

        result = self.client.post('/search-restaurant.json',
                                  {'location': 'San Francisco',
                                   'term': 'burrito'})

        self.assertEqual(result.status_code, 200)

    def test_uber_results(self):
        """tests route using uber API"""

        result = self.client.post('/get-uber-data.json',
                                  {'start_latitude': 0,
                                   'start_longitude': 0,
                                   'end_latitude': 0,
                                   'end_longitude': 0})

        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    # server.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
    unittest.main()
