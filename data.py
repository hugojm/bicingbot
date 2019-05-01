import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt


def data():
    options = {
        'node_color': 'black',
        'node_size': 10,
        'width': 3,
     }

    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(pd.read_json(dataset)['data']['stations'], index='station_id')
    print(bicing)
    G = nx.Graph()
    for st in bicing.itertuples():
        cord1 = (st.lat , st.lon)
        G.add_node(st.Index, pos=(-st.lat, -st.lon))
        pos=nx.get_node_attributes(G,'pos')

    nx.draw(G,pos,**options)
    plt.savefig("path.png")


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
