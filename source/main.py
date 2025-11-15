import random
from Espece import Espece
from algoADN import generer_sequence_adn_aleatoire, muter_remplacement, muter_complet
from calculSimilarite import distance_remplacement, distance_levenshtein
from arbresPhylogenetiques import reconstruire_arbre

def menu_principal():
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    print("--- Menu Principal ---")
    print("1. Générer une séquence d'ADN aléatoire")
    print("2. Muter une séquence d'ADN")
    print("3. Calculer la distance entre deux séquences")
    print("4. Reconstruire un arbre phylogénétique")
    print("0. Quitter")
    return input("Votre choix : ")

def generer_sequence():
    """Gère la génération d'une séquence ADN aléatoire."""
    while True:
        longueur_str = input("Entrez la longueur de la séquence d'ADN : ")
        if not longueur_str.isdigit():
            print("Erreur : Veuillez entrer un nombre entier positif.")
            continue
        longueur = int(longueur_str)
        if longueur <= 0:
            print("Erreur : La longueur doit être un entier positif.")
            continue
        break
    sequence = generer_sequence_adn_aleatoire(longueur)
    print(f"Séquence générée : {sequence}")

def muter_sequence():
    """Gère les différentes mutations d'une séquence ADN."""
    sequence = input("Entrez la séquence d'ADN à muter : ").upper()
    for c in sequence:
        if c not in 'ATCG':
            print("Erreur : La séquence contient des bases non valides (doit être A, T, C, ou G).")
            return

    print("--- Type de Mutation ---")
    print("1. Remplacement simple")
    print("2. Mutation complète (remplacement, insertion, délétion)")
    choix_mutation = input("Votre choix : ")

    try:
        if choix_mutation == '1':
            while True:
                p_str = input("Entrez la probabilité de remplacement (entre 0 et 1) : ")
                try:
                    p = float(p_str)
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre réel (ex: 0.5).")
                    continue
                if not (0 <= p <= 1):
                    print("Erreur : La probabilité doit être comprise entre 0 et 1.")
                    continue
                break
            sequence_mutee = muter_remplacement(sequence, p)
            print(f"Séquence originale : {sequence}")
            print(f"Séquence mutée    : {sequence_mutee}")
        elif choix_mutation == '2':
            while True:
                try:
                    p_remplacement = float(input("Entrez la probabilité de remplacement (0-1) : "))
                    p_insertion = float(input("Entrez la probabilité d'insertion (0-1) : "))
                    p_delation = float(input("Entrez la probabilité de délétion (0-1) : "))
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre réel (ex: 0.5).")
                    continue
                if not (0 <= p_remplacement <= 1 and 0 <= p_insertion <= 1 and 0 <= p_delation <= 1):
                    print("Erreur : Toutes les probabilités doivent être entre 0 et 1.")
                    continue
                break
            sequence_mutee = muter_complet(sequence, p_remplacement, p_insertion, p_delation)
            print(f"Séquence originale : {sequence}")
            print(f"Séquence mutée    : {sequence_mutee}")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Erreur : Veuillez entrer une probabilité valide (nombre flottant).")

def calculer_distance_sequences():
    """Gère le calcul de distance entre deux séquences ADN."""
    seq1 = input("Entrez la première séquence d'ADN : ").upper()
    seq2 = input("Entrez la deuxième séquence d'ADN : ").upper()

    for c in seq1:
        if c not in 'ATCG':
            print("Erreur : La première séquence contient des bases non valides.")
            return
    for c in seq2:
        if c not in 'ATCG':
            print("Erreur : La deuxième séquence contient des bases non valides.")
            return

    print("--- Type de Distance ---")
    print("1. Distance de remplacement (pour séquences de même taille)")
    print("2. Distance de Levenshtein")
    choix_distance = input("Votre choix : ")

    if choix_distance == '1':
        distance = distance_remplacement(seq1, seq2)
        if distance is None:
            print("Erreur : Les séquences doivent avoir la même longueur pour cette distance.")
        else:
            print(f"La distance de remplacement entre '{seq1}' et '{seq2}' est : {distance}")
    elif choix_distance == '2':
        distance = distance_levenshtein(seq1, seq2)
        print(f"La distance de Levenshtein entre '{seq1}' et '{seq2}' est : {distance}")
    else:
        print("Choix invalide.")

def reconstruire_arbre_phylogenetique():
    """Gère la création d'un arbre à partir d'espèces générées aléatoirement."""
    while True:
        nb_especes_str = input("Combien d'espèces voulez-vous générer pour l'arbre ? (ex: 5) : ")
        if not nb_especes_str.isdigit():
            print("Erreur : Veuillez entrer un nombre entier positif.")
            continue
        nb_especes = int(nb_especes_str)
        if nb_especes < 2:
            print("Erreur : Il faut au moins 2 espèces pour construire un arbre.")
            continue
        break

    while True:
        longueur_min_str = input("Longueur minimale de l'ADN pour chaque espèce ? (ex: 10) : ")
        longueur_max_str = input("Longueur maximale de l'ADN pour chaque espèce ? (ex: 20) : ")
        if not (longueur_min_str.isdigit() and longueur_max_str.isdigit()):
            print("Erreur : Veuillez entrer des nombres entiers positifs.")
            continue
        longueur_min = int(longueur_min_str)
        longueur_max = int(longueur_max_str)
        if longueur_min <= 0 or longueur_max <= 0 or longueur_min > longueur_max:
            print("Erreur : Les longueurs doivent être des entiers positifs et min <= max.")
            continue
        break

    print("--- Génération des espèces ---")
    especes = []
    for i in range(nb_especes):
        nom = f"Espece_{i+1}"
        longueur_adn = random.randint(longueur_min, longueur_max)
        adn = generer_sequence_adn_aleatoire(longueur_adn)
        espece = Espece(nom, adn)
        especes.append(espece)
        print(f"Création de {nom} avec ADN de longueur {len(adn)}")

    print("--- Reconstruction de l'arbre ---")

    arbre_final = reconstruire_arbre(especes)

    print("--- Structure de l'arbre final ---")
    afficher_arbre(arbre_final)

def afficher_arbre(noeud, prefixe="", est_dernier=True):
    """Affiche la structure de l'arbre de manière récursive."""
    print(prefixe + ("└── " if est_dernier else "├── ") + noeud.nom)
    
    if hasattr(noeud, 'especes_filles'):
        enfants = noeud.especes_filles
        nouveau_prefixe = prefixe + ("    " if est_dernier else "│   ")
        for enfant in enfants[:-1]:
            afficher_arbre(enfant, nouveau_prefixe, False)
        if enfants:
            afficher_arbre(enfants[-1], nouveau_prefixe, True)

def main():
    """Fonction principale de l'application."""
    print("Bienvenue dans l'outil d'analyse phylogénétique !")
    while True:
        choix = menu_principal()
        if choix == '1':
            generer_sequence()
        elif choix == '2':
            muter_sequence()
        elif choix == '3':
            calculer_distance_sequences()
        elif choix == '4':
            reconstruire_arbre_phylogenetique()
        elif choix == '0':
            print("Au revoir !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
