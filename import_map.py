import numpy as np
import pandas as pd

# importing database from kaggle's .csv file
df = pd.read_csv("train_stations_europe.csv", low_memory=False)

# extracting just the samples where train station is a main station
filtered = df[df["is_main_station"] == True].copy()

# removing rows without coordinates
filtered = filtered.dropna(subset=["latitude", "longitude"])

# sampling for country 
sampled_list = []
for country, group in filtered.groupby("country"):
    sample_size = min(3, len(group))
    sampled_group = group.sample(n=sample_size, random_state=42)
    sampled_list.append(sampled_group)

sampled = pd.concat(sampled_list, ignore_index=True)

# columns we want to pass to Google My Maps hust for visualization
selected = sampled[[
    "name",
    "country",
    "latitude",
    "longitude"
]]

# save the info in a csv file for Google My Maps
selected.to_csv("selected_train_stations.csv", index=False)

# print("File creato con successo!")
# print(f"Numero di stazioni selezionate: {len(selected)}")
# print(f"\nPaesi inclusi:\n{selected['country'].value_counts()}")

import matplotlib.pyplot as plt

# uploading the selected train stations file
df_plot = pd.read_csv("selected_train_stations.csv")

plt.figure(figsize=(12, 8))
plt.scatter(df_plot['longitude'], df_plot['latitude'], color='red', s=15, alpha=0.7)

# Adding name to each station in the plot
for i, row in df_plot.iterrows():
    # if i % 5 == 0: # Etichetta una stazione ogni 5 per non affollare la mappa
        plt.text(row['longitude'], row['latitude'], row['name'], fontsize=8)

plt.title("Geographical distribution of selected train stations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

import networkx as nx
import matplotlib.pyplot as plt
import math

# Computing geodetic function between two point given their coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlamb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlamb/2)**2
    return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)

# creating a df 
# setting the name as index for every row, ready for the next loop  
df = pd.read_csv('selected_train_stations.csv').set_index('name')

# Defining connections for state space (no orientation between nodes)
connections = [
    ("Antwerpen-Centraal", "Amsterdam-Centraal"),
    ("Amsterdam-Centraal", "Den Haag Centraal"),
    ("Den Haag Centraal", "Leiden Lammenschans"),
    ("Bruxelles-Midi", "Luxembourg"),
    ("Luxembourg", "Rodange"),
    ("Luxembourg", "Luxembourg Gare Centrale (Quai 13)"),
    ("Nomain", "Charleroi-Ouest"),
    ("Charleroi-Ouest", "Bruxelles-Midi"),
    ("Salzburg Hbf", "Villach Hbf"),
    ("Villach Hbf", "Wolfsberg in Ktn Bahnhof"),
    ("Praha hl.n.", "Ústí nad Labem hl.n."),
    ("Praha hl.n.", "Ostrava-Vítkovice"),
    ("Magdeburg Hbf", "Bremen Hbf"),
    ("Bremen Hbf", "Freudenstadt Hbf"),
    ("Villach Hbf", "Pula Airport"),
    ("Imperia", "Bellinzona"),
    ("Bellinzona", "Frauenfeld Bahnhof"),
    ("Frauenfeld Bahnhof", "Balsthal"),
    ("Catanzaro (Germaneto)", "Nardò Città"),
    ("Porto Campanhã", "Porto Sao Bento"),
    ("Porto Campanhã", "Lisboa Santa Apolónia"),
    ("Porto Campanhã", "San Fernando de Cádiz"),
    ("Porto Campanhã", "Barcelona El Prat T1"),
    ("Lisboa Santa Apolónia", "San Fernando de Cádiz"),
    ("Lisboa Santa Apolónia", "Barcelona El Prat T1"),
    ("San Fernando de Cádiz", "Barcelona El Prat T1"),
    ("San Fernando de Cádiz", "Lorca-San Diego"),
    ("Barcelona El Prat T1", "Imperia"),
    ("Barcelona El Prat T1", "Langres"),
    ("Barcelona El Prat T1", "St-Sever Calvados"),
    ("Pembroke Station", "Newhaven Town"),
    ("Newhaven Town", "Falkirk High"),
    ("Warszawa-Centralna", "Łódź Kaliska"),
    ("Warszawa-Centralna", "Bratislava hl.st."),
    ("Bratislava hl.st.", "Budapest-Keleti"),
    ("Odense St.", "Herning St."),
    ("Herning St.", "Nykøbing Falster St."),
    ("Vetlanda station", "Ekenässjön station"),
    ("Ekenässjön station", "Nybro Station"),
    ("Bremen Hbf", "Odense St."),            
    ("Nykøbing Falster St.", "Vetlanda station"), 
    ("Magdeburg Hbf", "Warszawa-Centralna"), 
    ("Budapest-Keleti", "Salzburg Hbf"),
    ("Nardò Città", "Imperia"),         
    ("Bruxelles-Midi", "Newhaven Town"),
    ("St-Sever Calvados", "Nomain"),    
    ("Den Haag Centraal", "Bruxelles-Midi"), 
    ("Den Haag Centraal", "Antwerpen-Centraal"),  
    ("Leiden Lammenschans", "Antwerpen-Centraal"),
    ("Rodange", "Bruxelles-Midi"), 
    ("Rodange", "Charleroi-Ouest"), 
    ("Rodange", "Nomain"),
    ("Den Haag Centraal", "Newhaven Town"),
    ("Luxembourg", "Antwerpen-Centraal"), 
    ("Luxembourg", "Amsterdam-Centraal"), 
    ("Luxembourg", "Bruxelles-Midi"), 
    ("Luxembourg", "Charleroi-Ouest"),
    ("Rodange", "Langres"), 
    ("Rodange", "Freudenstadt Hbf"),
    ("Balsthal", "Langres"), 
    ("Freuenfeld Bahnhof", "Langres"), 
    ("Balsthal", "Freudenstadt Hbf"), 
    ("Luxembourg", "Freudenstadt Hbf"), 
    ("Luxembourg Gare Centrale (Quai 13)", "Freudenstadt Hbf"),
    ("Frauenfeld Bahnhof", "Freudenstadt Hbf"),
    ("Langres", "St-Sever Calvados"), 
    ("Langres", "Nomain"), 
    ("Langres", "Newhaven Town"), 
    ("Langres", "Charleroi-Ouest"), 
    ("Rodange", "Balsthal"), 
    ("Amsterdam-Centraal", "Breemen Hbf"), 
    ("Amsterdam-Centraal", "Magdeburg Hbf"),
    ("Amsterdam-Centraal", "Herning St."), 
    ("Amsterdam-Centraal", "Odense St."), 
    ("Antwerpen-Centraal", "Breemen Hbf"), 
    ("Antwerpen-Centraal", "Magdeburg Hbf"),
    ("Antwerpen-Centraal", "Herning St."), 
    ("Antwerpen-Centraal", "Odense St."),
    ("Freudenstadt Hbf", "Praha hl.n."), 
    ("Freudenstadt Hbf", "Magdeburg Hbf"), 
    ("Freudenstadt Hbf", "Villach Hbf"),  
    ("Imperia", "St-Sever Calvados"),  
    ("Imperia", "Pula Airport"), 
    #("Nardò Città", "Pula Airport"), 
    ("Nardò Città", "Bellinzona"), 
    ("Nardo Città", "Budapest-Keleti"), 
    #("Nardò Città", "Wolfsberg in Ktn Bahnhof"), 
    ("Bratislava hl.st.", "Salzburg Hbf"), 
    ("Bratislava hl.st.", "Freudenstadt Hbf"), 
    ("Bratislava hl.st.", "Praha hl.n."), 
    ("Ostrava-Vítkovice", "Warszawa Centralna"), 
    ("Nybro Station", "Warszawa Centralna"), 
    ("Nybro Station", "Herning St."), 
    ("Nybro Station", "Magdeburg Hbf"), 
    ("Ekenässjön station", "Warszawa Centralna"), 
    ("Łódź Kaliska", "Ústí nad Labem hl.n."), 
    ("Warszawa-Centralna", "Moskva Kievskaia"),
    #("Moskva Kievskaia", "Nybro Station"),
    ("Moskva Kievskaia", "Bratislava hl.st."),
    ("Moskva Kievskaia", "Budapest-Keleti"),
    ("Nykøbing Falster St.", "Warszawa-Centralna"), 
    ("Dublin Connolly", "Newhaven Town"), 
    ("Dublin Connolly", "Falkirk High"), 
    ("Dublin Connolly", "Pembroke Station"),
    ("Rovini Autobusni Kolodvor", "Pula Airport"), 
    ("Rovini Autobusni Kolodvor", "Bellinzona"), 
    ("Rovini Autobusni Kolodvor", "Imperia"), 
    ("Biograd na Moru Autobusni Kolodvor", "Pula Airport"), 
    ("Biograd na Moru Autobusni Kolodvor", "Nardo Città"), 
    ("Biograd na Moru Autobusni Kolodvor", "Imperia"), 
    ("Antwerpen-Centraal", "Bruxelles-Midi"),  
]

# Builiding state space graph
# Initializa an empty graph of NetworkX non-oriented
G = nx.Graph()
# creating an empty dictionary for station positions in the state space graph
pos = {}

# loop that analyzes each couple (node, node) of the dictionary, providing mutual distance for the edge
# and stores their position in the graph
for start, end in connections:
    # check if the two nodes are both in csv file
    if start in df.index and end in df.index:
        d = haversine(df.loc[start, 'latitude'], df.loc[start, 'longitude'],
                      df.loc[end, 'latitude'], df.loc[end, 'longitude'])
        G.add_edge(start, end, weight=d)
        # populating the dictionary "pos" with positions of each station
        pos[start] = (df.loc[start, 'longitude'], df.loc[start, 'latitude'])
        pos[end] = (df.loc[end, 'longitude'], df.loc[end, 'latitude'])

# prepraring plot figure
plt.figure(figsize=(12, 9))
# drawing nodes (stations) and their names and edges in the plot
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='teal', alpha=0.8)
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', verticalalignment='bottom')
nx.draw_networkx_edges(G, pos, width=2, edge_color='navy', alpha=0.4)

# Drawing distances into each edge and formatting for km representation on the graph
edge_labels = nx.get_edge_attributes(G, 'weight')
formatted_edge_labels = {k: f"{v} km" for k, v in edge_labels.items()}

nx.draw_networkx_edge_labels(
    G, pos, 
    edge_labels=formatted_edge_labels, 
    font_color='red', 
    font_size=8,
    label_pos=0.5 
)

# naming axies and providing a title
plt.title("Railway State Space: Connections and Geodetic Distances", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle='--', alpha=0.3)

# Margins for not cutting city names
plt.margins(0.15)
plt.show()


# SHOWING SPACE STATE OVER EUROPE MAP
import geopandas as gpd

# Carica i dati dall'URL
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

# Controlliamo come si chiama la colonna (spesso è 'CONTINENT' o 'continent')
# Per sicurezza usiamo un approccio che non fallisce:
if 'CONTINENT' in world.columns:
    europe = world[world['CONTINENT'] == 'Europe']
elif 'continent' in world.columns:
    europe = world[world['continent'] == 'Europe']
else:
    # Se proprio non la trova, prendiamo tutto il mondo 
    # e useremo i limiti della mappa (set_xlim) per inquadrare l'Europa
    europe = world

# 3. Creiamo il plot
fig, ax = plt.subplots(figsize=(15, 10))

# Disegniamo la mappa dell'Europa come sfondo
europe.plot(ax=ax, color='whitesmoke', edgecolor='lightgray')

# 4. Sovrapponiamo il tuo Grafo
# Nota: passiamo 'ax=ax' alle funzioni di NetworkX per disegnare sopra la mappa
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=50, node_color='teal', alpha=0.8)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight='bold')
nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, edge_color='navy', alpha=0.3)

# Impostiamo i limiti della vista per zoomare sull'area interessata
ax.set_xlim([-15, 45]) 
ax.set_ylim([34, 70])  

plt.title("Rete Ferroviaria Europea su Mappa Reale")
plt.margins(0.15)
plt.show()