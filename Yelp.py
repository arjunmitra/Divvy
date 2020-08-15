import os
from typing import Dict
# GraphQL library
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
class Yelp:
    api_key = os.environ['YELP']

    # Specifies authorization
    header = {
        'Authorization': 'bearer {}'.format(api_key),
        'Content-Type': "application/json"
    }

    # Specifies endpoint
    transport = RequestsHTTPTransport(
        url = 'https://api.yelp.com/v3/graphql',
        headers = header,
        use_json = True,
        retries = 2
    )

    client = Client(
        transport = transport,
        fetch_schema_from_transport = True
    )

    # Returns dictionary of required information about restaurant
    @staticmethod
    def search(restaurant_name : str) -> Dict:
        # Search radius restricted to 10 miles
        query = gql("""
            {
                search(term: "%s", limit: 1, latitude: 34.020176, longitude: -118.285550, radius: 16093, sort_by: "distance") {
                    business {
                        name
                        url
                        categories {
                            title
                        }
                        coordinates {
                            latitude
                            longitude
                        }
                    }
                }
            }
            """ % restaurant_name)

        # Sends HTTP request
        response : Dict = Yelp.client.execute(query)
        response = response['search']['business'][0]
        search_result : Dict = dict()
        # Name of business
        search_result['Name'] = response['name']
        # URL for business page on Yelp
        search_result['URL'] = response['url']
        search_result['Coordinates'] = {
            'Latitude' : response['coordinates']['latitude'],
            'Longitude' : response['coordinates']['longitude']
        }
        # Transforms dict of category titles into list of categories
        search_result['Categories'] = [category['title'] for category in response['categories']]
        return search_result