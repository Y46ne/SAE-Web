-- Plateformes
INSERT INTO PLATEFORME (idPl, nom, nb_personnes_necessaires, cout_journalier, habilitations_requises, intervalle_maintenance)
VALUES
(1, 'Plateforme Alpha', 3, 1200, 'HAB1,HAB2', 30),
(2, 'Plateforme Beta', 2, 800, 'HAB2', 45);

-- Personnel
INSERT INTO PERSONNEL (idPers, nom, habilitations)
VALUES
(1, 'Dupont', 'HAB1,HAB2'),
(2, 'Martin', 'HAB2'),
(3, 'Durand', 'HAB3');

-- Campagnes
INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES
(1, '2025-01-10', 15, 'Brest', 1),
(2, '2025-02-05', 10, 'Nantes', 2);

-- Echantillons
INSERT INTO ECHANTILLON (idEch, fichier_sequence, commentaire, idCamp)
VALUES
(1, 'seq_001.fasta', 'Premier échantillon', 1),
(2, 'seq_002.fasta', 'Contrôle qualité', 1),
(3, 'seq_003.fasta', 'Deuxième campagne', 2);

-- Maintenance
INSERT INTO MAINTENANCE (idMaint, date_maintenance, duree, type_operation, idPl)
VALUES
(1, '2025-01-01', 2, 'Révision générale', 1),
(2, '2025-02-01', 1, 'Calibration', 2);

-- Budget
INSERT INTO BUDGET (idBudg, mois, montant)
VALUES
(1, '2025-01-01', 50000),
(2, '2025-02-01', 45000);

-- Implique (personnel impliqué dans les campagnes)
INSERT INTO IMPLIQUE (idCamp, idPers)
VALUES
(1, 1),
(1, 2),
(2, 3);

-- Participe (personnel ayant travaillé sur des échantillons)
INSERT INTO PARTICIPE (idEch, idPers)
VALUES
(1, 1),
(2, 2),
(3, 3);

-- Valide (budget validant une campagne)
INSERT INTO VALIDE (idBudg, idCamp)
VALUES
(1, 1),
(2, 2);
