from Espece import Espece
from EspeceHypothetique import EspeceHypothetique
from arbresPhylogenetiques import calculer_distance, reconstruire_arbre

###GENERE PAR UNE IA

#TESTS POUR calculer_distance

# --- Création des espèces avérées ---
lynx = Espece("Lynx", "ATCG")
chameau = Espece("Chameau", "ATCGGC")
gorille = Espece("Gorille", "ATCGGCA")
rat = Espece("Rat", "A")

# --- On passe le nom en premier paramètre ---
ancetre_lynx_chameau = EspeceHypothetique("(Lynx+Chameau)", lynx, chameau)
ancetre_gorille_rat = EspeceHypothetique("(Gorille+Rat)", gorille, rat)

# Le reste de vos fonctions de test fonctionnera maintenant sans erreur.
# --- Exécution des tests ---

print("--- Lancement des tests pour calculer_distance ---")

# 1. Test entre deux espèces avérées
dist_av_av = calculer_distance(lynx, chameau)
# Résultat attendu : distance_adn("ATCG", "ATCGGC") = abs(4 - 6) = 2
print(f"Test 1 (avérée/avérée): Lynx <-> Chameau. Résultat = {dist_av_av}. Attendu = 2. -> {'OK' if dist_av_av == 2 else 'ERREUR'}")

# 2. Test entre une espèce hypothétique et une avérée
dist_hypo_av = calculer_distance(ancetre_lynx_chameau, gorille)
# Résultat attendu :
# distance(lynx, gorille) = abs(4 - 7) = 3
# distance(chameau, gorille) = abs(6 - 7) = 1
# moyenne = (3 + 1) / 2 = 2.0
print(f"Test 2 (hypothétique/avérée): (Lynx+Chameau) <-> Gorille. Résultat = {dist_hypo_av}. Attendu = 2.0. -> {'OK' if dist_hypo_av == 2.0 else 'ERREUR'}")

# 3. Test entre une espèce avérée et une hypothétique (ordre inversé)
dist_av_hypo = calculer_distance(gorille, ancetre_lynx_chameau)
# Résultat attendu : identique au test 2 = 2.0
print(f"Test 3 (avérée/hypothétique): Gorille <-> (Lynx+Chameau). Résultat = {dist_av_hypo}. Attendu = 2.0. -> {'OK' if dist_av_hypo == 2.0 else 'ERREUR'}")

# 4. Test entre deux espèces hypothétiques
# Créons une deuxième espèce hypothétique
rat = Espece("Rat", "A") # len = 1

dist_hypo_hypo = calculer_distance(ancetre_lynx_chameau, ancetre_gorille_rat)
# Résultat attendu :
# dist((Lynx+Chameau), gorille) = 2.0 (calculé avant)
# dist((Lynx+Chameau), rat) = (dist(lynx,rat) + dist(chameau,rat))/2 = (abs(4-1) + abs(6-1))/2 = (3+5)/2 = 4.0
# moyenne finale = (2.0 + 4.0) / 2 = 3.0
print(f"Test 4 (hypothétique/hypothétique): (Lynx+Chameau) <-> (Gorille+Rat). Résultat = {dist_hypo_hypo}. Attendu = 3.0. -> {'OK' if dist_hypo_hypo == 3.0 else 'ERREUR'}")

#TEST DE RECONSTRUCTION D'ARBRE PHYLOGENETIQUE
# 1. Création d'un nouveau set d'espèces de départ pour ce test
espece_A = Espece("Souris", "ATCG")          # Longueur 4
espece_B = Espece("Rat", "ATCGA")         # Longueur 5 -> Distance de 1 avec A
espece_C = Espece("Lézard", "ATCGATCG")     # Longueur 8
espece_D = Espece("Crocodile", "ATCGATCGA") # Longueur 9 -> Distance de 1 avec C

especes_de_depart = [espece_A, espece_B, espece_C, espece_D]
print(f"Espèces de départ : {[e.nom for e in especes_de_depart]}\n")

# 2. Lancement de la reconstruction
arbre_final = reconstruire_arbre(especes_de_depart)

# 3. Affichage de la structure finale pour vérification
print("\n--- Structure de l'arbre final ---")
print(f"Racine : {arbre_final.nom}")
fille1 = arbre_final.especes_filles[0]
fille2 = arbre_final.especes_filles[1]
print(f"  -> Descendant 1 : {fille1.nom}")
print(f"  -> Descendant 2 : {fille2.nom}")