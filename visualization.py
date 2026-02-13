import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gpd

def plot_on_map(G, pos):
    # uploading dataset with political boundaries of the world as collection of coordinates
    # url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip" 
    # world = gpd.read_file(url)
    world = gpd.read_file("zip://ne_110m_admin_0_countries.zip")
    
    # preventing mismatch in format column dataset
    col = 'CONTINENT' if 'CONTINENT' in world.columns else 'continent'
    # extracting just european state boundaries
    europe = world[world[col] == 'Europe'] if col in world.columns else world

    fig, ax = plt.subplots(figsize=(15, 10))
    europe.plot(ax=ax, color='whitesmoke', edgecolor='lightgray')

    # Disegno NetworkX
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=50, node_color='teal', alpha=0.8)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, edge_color='navy', alpha=0.3)

    ax.set_xlim([-15, 45]) 
    ax.set_ylim([34, 70])
    plt.title("European Railways network on Map")
    plt.show()