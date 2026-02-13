import networkx as nx
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlamb = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlamb/2)**2
    return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)

def build_state_space(df, connections):
    # Initializa an empty graph of NetworkX non-oriented
    G = nx.Graph()
    # creating an empty dictionary for station positions in the state space graph
    pos = {}

    for start, end in connections:
    # loop that analyzes each couple (node, node) of the dictionary, providing mutual distance for the edge
    # and stores their position in the graph
        if start in df.index and end in df.index:
            # checks if the two nodes are both in csv file
            dist = haversine(df.loc[start, 'latitude'], df.loc[start, 'longitude'],
                             df.loc[end, 'latitude'], df.loc[end, 'longitude'])
            G.add_edge(start, end, weight=dist)
            # populating the dictionary "pos" with positions of each station
            pos[start] = (df.loc[start, 'longitude'], df.loc[start, 'latitude'])
            pos[end] = (df.loc[end, 'longitude'], df.loc[end, 'latitude'])
    return G, pos