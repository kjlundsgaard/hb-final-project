"""Restaurant List App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
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


@app.route('/login', methods=['POST'])
def submit_login():
    """Signs user in or creates new user based on form input"""

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
            return redirect('/dashboard')
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
        return redirect('/dashboard')


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

    user = User.query.filter_by(user_id=user_id).first()

    if user_id:
        return render_template('dashboard.html', user=user, login=session.get('user'))
    else:
        return render_template('login_form.html')


@app.route('/groups/<int:group_id>')
def show_group_details(group_id):
    """Shows group details"""

    user_id = session.get('user')
    user = User.query.filter_by(user_id=user_id).first()
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

    return redirect('/lists/' + str(new_list.list_id))


@app.route('/lists/<int:list_id>')
def show_list_details(list_id):
    """Shows list details"""

    user_id = session.get('user')
    user = User.query.filter_by(user_id=user_id).one()
    list_item = List.query.filter_by(list_id=list_id).one()

    return render_template('list_view.html', list=list_item, user=user, login=session.get('user'))


@app.route('/search-restaurant.json', methods=['POST'])
def search_restaurant():
    """Allows user to search restaurant based on location and food term"""

    location = request.form.get('location')
    term = request.form.get('term')

    results = yelp.get_results(location=location, term=term)
    return jsonify(results=results)


@app.route('/add-restaurant.json', methods=['POST'])
def add_restaurant():
    """Allows user to add restaurant to a list"""

    item_id = request.form.get('id')
    restaurant_name = request.form.get('restaurant_name')
    yelp_rating = request.form.get('yelp_rating')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    list_id = request.form.get('list_id')

    # check if restaurant already in db
    get_restaurant = Restaurant.query.filter_by(restaurant_name=restaurant_name, latitude=latitude, longitude=longitude).first()
    if get_restaurant:
        # check if already part of list then add if no
        get_restaurant_list = RestaurantList.query.filter_by(restaurant_id=get_restaurant.restaurant_id, list_id=list_id)
        if get_restaurant_list:
            flash("Restaurant is already part of list")
        else:
            new_restaurant_list = RestaurantList(restaurant_id=get_restaurant.restaurant_id, list_id=list_id)
            db.session.add(new_restaurant_list)
            db.session.commit()
            flash("Added restaurant " + get_restaurant.restaurant_name + " to list")
    # if restaurant is not already in db, add it and add to RestaurantList
    else:
        new_restaurant = Restaurant(restaurant_name=restaurant_name, yelp_rating=yelp_rating, latitude=latitude, longitude=longitude)
        db.session.add(new_restaurant)
        db.session.commit()
        # need this line because we just added the restaurant to db and need to get the id to add to RestaurantList
        restaurant_info = Restaurant.query.filter_by(restaurant_name=restaurant_name, latitude=latitude, longitude=longitude).first()
        new_restaurant_list = RestaurantList(restaurant_id=restaurant_info.restaurant_id, list_id=list_id)
        db.session.add(new_restaurant_list)
        db.session.commit()
        flash("Added restaurant " + restaurant_name + " to list")

    return jsonify(status='success', id=item_id)


@app.route("/delete-restaurant.json", methods=["POST"])
def delete_restaurant():
    """Allows user to remove restaurant from list"""

    restaurant_id = request.form.get('restaurant_id')
    list_id = request.form.get('list_id')
    restaurant = Restaurant.query.get(restaurant_id)
    print restaurant

    restaurant_list = RestaurantList.query.filter_by(restaurant_id=restaurant_id, list_id=list_id).first()
    print restaurant_list
    db.session.delete(restaurant_list)
    db.session.commit()

    flash("Removed " + restaurant.restaurant_name)
    return jsonify(status='success')


@app.route("/delete-list.json", methods=["POST"])
def delete_list():
    """Allows user to remove a list from a group"""

    list_id = request.form.get('list_id')

    list_item = List.query.get(list_id)

    db.session.delete(list_item)
    db.session.commit()

    flash("Removed " + list_item.list_name)
    return jsonify(status="success")


# TODO CREATE LEAVE GROUP OPTION FOR A USER TO LEAVE A GROUP

@app.route("/leave-group", methods=["POST"])
def leave_group():
    """Allows a user to leave a group"""

    group_id = request.form.get('group_id')
    user_id = session.get('user')

    get_user_group = UserGroup.query.filter_by(group_id=group_id, user_id=user_id).first()

    db.session.delete(get_user_group)
    db.session.commit()

    flash("You have left the group")
    return jsonify(result="success")


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
