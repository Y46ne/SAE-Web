def distance_remplacement(seq1,seq2):
    """
    Fonction qui calcul la distance entre 2 séquences.
    La distance correspondant au nombre de différences entre les 2 séquences

    Args:
        seq1 (str): séquence d'ADN
        seq2 (str): séquence d'ADN


    Returns:
        int: distance entre les 2 séquences
    """
    if len(seq1) != len(seq2):
        return None
    else:
        distance = 0
        for i in range(len(seq1)):
            if seq1[i] != seq2[i]:
                distance += 1
        return distance


# Fonction faites avec une assistance de l'IA ( elle m'a expliqué l'algorithme que je ne comprenais pas)
def distance_levenshtein(seq1,seq2):
    """
    Fonction qui calcul la distance de levenshtein entre 2 séquence d'ADN

    Args:
        seq1 (str): séquence d'ADN
        seq2 (str): séquence d'ADN

    Returns:
        int: distance entre les 2 séquences
    """
    n = len(seq1)
    m = len(seq2)

    matrice = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        matrice[i][0] = i
    for j in range(m + 1):
        matrice[0][j] = j

    # Remplir la matrice
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                cout_sub = 0
            else:
                cout_sub = 1

            matrice[i][j] = min(
                matrice[i - 1][j] + 1, # Suppression
                matrice[i][j - 1] + 1, # Insertion
                matrice[i - 1][j - 1] + cout_sub # Remplacement ou correspondance
            )

    return matrice[n][m]