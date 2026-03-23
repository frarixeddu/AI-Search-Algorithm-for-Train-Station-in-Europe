from data_processing import process_stations
from graph_engine import build_state_space, haversine
from visualization import plot_on_map
from a_star_search import a_star_search
from id_DFS import dfs_search

# 1. Data processing - extracting the dataframe we will use
df_stations = process_stations("train_stations_europe.csv", "selected_train_stations.csv")

# 2. Connection definition
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

# 3. Building state space
# Returning graph "G" and dictionary "pos" with the position of every station
G, pos = build_state_space(df_stations, connections)

# 4. Plotting the state space on Europe map (just for visualization)
plot_on_map(G, pos)

import random

random.seed(42)

# print (f"Viaggio da: {initial_state} a: {final_state}")

# we convert the view "G.nodes()" into a list for future data manipulation operations 
# Dictionaries are optimized for key access so we have to convert the keys into a list 
available_states = list(G.nodes())

# Nome del file in cui salvare i risultati
astar_output_file = "risultati_test_AStar.txt"

# Apriamo il file in modalità 'w' (write - scrittura)
with open(astar_output_file, "w", encoding="utf-8") as f:
    f.write("REPORT RICERCA A* - 100 TEST CASUALI\n")
    f.write("="*50 + "\n")

    for i in range(1, 101):
        # initial state definition
        start = random.choice(available_states)
        # goal state's definition
        goal = random.choice([s for s in available_states if s != start])
        
        path, cost = a_star_search(G, start, goal, pos)
        
        # Prepariamo le stringhe da scrivere nel file
        f.write(f"\nTEST {i}\n")
        f.write(f"Da: {start} -> A: {goal}\n")
        
        if path:
            path_string = " -> ".join(path)
            f.write(f"Distanza totale: {cost:.2f} km\n")
            f.write(f"Percorso: {path_string}\n")
        else:
            f.write("Esito: Nessun percorso trovato.\n")
            
        f.write("-" * 30 + "\n")
    

available_states = list(G.nodes())

idDFS_output_file = "risultati_test_idDFS.txt"    

with open(idDFS_output_file, "w", encoding="utf-8") as f:
    f.write("REPORT RICERCA idDFS - 100 TEST CASUALI\n")
    f.write("="*50 + "\n")

    for i in range(1, 101):
        # initial state definition
        start = random.choice(available_states)
        # goal state's definition
        goal = random.choice([s for s in available_states if s != start])
        
        idDFS_path = dfs_search(G, start, goal)
        
        # Prepariamo le stringhe da scrivere nel file
        f.write(f"\nTEST {i}\n")
        f.write(f"Da: {start} -> A: {goal}\n")
        
        if idDFS_path:
            path_string = " -> ".join(idDFS_path)
            # f.write(f"Distanza totale: {cost:.2f} km\n")
            f.write(f"Percorso: {path_string}\n")
        else:
            f.write("Esito: Nessun percorso trovato.\n")
            
        f.write("-" * 30 + "\n")

    print(f"Operazione completata!")