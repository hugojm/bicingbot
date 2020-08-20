import pandas as pd
import networkx as nx
import itertools as it
from pandas import DataFrame
from haversine import haversine
from staticmap import StaticMap, CircleMarker, Line
from geopy.geocoders import Nominatim
import time

# Given the graph it returns the bounding box


def bbox(G):
    # lat y [1]
    # lon x [0]
    H = list(G.nodes())
    maxx, maxy = H[0]
    minx, miny = H[0]
    for nodes in G.nodes():
        if (nodes[0] > maxx):
            maxx = nodes[0]
        if (nodes[0] < minx):
            minx = nodes[0]
        if (nodes[1] > maxy):
            maxy = nodes[1]
        if (nodes[1] < miny):
            miny = nodes[1]
    return minx, miny, maxy, maxx

# given a matrix with all the points of the graph classified, it returns the
# graph G with the edges with length d or less.


def compare(G, rows, columns, matriz, dist):
    for i in range(rows):
        for j in range(columns):
            for node in matriz[i][j]:
                for node_comp in matriz[i][j]:  # same
                    distance = haversine(
                        (node[1], node[0]), (node_comp[1], node_comp[0]))
                    if (distance <= dist / 1000.0 and node != node_comp):
                        G.add_edge(
                            node, node_comp, weight=float(
                                distance / 10))
                if (i + 1 < rows):
                    for node_comp in matriz[i + 1][j]:  # below
                        distance = haversine(
                            (node[1], node[0]), (node_comp[1], node_comp[0]))
                        if (distance <= dist / 1000.0):
                            G.add_edge(node, node_comp,
                                       weight=float(distance / 10))
                if (i + 1 < rows and j + 1 < columns):
                    for node_comp in matriz[i + 1][j + 1]:  # right below
                        distance = haversine(
                            (node[1], node[0]), (node_comp[1], node_comp[0]))
                        if (distance <= dist / 1000.0):
                            G.add_edge(node, node_comp,
                                       weight=float(distance / 10))
                if (j + 1 < columns):
                    for node_comp in matriz[i][j + 1]:  # right
                        distance = haversine(
                            (node[1], node[0]), (node_comp[1], node_comp[0]))
                        if (distance <= dist / 1000.0):
                            G.add_edge(node, node_comp,
                                       weight=float(distance / 10))
                if (i + 1 < rows and j - 1 >= 0):
                    for node_comp in matriz[i + 1][j - 1]:  # left below
                        distance = haversine(
                            (node[1], node[0]), (node_comp[1], node_comp[0]))
                        if (distance <= dist / 1000.0):
                            G.add_edge(node, node_comp,
                                       weight=float(distance / 10))
    return G


# linear algorithm for finding the edges


def CreateGraph(dist=1000):
    # import the data
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(
        pd.read_json(dataset)['data']['stations'],
        index='station_id')
    G = nx.Graph()
    # add all the nodes in the graph
    for st in bicing.itertuples():
        G.add_node((st.lon, st.lat), id=st.Index)

    # calculates the bounding box of the coordinates given the graph
    minx, miny, maxy, maxx = bbox(G)
    # calculates the width and height of the bbox
    width = haversine((miny, minx), (maxy, minx))
    height = haversine((miny, minx), (miny, maxx))
    # how many columns and rows the matrix has
    columns = int((width // (dist / 1000.0)) + 1)
    rows = int((height // (dist / 1000.0)) + 1)

    # x [0] lon
    # y [1] lat
    # creates a matrix of lists
    matriz = []
    for i in range(rows):
        matriz.append([])
        for j in range(columns):
            matriz[i].append([])

    # sorts out every node in the matrix
    for node in G.nodes():
        x = int(haversine((node[1], minx),
                          (node[1], node[0])) / (dist / 1000.0))
        y = int(haversine((maxy, node[0]),
                          (node[1], node[0])) / (dist / 1000.0))
        matriz[x][y].append(node)
    # given the matrix, it compares with the possible edges
    G = compare(G, rows, columns, matriz, dist)
    return G

# quadratic algorithm for finding the edges (used when distance <= 250)


def Graph(distance=1000):
    dataset = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
    bicing = DataFrame.from_records(
        pd.read_json(dataset)['data']['stations'],
        index='station_id')
    G = nx.Graph()
    # add coordinates as nodes of the graph
    for st in bicing.itertuples():
        G.add_node((st.lon, st.lat), id=st.Index)
    for nod in G.nodes():
        for nod2 in G.nodes():
            # first latitude and then longitude to calculate haversine
            coord1 = (nod[1], nod[0])
            coord2 = (nod2[1], nod2[0])
            if (haversine(coord1, coord2) <= float(distance / 1000) and
                    nod != nod2):
                G.add_edge(
                    nod, nod2, weight=float(
                        haversine(
                            coord1, coord2) / 10))
    return G

# given the graph and a filename it returns a map with that filename


def print_map(G, filename):
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

# given the path and the graph it returns the map of the path


def print_path(path, G, file):
    m = StaticMap(800, 800)
    # go through the path and print every node
    for i in range(len(path) - 1):
        marker = CircleMarker(path[i], 'red', 6)
        m.add_marker(marker)
        coordinates = [path[i], path[i + 1]]
        line = Line(coordinates, 'blue', 1)
        m.add_line(line)
    marker = CircleMarker(path[len(path) - 1], 'red', 6)
    m.add_marker(marker)
    image = m.render()
    image.save(file)

# given the graph and source and target it returns the time employed


def time(G, coord1, coord2):
    time = nx.dijkstra_path_length(G, coord1, coord2, weight='weight')
    return time

# Given the graph and 2 coordinates we find if they aren't already in
# the graph


def search_coordinates(G, coord1, coord2):
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

    return G, found1, found2

# Given the graph, source, target and filename it returns the shortest path


def route(G, coord1, coord2, filename):
    G, found1, found2 = search_coordinates(G, coord1, coord2)
    # We find if the given coordinates aren't bicing stations
    path = nx.dijkstra_path(G, coord1, coord2, weight='weight')
    print_path(path, G, filename)
    t = time(G, coord1, coord2)
    # Removes from the graph the source and target if they weren't there before
    if not found1:
        G.remove_node(coord1)
    if not found2:
        G.remove_node(coord2)

    return t


def data_acquisition():
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/'\
        'station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    stations = DataFrame.from_records(pd.read_json(
        url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(
        url_status)['data']['stations'], index='station_id')
    nbikes = 'num_bikes_available'
    ndocks = 'num_docks_available'
    bikes = bikes[[nbikes, ndocks]]  # We only select the interesting columns
    TotalBikes = bikes[nbikes].sum()
    TotalDocks = bikes[ndocks].sum()
    return stations, bikes, nbikes, ndocks, TotalBikes, TotalDocks

# given the information it creates the flow graph


def digraph(bikes, requiredBikes, requiredDocks, stations, F):
    G = nx.DiGraph()
    G.add_node('TOP', demand=0)  # The green node
    demand = 0
    # we create a dictionary with key the coordinates and value the index in
    # order to guarantee the proper performance of the algorithm, provided
    # the index of the stations is needed.
    J = dict(F.nodes(data='id', default='Not Available'))
    for st in bikes.itertuples():
        idx = st.Index
        if idx not in stations.index:
            continue
        stridx = str(idx)

        # The blue (s), black (g) and red (t) nodes of the graph
        s_idx, g_idx, t_idx = 's' + stridx, 'g' + stridx, 't' + stridx
        G.add_node(g_idx)
        G.add_node(s_idx)
        G.add_node(t_idx)

        b, d = st.num_bikes_available, st.num_docks_available
        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)

        G.add_edge('TOP', s_idx)
        G.add_edge(t_idx, 'TOP')
        G.add_edge(s_idx, g_idx, capacity=max(0, b - requiredBikes))
        G.add_edge(g_idx, t_idx, capacity=max(0, d - requiredDocks))

        if req_bikes > 0:
            demand += req_bikes
            G.nodes[t_idx]['demand'] = req_bikes

        elif req_docks > 0:
            demand -= req_docks
            G.nodes[s_idx]['demand'] = -req_docks

    G.nodes['TOP']['demand'] = -demand
    for edge in F.edges():
        coord1 = (edge[0][1], edge[0][0])
        coord2 = (edge[1][1], edge[1][0])
        dist = int(haversine(coord1, coord2) * 1000)
        # The edges must be bidirectional: g_idx1 <--> g_idx2
        G.add_edge('g' + str(J[edge[0]]), 'g' + str(J[edge[1]]), weight=dist)
        G.add_edge('g' + str(J[edge[1]]), 'g' + str(J[edge[0]]), weight=dist)

    return G

# it calculates the bicing flow needed to satisfy the conditions


def bicing_flow(G, requiredBikes, requiredDocks):
    # take the data
    sts, bikes, nbikes, ndocks, TotalBikes, TotalDocks = data_acquisition()
    # create the flow graph
    G = digraph(bikes, requiredBikes, requiredDocks, sts, G)
    # computes the flow and returns the flow cost and the movements needed
    flowCost, flowDict = nx.network_simplex(G)

    # update the status of the stations according to the calculated
    # transportation of bicycles
    cost = 0
    for src in flowDict:
        if src[0] != 'g':
            continue
        idx_src = int(src[1:])
        for dst, b in flowDict[src].items():
            if dst[0] == 'g' and b > 0:
                idx_dst = int(dst[1:])
                if G.edges[src, dst]['weight'] * b > cost:
                    cost = G.edges[src, dst]['weight'] * b
                    aresta1, aresta2 = idx_src, idx_dst
                    bikes = b
                    dist = G.edges[src, dst]['weight']

    return flowCost, aresta1, aresta2, bikes, dist

# Given the graph it returns the number of connected components


def components(G):
    return nx.number_connected_components(G)

# Given the graph it returns the number of nodes


def Nodes(G):
    return G.number_of_nodes()

# Given the graph it returns the number of edges


def Edges(G):
    return G.number_of_edges()

# It returns the authors' names


def authors():
    authors = "*Hugo Jiménez Muñoz* (hugo.jimenez@est.fib.upc.edu)\n" +\
        "*Jaume Martínez Ara* (jaume.martinez.ara@est.fib.upc.edu)\n" +\
        "_Universitat Politècnica de Catalunya_ ***(UPC-FIB)***"
    return authors
