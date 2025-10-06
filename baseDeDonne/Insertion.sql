
-- INSERTIONS DE DONNÉES TEST (VALIDES)


-- Plateformes
INSERT INTO PLATEFORME (idPl, nom, nb_personnes_necessaires, cout_journalier, habilitations_requises, intervalle_maintenance)
VALUES
(1, 'Plateforme Alpha', 3, 1200.00, 'HAB1,HAB2', 30),
(2, 'Plateforme Beta', 2, 800.00, 'HAB2', 45),
(3, 'Plateforme Gamma', 4, 1500.00, 'HAB1,HAB3', 60),
(4, 'Plateforme Delta', 3, 1000.00, 'HAB3', 30),
(5, 'Plateforme Epsilon', 5, 1800.00, 'HAB2,HAB4', 90);

-- Personnel
INSERT INTO PERSONNEL (idPers, nom, habilitations)
VALUES
(1, 'Dupont', 'HAB1,HAB2'),
(2, 'Martin', 'HAB2'),
(3, 'Durand', 'HAB3'),
(4, 'Petit', 'HAB1,HAB3'),
(5, 'Bernard', 'HAB2,HAB4'),
(6, 'Roux', 'HAB1'),
(7, 'Garcia', 'HAB3,HAB4'),
(8, 'Fournier', 'HAB2,HAB3'),
(9, 'Morel', 'HAB4'),
(10, 'Lambert', 'HAB1,HAB2,HAB3');

-- Campagnes (dates récentes pour passer le trigger)
INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES
(1, '2025-10-01', 15, 'Brest', 1),
(2, '2025-10-05', 10, 'Nantes', 2),
(3, '2025-10-10', 20, 'Lyon', 3),
(4, '2025-10-12', 25, 'Paris', 4),
(5, '2025-10-15', 18, 'Marseille', 5),
(6, '2025-10-18', 12, 'Toulouse', 2),
(7, '2025-10-20', 30, 'Bordeaux', 1),
(8, '2025-10-22', 10, 'Nice', 3),
(9, '2025-10-24', 22, 'Rennes', 4),
(10, '2025-10-26', 14, 'Lille', 5);

-- Échantillons
INSERT INTO ECHANTILLON (idEch, fichier_sequence, commentaire, idCamp)
VALUES
(1, 'seq_001.fasta', 'Premier échantillon', 1),
(2, 'seq_002.fasta', 'Contrôle qualité', 1),
(3, 'seq_003.fasta', 'Deuxième campagne', 2),
(4, 'seq_004.fasta', 'Analyse gamma', 3),
(5, 'seq_005.fasta', 'Test complémentaire', 3),
(6, 'seq_006.fasta', 'Mesure comparative', 4),
(7, 'seq_007.fasta', 'Campagne mer', 5),
(8, 'seq_008.fasta', 'Suivi microbiologique', 6),
(9, 'seq_009.fasta', 'Validation post-traitement', 7),
(10, 'seq_010.fasta', 'Échantillon de référence', 8);

-- Maintenance
INSERT INTO MAINTENANCE (idMaint, date_maintenance, duree, type_operation, idPl)
VALUES
(1, '2025-10-01', 2, 'Révision générale', 1),
(2, '2025-10-02', 1, 'Calibration', 2),
(3, '2025-10-03', 3, 'Mise à jour système', 3),
(4, '2025-10-04', 2, 'Nettoyage', 4),
(5, '2025-10-05', 4, 'Remplacement capteur', 5);

-- Budgets
INSERT INTO BUDGET (idBudg, mois, montant)
VALUES
(1, '2025-10-01', 50000.00),
(2, '2025-10-01', 45000.00),
(3, '2025-10-01', 60000.00),
(4, '2025-10-01', 55000.00),
(5, '2025-10-01', 48000.00);

-- Implique
INSERT INTO IMPLIQUE (idCamp, idPers)
VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(3, 5),
(4, 6),
(5, 7);

-- Participe
INSERT INTO PARTICIPE (idEch, idPers)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

-- Valide
INSERT INTO VALIDE (idBudg, idCamp)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
