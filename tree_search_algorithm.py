import random
import pandas as pd
import graph_engine as ge

# df = pd.read_csv("selected_train_stations.csv", low_memory = False)

# problem = G
def SearchTreeAlgorithm(problem, strategy)
    # converting DataFrame in list for randomchoice function
    available_states = problem.nodes()
    # scegli uno stato dal df come stato iniziale
    initial_state = random.choice(available_states)  # i dizionari sono ottimizzati per l'accesso tramite 
                                                    # chiavi, quindi dobbiamo trasformare le chiavi in una 
                                                    # lista 
    # crea una lista di candidati per stato finale che sia diversa dallo stato iniziale
    candidated_goal_states = [s for s in available_states if s != initial_state]
    # scegli uno stato finale dai candidati per stato finale
    final_state = random.choice(candidated_goal_states)

    print (f"Viaggio da: {initial_state} a: {final_state}")