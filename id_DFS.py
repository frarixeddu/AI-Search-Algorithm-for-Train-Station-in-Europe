# libreria che trasforma una lista in una Priority Queue basata sul valore minimo del contenuto
import heapq
import math
from graph_engine import haversine

def dfs_search(G, start_node, goal_node):
    """
    Esegue la ricerca IDD
    """
    # 2. Inizializzazione della Fringe
    # ogni elemento è una tupla: (nodo corrente, percorso_per_arrivarci)
    fringe = [(start_node, [start_node])]

    # usare set() è molto più veloce di usare una lista
    visited = set()

    while fringe:
        # estrai l'ultimo elemento della fringe (LIFO)
        current_node, path = fringe.pop()

        # GOAL TEST: se siamo arrivati a destinazione, ritorna il percorso compiuto e la distanza totale percorsa
        if current_node == goal_node:
            return path
        
        # evita loop 
        if current_node not in visited:
            visited.add(current_node)

        # ESPANSIONE: per ogni elemento selezionato nella fringe, guardiamo i vicini 
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                new_path = path + [neighbor]
                fringe.append((neighbor, new_path))

    return None  # Nessun percorso trovato
