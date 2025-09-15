-- Plateformes
INSERT INTO Plateforme (id, nom, nb_personnes_necessaires, cout_journalier, habilitations_requises, intervalle_maintenance)
VALUES
(1, 'Plateforme Alpha', 3, 1200, 'HAB1,HAB2', 30),
(2, 'Plateforme Beta', 2, 800, 'HAB2', 45);

-- Personnel
INSERT INTO Personnel (id, nom, habilitations)
VALUES
(1, 'Dupont', 'HAB1,HAB2'),
(2, 'Martin', 'HAB2'),
(3, 'Durand', 'HAB3');

-- Campagnes
INSERT INTO Campagne (id, date_debut, duree, lieu, plateforme_id)
VALUES
(1, '2025-01-10', 15, 'Brest', 1),
(2, '2025-02-05', 10, 'Nantes', 2);

-- Echantillons
INSERT INTO Echantillon (id, fichier_sequence, commentaire, campagne_id)
VALUES
(1, 'seq_001.fasta', 'Premier échantillon', 1),
(2, 'seq_002.fasta', 'Contrôle qualité', 1),
(3, 'seq_003.fasta', 'Deuxième campagne', 2);

-- Maintenance
INSERT INTO Maintenance (id, date_maintenance, duree, type_operation, plateforme_id)
VALUES
(1, '2025-01-01', 2, 'Révision générale', 1),
(2, '2025-02-01', 1, 'Calibration', 2);

-- Budget
INSERT INTO Budget (id, mois, montant)
VALUES
(1, '2025-01-01', 50000),
(2, '2025-02-01', 45000);

-- Implique (personnel impliqué dans les campagnes)
INSERT INTO Implique (campagne_id, personnel_id)
VALUES
(1, 1),
(1, 2),
(2, 3);

-- Participe (personnel ayant travaillé sur des échantillons)
INSERT INTO Participe (echantillon_id, personnel_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

-- Valide (budget validant une campagne)
INSERT INTO Valide (budget_id, campagne_id)
VALUES
(1, 1),
(2, 2);
