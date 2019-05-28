import pandas as pd
import networkx as nx
import itertools as it
from pandas import DataFrame
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line
from geopy.geocoders import Nominatim
from IPython.display import display
from PIL import Image

def Graph(distance=1000):
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(
        pd.read_json(dataset)['data']['stations'],
        index='station_id')
    G = nx.Graph()
    # add coordinates as    nodes of the graph
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


def print_map(G,filename):
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
    image.save(filename)





def print_path(path, G, file):
    m = StaticMap(800, 800)
    # print nodes on the map
    for i in range(len(path) - 1):
        marker = CircleMarker(path[i], 'red', 6)
        m.add_marker(marker)
        coordinates = [path[i], path[i + 1]]
        line = Line(coordinates, 'blue', 1)
        m.add_line(line)
    marker = CircleMarker(path[len(path)-1], 'red', 6)
    m.add_marker(marker)
    image = m.render()
    image.save(file)

def time(G, coord1, coord2):
    time = nx.dijkstra_path_length(G, coord1, coord2, weight='weight')
    return time


def route(G, coord1,coord2,filename):
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
    print_path(path, G,filename)
    t = time(G,coord1,coord2)
    if (not found1): G.remove_node(coord1)
    if (not found2): G.remove_node(coord2)
    return t

def data_acquisition():
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    stations = DataFrame.from_records(pd.read_json(url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(url_status)['data']['stations'], index='station_id')
    nbikes = 'num_bikes_available'
    ndocks = 'num_docks_available'
    bikes = bikes[[nbikes, ndocks]] # We only select the interesting columns
    TotalBikes = bikes[nbikes].sum()
    TotalDocks = bikes[ndocks].sum()
    return stations, bikes, nbikes, ndocks, TotalBikes, TotalDocks


def digraph(bikes, requiredBikes, requiredDocks, stations, radius):
    G = nx.DiGraph()
    G.add_node('TOP',demand=0) # The green node
    demand = 0

    for st in bikes.itertuples():
        idx = st.Index
        stridx = str(idx)

        # The blue (s), black (g) and red (t) nodes of the graph
        s_idx, g_idx, t_idx = 's'+stridx, 'g'+stridx, 't'+stridx
        G.add_node(g_idx)
        G.add_node(s_idx)
        G.add_node(t_idx)

        b, d = st.num_bikes_available, st.num_docks_available
        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)


        G.add_edge('TOP', s_idx)
        G.add_edge(t_idx, 'TOP')
        G.add_edge(s_idx, g_idx,capacity=max(0,b-requiredBikes))
        G.add_edge(g_idx, t_idx,capacity=max(0,d-requiredDocks))

        if req_bikes > 0:
            demand += req_bikes
            G.nodes[t_idx]['demand'] = req_bikes

        elif req_docks > 0:
            demand -= req_docks
            G.nodes[s_idx]['demand'] = -req_docks

    G.nodes['TOP']['demand'] =  -demand
    for idx1, idx2 in it.combinations(stations.index.values, 2):
        coord1 = (stations.at[idx1, 'lat'], stations.at[idx1, 'lon'])
        coord2 = (stations.at[idx2, 'lat'], stations.at[idx2, 'lon'])
        dist = haversine(coord1, coord2)
        if dist <= radius:
            dist = int(dist*1000)
            # The edges must be bidirectional: g_idx1 <--> g_idx2
            G.add_edge('g'+str(idx1), 'g'+str(idx2), weight=dist)
            G.add_edge('g'+str(idx2), 'g'+str(idx1), weight=dist)

    return G

def bicing_flow(radius = 0.6, requiredBikes =4, requiredDocks=3):
    stations, bikes, nbikes, ndocks, TotalBikes, TotalDocks = data_acquisition()
    G = digraph(bikes, requiredBikes, requiredDocks, stations, radius)
    err = False
    try:
        flowCost, flowDict = nx.network_simplex(G)

    except nx.NetworkXUnfeasible:
        err = True
        message = "No solution could be found"
        #return message

    except:
        err = True
        message = "Fatal error: Incorrect graph model"
        #return message

    if not err:
        # We update the status of the stations according to the calculated transportation of bicycles
        for src in flowDict:
            if src[0] != 'g': continue
            idx_src = int(src[1:])
            for dst, b in flowDict[src].items():
                if dst[0] == 'g' and b > 0:
                    idx_dst = int(dst[1:])
                    #print(idx_src, "->", idx_dst, " ", b, "bikes, distance", G.edges[src, dst]['weight'])
                    bikes.at[idx_src, nbikes] -= b
                    bikes.at[idx_dst, nbikes] += b
                    bikes.at[idx_src, ndocks] += b
                    bikes.at[idx_dst, ndocks] -= b
    return flowCost, flowDict,G

def components(G):
    return nx.number_connected_components(G)


def Nodes(G):
    return G.number_of_nodes()


def Edges(G):
    return G.number_of_edges()

def authors():
    authors = "Hugo Jiménez (hugo.jimenez@est.fib.upc.edu) and Jaume Martínez (jaume.martinez.ara@est.fib.upc.edu)"
    return authors
