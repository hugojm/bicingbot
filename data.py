import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
import matplotlib.pyplot as plt
from staticmap import StaticMap, CircleMarker


def data():
    """options = {
        'node_color': 'black',
        'node_size': 10,
        'width': 3,
    }
    """
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(
        pd.read_json(dataset)['data']['stations'],
        index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node(st.Index, pos=(st.lon, st.lat))
        for st2 in bicing.itertuples():
    return G
    # pos = nx.get_node_attributes(G, 'pos')
    # nx.draw(G, pos, **options)
    # plt.savefig("path.png")

def print_map(G):
    distance = input("Distance ")
    m = StaticMap(800, 800)
    for n in list(G.nodes(data=True)):
        marker = CircleMarker(n[1]['pos'], 'red', 4)
        m.add_marker(marker)
    image = m.render()
    image.save('map.png')


def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude,
                location1.longitude), (location2.latitude, location2.longitude)
    except BaseException:
        return None


data()
print_map(data())
