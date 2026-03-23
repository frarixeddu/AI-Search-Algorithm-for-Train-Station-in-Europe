# libreria che trasforma una lista in una Priority Queue basata sul valore minimo del contenuto
import heapq
import math
from graph_engine import haversine

def a_star_search(G, start_node, goal_node, pos):
    """
    Esegue la ricerca A* 
    """
    # --- METRICHE ---
    nodes_expanded = 0  # complessità temporale
    max_memory = 0      # complessità spaziale
    # ----------------

    # 1. Definizione dell'euristica h(n) internamente per comodità
    def get_h(node):
        # calcola la distanza in linea d'aria (euristica) tra il nodo considerato e il nodo obbiettivo 
        # pos[node] contiene (lon, lat) del nodo
        
        # Usiamo la tua funzione haversine (assicurati sia importata o definita)
        return haversine(pos[node], pos[goal_node])

    # 2. Inizializzazione della Fringe (Priority Queue)
    # Formato nodi/states nella fringe: (f_score, g_score, nodo_attuale, percorso_compiuto)
    # inizializzazione fringe
    fringe = [] #fringe è una OPEN LIST
    # euristica stato iniziale (f(n)=h(n) because g(n)=0 initially)
    h_start = get_h(start_node)

    # enqueue the initial state into the fringe
    # heappush inserisce l'elemento nell'heap e lo riordina in modo che l'oggetto (il nodo) con primo elemento (f_score) 
    # più piccolo si trovi sempre in prima posizione nell'heap
    heapq.heappush(fringe, (h_start, 0, start_node, [start_node]))

    # 3. Dizionario per i costi minimi trovati (formato: {nodo visitato: costo accumulato per arrivarci}
    # Durante una "run" (da start vogliamo arrivare a end) ogni nodo incontrato viene mano a mano espanso.
    # Durante ogni espansione, bisogna memorizzare il costo totale accumulato (g(n)) fino a quel momento da quel nodo
    # In questo modo, sarà sempre disponibile per ulteriori future espansioni
    # Viene ciclicamente popolato mano a mano che si esplorano tutti i nodi papabili
    visited_costs = {start_node: 0} # visited_costs è una CLOSED LIST

    while fringe:

        # Update max memory (complessità spaziale)
        max_memory = max(max_memory, len(fringe))

        # heappop estrae e rimuove l'oggetto (il nodo) con f_score minore dalla fringe
        f, g, current_node, path = heapq.heappop(fringe)

        nodes_expanded += 1 # Incrementa ogni volta che estrai (complessità temporale)

        # GOAL TEST: se siamo arrivati a destinazione, ritorna il percorso compiuto e la distanza totale percorsa
        if current_node == goal_node:
            return path, g

        # ESPANSIONE: per ogni elemento selezionato nella fringe, guardiamo i vicini 
        for neighbor in G.neighbors(current_node):
            # Peso del tragitto (distanza reale tra le stazioni)
            step_cost = G[current_node][neighbor].get('weight', 1)  # g'(n) = distanza tra nodo corrente e suo vicino
            new_g = g + step_cost   # aggiungi g'(n) al totale calcolato fino ad ora per quel vicino => g_tot(n) = g(n) + g'(n)  
            
            # Controlla: 
            # - se è un nodo già esplorato (evita loops) 
            # OPPURE 
            # - (tuttavia, se l'euristica è consistente questo non accadrà mai) se il nodo è già presente, allora entra nell'if solo se g(n) è un costo migliore di quello trovato fino ad ora per quel nodo
            if neighbor not in visited_costs or new_g < visited_costs[neighbor]:
                # aggiungi il nuovo costo g(n) del nodo alla lista "visited_costs"
                visited_costs[neighbor] = new_g
                
                # Aggiorniamo f = g + h per quel nodo
                new_f = new_g + get_h(neighbor)
                
                # calcola percorso compiuto finora per quel nodo
                new_path = path + [neighbor]
                # Aggiungiamo alla fringe il nodo aggiornato dei suoi valori per espansioni future
                heapq.heappush(fringe, (new_f, new_g, neighbor, new_path))

    return None, float('inf')  # Nessun percorso trovato
