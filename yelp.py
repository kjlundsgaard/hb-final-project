from yelpapi import YelpAPI
import os
from pprint import pprint


yelp_api = YelpAPI(
    consumer_key=os.environ['yelp_consumer_key'],
    consumer_secret=os.environ['yelp_consumer_secret'],
    token=os.environ['yelp_token'],
    token_secret=os.environ['yelp_token_secret']
)


def get_results(location, term):
    search_results = yelp_api.search_query(location=location, term=term, limit=10)

    pprint(search_results)


get_results("New York, NY", "pizza")
