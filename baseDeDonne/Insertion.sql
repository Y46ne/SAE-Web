INSERT INTO HABILITATION (idHab, nomHab)
VALUES
(1, 'Electrique'),
(2, 'Chimique'),
(3, 'Biologique'),
(4, 'Radiations');

INSERT INTO PLATEFORME (idPl, nom, nb_personnes_necessaires, cout_journalier, intervalle_maintenance)
VALUES
(1, 'Plateforme Alpha', 3, 1200.00, 30),
(2, 'Plateforme Beta', 2, 800.00, 45),
(3, 'Plateforme Gamma', 4, 1500.00, 60),
(4, 'Plateforme Delta', 3, 1000.00, 30),
(5, 'Plateforme Epsilon', 5, 1800.00, 90);

INSERT INTO REQUIERT (idPl, idHab)
VALUES
(1, 1), (1, 2),
(2, 2),
(3, 1), (3, 3),
(4, 3),
(5, 2), (5, 4);

INSERT INTO PERSONNEL (idPers, nom)
VALUES
(1, 'Dupont'),
(2, 'Martin'),
(3, 'Durand'),
(4, 'Petit'),
(5, 'Bernard'),
(6, 'Roux'),
(7, 'Garcia'),
(8, 'Fournier'),
(9, 'Morel'),
(10, 'Lambert');

INSERT INTO POSSEDE (idPers, idHab)
VALUES
(1, 1), (1, 2),
(2, 2),
(3, 3),
(4, 1), (4, 3),
(5, 2), (5, 4),
(6, 1),
(7, 3), (7, 4),
(8, 2), (8, 3),
(9, 4),
(10, 1), (10, 2), (10, 3);

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

INSERT INTO MAINTENANCE (idMaint, date_maintenance, duree, type_operation, idPl)
VALUES
(1, '2025-10-01', 2, 'Révision générale', 1),
(2, '2025-10-02', 1, 'Calibration', 2),
(3, '2025-10-03', 3, 'Mise à jour système', 3),
(4, '2025-10-04', 2, 'Nettoyage', 4),
(5, '2025-10-05', 4, 'Remplacement capteur', 5);

INSERT INTO BUDGET (idBudg, mois, montant)
VALUES
(1, '2025-10-01', 50000.00),
(2, '2025-10-01', 45000.00),
(3, '2025-10-01', 60000.00),
(4, '2025-10-01', 55000.00),
(5, '2025-10-01', 48000.00);

INSERT INTO IMPLIQUE (idCamp, idPers)
VALUES
(1, 1),
(1, 10),
(2, 2),
(3, 4),
(3, 10),
(4, 3),
(5, 5);

INSERT INTO PARTICIPE (idEch, idPers)
VALUES
(1, 1),
(2, 10),
(3, 2),
(4, 4),
(5, 10),
(6, 3),
(7, 5);

INSERT INTO VALIDE (idBudg, idCamp)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
