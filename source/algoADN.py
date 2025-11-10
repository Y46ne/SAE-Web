import random
from constantes import *


def generer_sequence_adn_aleatoire(longueur: int):
    """Génère une séquence ADN aléatoire d'une longueur spécifiée.

    Args:
        longueur (int): La longueur désirée de la séquence ADN.

    Returns:
        str: La séquence ADN générée.
    """
    sequence = ""
    for i in range(longueur):
        lettre=random.choice(bases)
        sequence+=lettre
    return sequence
   


def muter_remplacement(sequence:str, p:float):
    """
    Muter une séquence par remplacement aléatoire avec un taux p.
    
    Args:
        sequence (str): Séquence d'ADN originale.
        p (float): Probabilité de mutation pour chaque base (entre 0 et 1).
        
    Returns:
        str: Séquence mutée.
    """
    sequence_mutée = ""  
    for base in sequence:
        if random.random() < p:
            nouvelles_bases = []
            for b in bases:
                if b != base:
                    nouvelles_bases.append(b)
            base = random.choice(nouvelles_bases)
        sequence_mutée += base  
    return sequence_mutée




def muter_complet(sequence, p_remplacement, p_insertion, p_delation):
    """
    Appliquer trois types de mutations sur une séquence : remplacement, insertion, délétion.
    
    Args:
        sequence (str): Séquence d'ADN originale.
        p_remplacement (float): Probabilité de remplacer une base.
        p_insertion (float): Probabilité d'insérer une nouvelle base avant la base actuelle.
        p_delation (float): Probabilité de supprimer la base actuelle.
        
    Returns:
        str: Séquence mutée.
    """
    sequence_mutée = "" 
    for base in sequence:
        if random.random() < p_delation:
            continue
        if random.random() < p_insertion:
            sequence_mutée += random.choice(bases)
        if random.random() < p_remplacement:
            nouvelles_bases = []
            for b in bases:
                if b != base:
                    nouvelles_bases.append(b)
            base = random.choice(nouvelles_bases)
        sequence_mutée += base
    return sequence_mutée
