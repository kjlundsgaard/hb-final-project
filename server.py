"""Restaurant List App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
# import Classes from model db
from model import User, Group, UserGroup, List, Restaurant, RestaurantList, Address, Review
# gets access to yelp.py file
import yelp

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "supersecretkey"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('index.html', login=session.get('user'))


@app.route('/login')
def login():
    """Prompts user for login info"""

    return render_template('login_form.html', login=session.get('user'))


@app.route('/login', methods=['POST'])
def submit_login():

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = User.query.filter_by(email=email).first()
    # if user already exists, checks password and logs them in if correct. If not, prompts
    # for password again
    if user:
        if user.password == password:
            session['user'] = user.user_id
            flash("You are now logged in")
            return redirect('/')
            # return redirect('/users/' + str(user.user_id))
        else:
            flash("Password incorrect")
            return redirect('/login')
    else:
        #instantiates new user and passes user_id to session
        user = User(email=email, password=password, fname=fname, lname=lname)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.user_id
        flash("Your account has been created")
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out"""

    session['user'] = None

    flash("You are now logged out")

    return redirect('/')


@app.route('/dashboard')
def show_lists():
    """Shows user their lists of restaurants"""

    user_id = session.get('user')

    user = User.query.filter_by(user_id=user_id).one()

    return render_template('dashboard.html', user=user, login=session.get('user'))


@app.route('/groups/<int:group_id>')
def show_group_details(group_id):
    """Shows group details"""

    user_id = session.get('user')
    user = User.query.filter_by(user_id=user_id).one()
    group = Group.query.filter_by(group_id=group_id).one()

    return render_template('group_view.html', group=group, user=user, login=session.get('user'))


@app.route('/invite', methods=["POST"])
def invite_user():
    """Allows user to invite other member to group by email"""

    email = request.form.get('invite')
    user = User.query.filter_by(email=email).first()
    group_id = request.form.get('group_id')

    if user:
        user_search = UserGroup.query.filter_by(user_id=user.user_id, group_id=group_id).first()
        if user_search:
            flash("User is already in this group")
        else:
            new_user = UserGroup(user_id=user.user_id, group_id=group_id)
            db.session.add(new_user)
            db.session.commit()
            flash("Added new user " + email + " to group")
    else:
        flash("No such user")

    return redirect('/groups/' + group_id)


# TODO
# add group/individual list
@app.route('/new-group', methods=["POST"])
def add_new_group():
    """Allows user to create a new group"""

    group_name = request.form.get('group')
    user_id = session.get('user')

    new_group = Group(group_name=group_name)
    db.session.add(new_group)
    db.session.commit()

    new_user_group = UserGroup(group_id=new_group.group_id, user_id=user_id)
    db.session.add(new_user_group)
    db.session.commit()

    return redirect('/groups/' + str(new_group.group_id))


@app.route('/new-list', methods=["POST"])
def add_new_list():
    """Allows user to add a new list"""

    list_name = request.form.get('list')
    group_id = request.form.get('group_id')

    new_list = List(list_name=list_name, group_id=group_id)
    db.session.add(new_list)
    db.session.commit()

    return redirect('/groups/' + group_id)


# TO DO TODO TODO FIXME FIX ME
@app.route('/search-restaurant', methods=['POST'])
def search_restaurant():
    """Allows user to search restaurant based on location and food term"""
    # presumably getting these from a form where users can input location and search terms
    location = request.form.get('location')
    term = request.form.get('term')

    results = yelp.get_results(location=location, term=term)
    # this is probably not right??? need to figure out what response in yelp.py file looks like
    return jsonify(results)

    # handle yelp results

    # render results on page

# TODO
# ability to search yelp and add restaurants to lists


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
