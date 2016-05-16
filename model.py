"""Models and database functions for HB project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

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

    # Defines relationship between groups and users
    groups = db.relationship("Group",
                             secondary="users_groups",
                             backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


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
    __table_args__ = (UniqueConstraint(user_id, group_id),
                      )

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
    restaurant_name = db.Column(db.String(100), nullable=False)
    yelp_rating = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

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
    # attempt at unique constraint across restaurant_id and list_id tables
    __table_args__ = (UniqueConstraint(restaurant_id, list_id),
                      )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RestaurantList restaurant_list_id=%s restaurant_id=%s list_id=%s>" % (self.restaurant_list_id, self.restaurant_id, self.list_id)


class Address(db.Model):
    """Address of restaurants"""

    __tablename__ = "addresses"

    address_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String(150), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))

    restaurants = db.relationship("Restaurant", backref=db.backref("addresses"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Address address_id=%s address=%s>" % (self.address_id, self.address)


class Fave(db.Model):
    """Restaurants favorited by users"""

    __tablename__ = "faves"

    fave_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    __table_args__ = (UniqueConstraint(user_id, restaurant_id),
                      )

    users = db.relationship("User", backref=db.backref("faves"))

    restaurants = db.relationship("Restaurant", backref=db.backref("faves"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Review fave_id=%s restaurant_id=%s user_id=%s>" % (self.fave_id, self.restaurant_id, self.user_id)

##############################################################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    # creates tables in project db
    db.create_all()
