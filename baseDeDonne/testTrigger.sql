-- INSERTIONS DESTINÉES À ÉCHOUER POUR VALIDER LES TRIGGERS

-- Test 1 : Tenter d'insérer une campagne avec une durée invalide 
-- TRIGGER TESTÉ : validate_campagne_dates_insert

INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES (100, CURDATE(), 0, 'Ville Test Trigger', 1);


-- Test 2 : Tenter d'ajouter trop de personnes à une campagne 
-- TRIGGER TESTÉ : check_nb_personnes_insert

INSERT INTO IMPLIQUE (idCamp, idPers) VALUES (2, 1);


-- Test 3 : Tenter d'ajouter du personnel qui n'a pas les bonnes habilitations 
-- TRIGGER TESTÉ : check_habilitations_insert

INSERT INTO IMPLIQUE (idCamp, idPers) VALUES (1, 3);


-- Test 4 : Tenter de valider une campagne avec un budget insuffisant
-- TRIGGER TESTÉ : check_budget_valide

INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES (101, CURDATE(), 50, 'Ville Chère', 5);

-- On essaie de valider cette campagne avec le budget le plus élevé (idBudg = 3, montant = 60000€)
INSERT INTO VALIDE (idBudg, idCamp) VALUES (3, 101);