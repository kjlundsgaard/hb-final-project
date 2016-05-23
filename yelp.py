from yelpapi import YelpAPI
import os

yelp_api = YelpAPI(
    consumer_key=os.environ['yelp_consumer_key'],
    consumer_secret=os.environ['yelp_consumer_secret'],
    token=os.environ['yelp_token'],
    token_secret=os.environ['yelp_token_secret']
)


def get_results(location, term):
    resp = yelp_api.search_query(location=location, term=term, limit=20)

    # create list of results to store result objects
    results = []

    for restaurant in resp['businesses']:
        if restaurant['location'].get('neighborhoods'):
            results.append({'name': restaurant['name'],
                            'rating': restaurant['rating'],
                            'latitude': restaurant['location']['coordinate']['latitude'],
                            'longitude': restaurant['location']['coordinate']['longitude'],
                            'categories': restaurant['categories'],
                            'neighborhoods': restaurant['location']['neighborhoods'],
                            'address': restaurant['location']['address'],
                            'image': restaurant['image_url']})

        else:
            results.append({'name': restaurant['name'],
                            'rating': restaurant['rating'],
                            'latitude': restaurant['location']['coordinate']['latitude'],
                            'longitude': restaurant['location']['coordinate']['longitude'],
                            'categories': restaurant['categories'],
                            'neighborhoods': None,
                            'address': restaurant['location']['address'],
                            'image': restaurant['image_url']})
    # print results
    return results

# get_results("chicago", "food")
