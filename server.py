"""Restaurant List App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
# import Classes from model db
from model import User, Group, UserGroup, List, Restaurant, RestaurantList, Address, Review

# if I want to keep db functions in a separate file, could use this?
import seed

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

    username = request.form.get("username")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = User.query.filter_by(email=username).first()
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
        user = User(email=username, password=password, fname=fname, lname=lname)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.user_id
        flash("Your account has been created")
        return redirect('/')

@app.route('/logout')
def logout():
    """Logs user out"""

    session['user'] = None

    flash ("You are now logged out")

    return redirect('/')



##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
