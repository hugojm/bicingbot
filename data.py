import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim


def data():
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(pd.read_json(dataset)['data']['stations'], index='station_id')
    print(bicing)

def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

data()
