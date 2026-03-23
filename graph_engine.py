import networkx as nx
import math

def haversine(coord_start_node, coord_end_node):
    R = 6371
    lon_start_node, lat_start_node = coord_start_node
    lon_end_node, lat_end_node = coord_end_node
    phi1, phi2 = math.radians(lat_start_node), math.radians(lat_end_node)
    dphi, dlamb = math.radians(lat_end_node - lat_start_node), math.radians(lon_end_node - lon_start_node)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlamb/2)**2
    return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371
#     phi1, phi2 = math.radians(lat1), math.radians(lat2)
#     dphi, dlamb = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
#     a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlamb/2)**2
#     return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)

def build_state_space(df, connections):
    # Initialize an empty graph of NetworkX non-oriented
    G = nx.Graph()
    # creating an empty dictionary for station positions in the state space graph
    pos = {}

    for start_node, end_node in connections:
    # loop that analyzes each couple (node, node) of the dictionary "connections", and provides their mutual distance
    # and stores their position in the graph
        if start_node in df.index and end_node in df.index:     # if (start_node belonging to "connections") is in the dataframe... checks if the two nodes are both in DF. We make sure that a city in the connections list is actually in the DF (it's just a safety parachute)
            if start_node not in pos:   # popolates "pos" only if we don't have the coordinates of the station yet 
                pos[start_node] = (df.loc[start_node, 'longitude'], df.loc[start_node, 'latitude'])
            if end_node not in pos:
                pos[end_node] = (df.loc[end_node, 'longitude'], df.loc[end_node, 'latitude'])
            
            dist = haversine(pos[start_node], pos[end_node])
            # creating edge in the G graph with distance "dist" as a weight
            G.add_edge(start_node, end_node, weight=dist)
            # populating the dictionary "pos" with positions of each station
    return G, pos