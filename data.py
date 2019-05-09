import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
import matplotlib.pyplot as plt
from staticmap import StaticMap, CircleMarker, Line


def data():
    distance = float(input("Distance "))
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
    pos=nx.get_node_attributes(G,'pos')
    for nod in G.nodes():
        for nod2 in G.nodes():
            coord1 = (pos[nod][1],pos[nod][0])
            coord2 = (pos[nod2][1],pos[nod2][0])
            if (haversine(coord1,coord2) <= distance):
                G.add_edge(nod,nod2)

    return G
    # pos = nx.get_node_attributes(G, 'pos')
    # nx.draw(G, pos, **options)
    # plt.savefig("path.png")

def print_map(G):
    m = StaticMap(800, 800)
    for n in G.nodes():
        pos=nx.get_node_attributes(G,'pos')
        marker = CircleMarker(pos[n], 'red', 6)
        m.add_marker(marker)
    for n2 in G.edges():
        pos=nx.get_node_attributes(G,'pos')
        coordinates = [pos[n2[0]],pos[n2[1]]]
        line = Line(coordinates, 'blue', 1)
        m.add_line(line)
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

def shortest_path(G):
    print(nx.shortest_path(G, source=0, target=4))



print_map(data())
