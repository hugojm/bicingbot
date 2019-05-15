import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line
from geopy.geocoders import Nominatim
<<<<<<< HEAD
>>>>>>> 6f577e92e6689109f718216196f33fac46e28c6a

=======
>>>>>>> b4a69f286fc214aff078fb6aef3a5f5dfa5627a2

def Graph(distance=1000):
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(
        pd.read_json(dataset)['data']['stations'],
        index='station_id')
    G = nx.Graph()
    # add coordinates as nodes of the graph
    for st in bicing.itertuples():
        G.add_node((st.lon, st.lat))
    for nod in G.nodes():
        for nod2 in G.nodes():
            # first latitude and then longitude to calculate haversine
            coord1 = (nod[1], nod[0])
            coord2 = (nod2[1], nod2[0])
            if (haversine(coord1, coord2) <= float(distance / 1000)
                    and haversine(coord1, coord2) != 0):
                G.add_edge(
                    nod, nod2, weight=float(
                        haversine(
                            coord1, coord2) / 10))
    return G


def print_map(G):
    m = StaticMap(800, 800)
    # print nodes on the map
    for n in G.nodes():
        marker = CircleMarker(n, 'red', 6)
        m.add_marker(marker)
    # print edges on the map
    for n2 in G.edges(data=True):
        coordinates = [n2[0], n2[1]]
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
        return (location1.longitude,
                location1.latitude), (location2.longitude, location2.latitude)
    except BaseException:
        return None


def print_path(path, G):
    m = StaticMap(800, 800)
    # print nodes on the map
    for n in G.nodes():
        marker = CircleMarker(n, 'red', 6)
        m.add_marker(marker)
    for i in range(len(path) - 1):
        coordinates = [path[i], path[i + 1]]
        line = Line(coordinates, 'blue', 1)
        m.add_line(line)
    image = m.render()
    image.save('path.png')

def time(G, coord1, coord2):
    time = nx.dijkstra_path_length(G, coord1, coord2, weight='weight')
    return time


def route(G, cami):
    coord1, coord2 = addressesTOcoordinates(cami)
    found1 = False
    found2 = False
    for nod in G.nodes():
        if nod == coord1:
            found1 = True
        if nod == coord2:
            found2 = True
        if (found1 and found2):
            break
    if (not found1):
        G.add_node(coord1)
        for nod2 in G.nodes():
            inv = (coord1[1], coord1[0])
            inv2 = (nod2[1], nod2[0])
            G.add_edge(coord1, nod2, weight=float(haversine(inv, inv2) / 4))

    if (not found2):
        G.add_node(coord2)
        for nod2 in G.nodes():
            inv = (coord2[1], coord2[0])
            inv2 = (nod2[1], nod2[0])
            G.add_edge(coord2, nod2, weight=float(haversine(inv, inv2) / 4))
    path = nx.dijkstra_path(G, coord1, coord2, weight='weight')
    print_path(path, G)
    t = time(G,coord1,coord2)
    if (not found1): G.remove_node(coord1)
    if (not found2): G.remove_node(coord2)
    return t


def components(G):
    return nx.number_connected_components(G)


def Nodes(G):
    return G.number_of_nodes()


def Edges(G):
    return G.number_of_edges()

def authors():
    authors = "Hugo Jiménez (hugo.jimenez@est.fib.upc.edu) and Jaume Martínez (jaume.martinez.ara@est.fib.upc.edu)"
    return authors
