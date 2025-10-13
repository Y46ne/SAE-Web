import random
from algoADN import *
from constantes import *  

random.seed(42)

print("=== Test Génération de séquences aléatoires ===")
for i in range(5):
    seq = generer_sequence_adn_aleatoire(8)
    print(f"Séquence {i+1} : {seq}")
print("\n")

print("=== Test Mutation par remplacement ===")
for i in range(5):
    seq = generer_sequence_adn_aleatoire(8)
    seq_mutée = muter_remplacement(seq, 0.3)
    print(f"Original : {seq} -> Mutée : {seq_mutée}")
print("\n")

print("=== Test Mutation complète (remplacement + insertion + délétion) ===")
for i in range(5):
    seq = generer_sequence_adn_aleatoire(8)
    seq_mutée = muter_complet(seq, p_remplacement=0.3, p_insertion=0.2, p_delation=0.1)
    print(f"Original : {seq} -> Mutée complète : {seq_mutée}")
print("\n")
