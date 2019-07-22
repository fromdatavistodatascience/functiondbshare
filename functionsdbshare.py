def codedbshare():
    import json
    import requests

    # Load secrets from credentials.json
    url = 'https://api.foursquare.com/v2/venues/explore'
    with open('.secrets/credentials.json') as f:
        params = json.load(f)

    params['v'] = '20180323' #versioned
    params['ll'] = '47.608,-122.336', #latitue and longitude
    params['query'] = 'yoga',
    params['intent'] = 'browse',
    params['radius'] = 100000,
    params['limit'] = 100

    response = requests.get(url=url, params=params)
    data = json.loads(response.text)

    results = data['response']['groups'][0]['items']

    def get_names(result):
        return result['venue']['name']

    def get_address(result):
        return result['venue']['location'].get('address') 
    #.get('address') if it can't find an address becuase there is no value, .get will will return it as a none
    #['address'] will return an error

    import pandas as pd
    pd.DataFrame({'name': get_names(result),
                'address': get_address(result)}
                for result in results)

    venues = [
        {'name': get_names(result), 'address': get_address(result)}
        for result in results]

    import os
    home = os.environ['HOME']

    filename = f'{home}/.secret/mongoDBcollab'
    with open(filename, 'r') as f:
        mongoDBcollab = f.read().strip()

    import pymongo
    mc = pymongo.MongoClient(mongoDBcollab)
    db = mc['foursquare']
    coll = db['Yoga']

    coll.insert_many(venues)

    found_venues = list(coll.find())

    venues_df = pd.DataFrame(venues)

    return '🐄'