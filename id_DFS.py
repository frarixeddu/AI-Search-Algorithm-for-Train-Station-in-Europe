# libreria che trasforma una lista in una Priority Queue basata sul valore minimo del contenuto
import heapq
import math

def iterative_deepening_dfs(G, start, goal, max_depth):
    for depth_limit in range(max_depth):
        print(f"Ricerca con limite: {depth_limit}")
        result = depth_limited_search(G, start, goal, depth_limit)
        
        # Se result non è None, allora lo spacchettiamo
        if result:
            path, depth = result
            return path, depth
    return None, None

def depth_limited_search(G, start_node, goal_node, depth_limit):
    """
    Esegue la ricerca IDD
    """
    # 2. Inizializzazione della Fringe
    # ogni elemento è una tupla: (nodo corrente, percorso_per_arrivarci, depth_attuale)
    fringe = [(start_node, [start_node], 0)]

    while fringe:
        # estrai l'ultimo elemento della fringe (LIFO)
        # Quindi, l'ordine di espansione seguito è: estrai sempre l'ultimo nodo presente in fringe, che è il più recente
        current_node, path, depth = fringe.pop()

        # GOAL TEST: se siamo arrivati a destinazione, ritorna il percorso compiuto e la distanza totale percorsa
        if current_node == goal_node:
            return path, depth

        if depth < depth_limit: # se depth > depth_limit, allora quando rivà in fringe.pop, espande l'ultimo nodo presente nella fringe, che sarà il più recente
            # ESPANSIONE solo se non abbiamo superato il limite massimo
            for neighbor in G.neighbors(current_node):
                if neighbor not in path: # evita loop
                    new_path = path + [neighbor]
                    fringe.append((neighbor, new_path, depth+1))

    return None  # Nessun percorso trovato
