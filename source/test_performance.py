from Espece import Espece
from arbresPhylogenetiques import calculer_distance, reconstruire_arbre
import timeit
import random

#Fais par IA
# --- Test de performance pour calculer_distance ---
# Création de deux espèces avec de longues séquences ADN pour un test plus réaliste
adn_long_1 = ''.join(random.choices('ATCG', k=2000))
adn_long_2 = ''.join(random.choices('ATCG', k=2000))
espece_perf_1 = Espece("Perf_Espece_1", adn_long_1)
espece_perf_2 = Espece("Perf_Espece_2", adn_long_2)

# Mesure du temps d'exécution pour 10000 appels
temps_calcul_distance = timeit.timeit(lambda: calculer_distance(espece_perf_1, espece_perf_2), number=10000)
print(f"Temps d'exécution pour 10 000 appels à calculer_distance (ADN de taille 2000): {temps_calcul_distance:.6f} secondes.")

# --- Test de performance pour reconstruire_arbre ---
def generer_espece_aleatoire(nom, taille_adn):
    adn = ''.join(random.choices('ATCG', k=taille_adn))
    return Espece(nom, adn)

# Génération d'une liste de 50 espèces avec des ADN de tailles variables
especes_pour_arbre_perf = [generer_espece_aleatoire(f"Espece_{i}", random.randint(500, 1500)) for i in range(50)]

temps_reconstruction = timeit.timeit(lambda: reconstruire_arbre(especes_pour_arbre_perf), number=1)
print(f"Temps d'exécution pour reconstruire un arbre avec 50 espèces : {temps_reconstruction:.6f} secondes.")