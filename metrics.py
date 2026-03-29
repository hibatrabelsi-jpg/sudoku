import time
import tracemalloc
from backtracking import resoudre

def mesurer(grille):
    tracemalloc.start()
    debut = time.time()
    resultat = resoudre(grille)
    fin = time.time()
    _, memoire_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        "temps": fin - debut,
        "memoire_max": memoire_max,
        "compteur": resultat["compteur"],
        "snapshots": resultat["snapshots"]
    }