import requests
import os
# import pprint
import json

client_id = os.environ['uber_client_id']
server_token = os.environ['uber_server_token']


def get_uber_price_results(start_lat, start_lng, end_lat, end_lng):
    request_url = 'https://api.uber.com/v1/estimates/price'
    payload = {'start_latitude': start_lat,
               'start_longitude': start_lng,
               'end_latitude': end_lat,
               'end_longitude': end_lng}
    headers = {'Authorization': "Token " + server_token}

    r = requests.get(request_url, params=payload, headers=headers)
    resp = json.loads(r.text)

    price_results = []
    for item in resp['prices']:
        price_results.append({'car': item['localized_display_name'],
                              'price_estimate': item['estimate'],
                              'distance': item['distance'],
                              'duration': int(item['duration']) / 60})

    # print price_results
    return price_results

# get_uber_price_results(37.788699699999995, -122.4115356, 37.750977, -122.418073)
