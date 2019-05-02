<<<<<<< HEAD
import pandas as pd
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim

def authors():
    print("The authors of these fabulous project are:")
    print("Hugo Jiménez, whose email adress is hugo.jimenez@est.fib.upc.edu")
    print("Jaume Martínez, whose email adress is jaume.martinez.ara@est.fib.upc.edu")

def graph(G):
    n = read(int)
    #the new graph will have distance n
    # G = ... (the graph with distance n)

# prints the connex components of G
def connex(G):
    ...


# plots the map with all the bicing stations and their connections
def plotgraph(G):
    ...

def main():
    G = nx.Graph()
    accio = read(string)
    while accio is not None:
        if (accio == "/start"):
            print("Hello")
        else if (accio == "/authors"):
            authors()
        else if (accio == "/graph"):
            graph(G)
        else if (accio == "/nodes"):
            print(G.number_of_nodes())
        else if (accio == "/edges"):
            print(G.number_of_edges())
        else if (accio == "/components"):
            connex()
        else if (accio == "/plotgraph"):
            plotgraph()
