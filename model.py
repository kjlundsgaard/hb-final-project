"""Models and database functions for HB project."""

from flask_sqlalchemy import SQLAlchemy
# from flask.ext.bcrypt import Bcrypt
import bcrypt
import os

# from sqlalchemy.schema import UniqueConstraint

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    salt = db.Column(db.String(50), nullable=True)

    # Defines relationship between groups and users
    groups = db.relationship("Group",
                             secondary="users_groups",
                             backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name = %s email=%s>" % (self.user_id, self.fname, self.email)

    def __init__(self, email, password, fname, lname):
        """initializer"""

        self.salt = bcrypt.gensalt()
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.fname = fname
        self.lname = lname


    def verify_password(self, password):
        """verifies user's password"""

        # return self.bcrypt.check_password_hash(secret)
        return self.password == bcrypt.hashpw(password.encode('utf-8'), self.salt.encode('utf-8'))




class Group(db.Model):
    """Group of website."""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Group group_id=%s group_name=%s>" % (self.group_id, self.group_name)


class UserGroup(db.Model):
    """Association table between users and groups"""

    __tablename__ = "users_groups"

    user_group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    # attempt at unique constraint across restaurant_id and list_id tables
    # __table_args__ = (UniqueConstraint(user_id, group_id),
                      # )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserGroup user_group_id=%s group_id=%s user_id=%s>" % (self.user_group_id, self.group_id, self.user_id)


class List(db.Model):
    """List of restaurants"""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    list_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<List list_id=%s list_name=%s>" % (self.list_id, self.list_name)

    group = db.relationship("Group", backref=db.backref("lists"))


class Restaurant(db.Model):
    """Restaurants"""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=True)
    yelp_rating = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    categories = db.Column(db.String(100), nullable=True)
    neighborhoods = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant restaurant_id=%s restaurant_name=%s yelp_rating=%s>" % (self.restaurant_id, self.restaurant_name, self.yelp_rating)

    lists = db.relationship("List",
                            secondary="restaurants_lists",
                            backref="restaurants")


class RestaurantList(db.Model):
    """Association table between restaurants and lists"""

    __tablename__ = "restaurants_lists"

    restaurant_list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    visited = db.Column(db.Boolean, unique=False, default=False)
    restaurant = db.relationship("Restaurant", backref="restaurants_lists", uselist=False)
    list_table = db.relationship("List", backref="restaurants_lists", uselist=False)

    # attempt at unique constraint across restaurant_id and list_id tables
    # __table_args__ = (UniqueConstraint(restaurant_id, list_id),
                      # )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RestaurantList restaurant_list_id=%s restaurant_id=%s list_id=%s visited=%s>" % (self.restaurant_list_id, self.restaurant_id, self.list_id, self.visited)


class Fave(db.Model):
    """Restaurants favorited by users"""

    __tablename__ = "faves"

    fave_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # __table_args__ = (UniqueConstraint(user_id, restaurant_id),
                      # )

    users = db.relationship("User", backref=db.backref("faves"))

    restaurants = db.relationship("Restaurant", backref=db.backref("faves"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review fave_id=%s restaurant_id=%s user_id=%s>" % (self.fave_id, self.restaurant_id, self.user_id)

##############################################################################


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///gastrohub'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    print "Connected to DB."
    # creates tables in project db
    db.create_all()
