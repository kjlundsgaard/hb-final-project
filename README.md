# GastroHub

GastroHub allows users to create groups of friends with whom they would like to share lists of local establishments they'd like to visit. Users can invite other users to their groups, create lists and add restaurants to their lists using the Yelp API. They can view their restaurants on a map, see Uber price estimates from their current location, and mark the restaurants as visited and liked. On the dashboard, users can view their restaurant statistics.

## Table of Contents
  * [Tech Stack](#tech-stack)
  * [APIs](#apis)
  * [Features](#features)
  * [How to Run](#how-to-run)

### Tech Stack <a id="tech-stack"></a>

* PostgreSQL
* SQLAlchemy
* Python
* Flask
* Jinja
* JavaScript
* AJAX
* JQuery
* Bootstrap

### APIs <a id="apis"></a>

* Yelp
* Google Maps
* Uber

### Features <a id="features"></a>

* Login/Logout
* Create and leave groups
* Invite other users to groups
* Create and delete lists/categories
* Search for restaurants using Yelp API
* Add and remove restaurants to lists
* Mark restaurants as visited
* Mark restaurants as liked
* View restaurants on map
* View statistics of restaurant categories and number of restaurants visited
* Get Uber price estimates to restaurant for current location

### How to Run <a id="how-to-run"></a>

1. [Obtain Yelp access token](https://www.yelp.com/developers/manage_api_keys)
2. [Obtain Uber access token](https://developer.uber.com/docs/getting-started)
3. Store tokens in secrets.sh file as     

    ```|export yelp_consumer_key="YELP_CONSUMER_KEY" 
    |export yelp_consumer_secret="YELP_CONSUMER_SECRET"
    |export yelp_token="YELP_TOKEN"
    |export yelp_token_secret="YELP_TOKEN_SECRET"
    |export uber_client_id="UBER_CLIENT_ID"
    |export uber_client_secret="UBER_CLIENT_SECRET"
    |export uber_server_token="UBER_SERVER_TOKEN"```

4. Create a virtual environment
    >`virtualenv env`
    >`source env/bin/activate`

5. `pip install -r requirements.txt`

6. `source secrets.sh`

7. With PostgreSQL running, create database with name gastrohub
    `createdb gastrohub`

8. Run model.py
    `python model.py`

9. Run server.py
    `python server.py`

10. Visit `http://localhost:5000/`


