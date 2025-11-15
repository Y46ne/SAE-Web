from Espece import Espece
from EspeceHypothetique import EspeceHypothetique

def distance_adn(adn1, adn2):

    return abs(len(adn1) - len(adn2))


def calculer_distance(espece1, espece2):

    if not isinstance(espece1, EspeceHypothetique) and not isinstance(espece2, EspeceHypothetique):
        return distance_adn(espece1.adn, espece2.adn)

    elif isinstance(espece1, EspeceHypothetique) and not isinstance(espece2, EspeceHypothetique):
        dist1 = calculer_distance(espece1.especes_filles[0], espece2)
        dist2 = calculer_distance(espece1.especes_filles[1], espece2)
        return (dist1 + dist2) / 2

    elif not isinstance(espece1, EspeceHypothetique) and isinstance(espece2, EspeceHypothetique):
        return calculer_distance(espece2, espece1)

    elif isinstance(espece1, EspeceHypothetique) and isinstance(espece2, EspeceHypothetique):
        dist1 = calculer_distance(espece1.especes_filles[0], espece2)
        dist2 = calculer_distance(espece1.especes_filles[1], espece2)
        return (dist1 + dist2) / 2
    else:
        return None


def reconstruire_arbre(liste_especes_initiales):

    especes_en_cours = list(liste_especes_initiales)
    
    while len(especes_en_cours) > 1:
        distance_min = None
        meilleure_paire = (None, None)
        for i in range(len(especes_en_cours)):
            for j in range(i + 1, len(especes_en_cours)):
                espece1 = especes_en_cours[i]
                espece2 = especes_en_cours[j]
                dist = calculer_distance(espece1, espece2)
                if distance_min is None or dist < distance_min:
                    distance_min = dist
                    meilleure_paire = (espece1, espece2)
        e1, e2 = meilleure_paire
        nom_ancetre = f"({e1.nom}+{e2.nom})"
        nouvel_ancetre = EspeceHypothetique(nom_ancetre, e1, e2)
        print(f"Fusion de {e1.nom} et {e2.nom} (distance={distance_min:.2f}) -> Nouvel ancêtre : {nouvel_ancetre.nom}")
        
        especes_en_cours.remove(e1)
        especes_en_cours.remove(e2)
        especes_en_cours.append(nouvel_ancetre)
        
    racine_arbre = especes_en_cours[0]
    print(f"\nArbre reconstruit ! Racine : {racine_arbre.nom}")
    return racine_arbre