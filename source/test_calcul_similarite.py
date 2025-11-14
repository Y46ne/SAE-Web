import pytest
from calculSimilarite import *

#GÉNÉRÉ PAR CHATGPT


# ----------------------------
# Tests pour distance_remplacement
# ----------------------------
def test_distance_remplacement_identiques():
    assert distance_remplacement("ATGC", "ATGC") == 0

def test_distance_remplacement_une_difference():
    assert distance_remplacement("ATGC", "ATGT") == 1

def test_distance_remplacement_plusieurs_differences():
    assert distance_remplacement("AAAA", "TTTT") == 4

def test_distance_remplacement_tailles_diff():
    assert distance_remplacement("ATGC", "ATG") is None

def test_distance_remplacement_vide():
    assert distance_remplacement("", "") == 0


# ----------------------------
# Tests pour distance_levenshtein
# ----------------------------
def test_levenshtein_identiques():
    assert distance_levenshtein("ATGC", "ATGC") == 0

def test_levenshtein_insertion():
    # Exemple : insérer "A" dans "TGC" pour obtenir "ATGC"
    assert distance_levenshtein("TGC", "ATGC") == 1

def test_levenshtein_suppression():
    # Exemple : supprimer "A" de "ATGC" pour obtenir "TGC"
    assert distance_levenshtein("ATGC", "TGC") == 1

def test_levenshtein_remplacement():
    # Exemple : "A" -> "T"
    assert distance_levenshtein("A", "T") == 1

def test_levenshtein_complexe():
    # Plusieurs modifications : "GATTACA" -> "GCATGCU"
    assert distance_levenshtein("GATTACA", "GCATGCU") == 4

def test_levenshtein_avec_vide():
    assert distance_levenshtein("", "ATGC") == 4
    assert distance_levenshtein("ATGC", "") == 4
    assert distance_levenshtein("", "") == 0
