"""Restaurant List App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
# using to hash passwords

from model import connect_to_db, db
# import Classes from model db
from model import User, Group, UserGroup, List, Restaurant, RestaurantList, Fave
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
    """Homepage/Shows user their lists of restaurants"""

    user_id = session.get('user')

    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('dashboard.html', user=user, login=session.get('user'))
    else:
        return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def submit_login():
    """Logs in user or directs to sign up form if no email"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    # if user already exists, checks password and logs them in if correct. If not, prompts
    # for password again
    if user:
        if user.verify_password(password):
            session['user'] = user.user_id
            flash("You are now logged in")
            return redirect('/')
            # return redirect('/users/' + str(user.user_id))
        else:
            flash("Password incorrect")
            return redirect('/')
    else:
        return render_template('sign_up_form.html', email=email, password=password)


@app.route('/signup', methods=['POST'])
def sign_up_user():
    """Signs up new user"""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = User.query.filter_by(email=email).first()
    # if user already exists, checks password and logs them in if correct. If not, prompts
    # for password again
    if user:
        if user.verify_password(password):
            session['user'] = user.user_id
            flash("You are now logged in")
            return redirect('/')
            # return redirect('/users/' + str(user.user_id))
        else:
            flash("Password incorrect - There is already a user with this email")
            return redirect('/')
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


@app.route('/groups/<int:group_id>')
def show_group_details(group_id):
    """Shows group details"""

    user_id = session.get('user')
    user = User.query.filter_by(user_id=user_id).first()
    group = Group.query.filter_by(group_id=group_id).one()

    user_group = UserGroup.query.filter_by(group_id=group_id, user_id=user_id).first()

    return render_template('group_view.html', group=group, user=user, user_group=user_group)


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
    user_group = UserGroup.query.filter_by(user_id=user_id, group_id=list_item.group_id).first()

    return render_template('list_view.html', list=list_item, user=user, user_group=user_group)


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
    address = request.form.get('address')
    categories = request.form.get('categories')
    neighborhoods = request.form.get('neighborhoods')

    # check if restaurant already in db
    get_restaurant = Restaurant.query.filter_by(restaurant_name=restaurant_name, latitude=latitude, longitude=longitude).first()
    if get_restaurant:
        # check if already part of list then add if no
        get_restaurant_list = RestaurantList.query.filter_by(restaurant_id=get_restaurant.restaurant_id, list_id=list_id).first()
        if get_restaurant_list:
            flash("Restaurant is already part of list")
        else:
            new_restaurant_list = RestaurantList(restaurant_id=get_restaurant.restaurant_id, list_id=list_id)
            db.session.add(new_restaurant_list)
            db.session.commit()
    # if restaurant is not already in db, add it and add to RestaurantList
    else:
        new_restaurant = Restaurant(restaurant_name=restaurant_name, yelp_rating=yelp_rating, latitude=latitude, longitude=longitude, address=address, categories=categories, neighborhoods=neighborhoods)
        db.session.add(new_restaurant)
        db.session.commit()
        # need this line because we just added the restaurant to db and need to get the id to add to RestaurantList
        restaurant_info = Restaurant.query.filter_by(restaurant_name=restaurant_name, latitude=latitude, longitude=longitude).first()
        new_restaurant_list = RestaurantList(restaurant_id=restaurant_info.restaurant_id, list_id=list_id)
        db.session.add(new_restaurant_list)
        db.session.commit()

    return jsonify(status='success', id=item_id, restaurant_name=restaurant_name, yelp_rating=yelp_rating, latitude=latitude, longitude=longitude)


@app.route("/delete-restaurant.json", methods=["POST"])
def delete_restaurant():
    """Allows user to remove restaurant from list"""

    restaurant_id = request.form.get('restaurant_id')
    list_id = request.form.get('list_id')
    restaurant = Restaurant.query.get(restaurant_id)

    restaurant_list = RestaurantList.query.filter_by(restaurant_id=restaurant_id, list_id=list_id).first()
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
    return jsonify(result='success')


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


@app.route("/star-restaurant.json", methods=["POST"])
def add_restaurant_to_faves():
    """Adds a restaurant to a user's favorites list"""

    restaurant_id = request.form.get('rest_id')
    user_id = session.get('user')

    get_fave_restaurant = Fave.query.filter_by(restaurant_id=restaurant_id, user_id=user_id).first()

    if get_fave_restaurant:
        pass
    else:
        fave_restaurant = Fave(restaurant_id=restaurant_id, user_id=user_id)
        db.session.add(fave_restaurant)
        db.session.commit()

    return jsonify(result="success", id=restaurant_id)


@app.route("/my-faves")
def show_favorites():
    """Shows list of user's favorited restaurant"""

    user_id = session.get("user")

    faves = Fave.query.filter_by(user_id=user_id).all()

    return render_template("my_faves.html", faves=faves, login=session.get('user'))


@app.route("/return-restaurants.json", methods=['POST'])
def return_restaurants():
    """Gives response to browser of restaurants in db for given list"""

    list_id = request.form.get('list_id')
    item_id = request.form.get('id')
    restaurants_lists = RestaurantList.query.filter_by(list_id=list_id).all()

    restaurants = []
    for item in restaurants_lists:
        restaurant = Restaurant.query.filter_by(restaurant_id=item.restaurant_id).first()

        restaurants.append({'restaurant_name': restaurant.restaurant_name,
                            'yelp_rating': restaurant.yelp_rating,
                            'latitude': restaurant.latitude,
                            'longitude': restaurant.longitude,
                            'restaurant_id': restaurant.restaurant_id})

    print restaurants
    return jsonify(status="success", results=restaurants, id=item_id)


##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
