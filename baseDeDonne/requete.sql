-- Coût total d'une campagne
SELECT c.idCamp AS campagne_id, c.lieu,
       (c.duree * p.cout_journalier) AS cout_total
FROM CAMPAGNE c
JOIN PLATEFORME p ON c.idPl = p.idPl;

-- Lister tout le personnel
SELECT * FROM PERSONNEL;

-- Campagnes et plateforme associée
SELECT c.idCamp, c.date_debut, c.duree, c.lieu, p.nom AS plateforme
FROM CAMPAGNE c
JOIN PLATEFORME p ON c.idPl = p.idPl;

-- Échantillons d’une campagne (ex: campagne 1)
SELECT e.idEch, e.fichier_sequence, e.commentaire
FROM ECHANTILLON e
WHERE e.idCamp = 1;

-- Maintenances prévues
SELECT m.date_maintenance, m.type_operation, p.nom AS plateforme
FROM MAINTENANCE m
JOIN PLATEFORME p ON m.idPl = p.idPl;

-- Personnel impliqué dans une campagne
SELECT c.idCamp AS campagne_id, c.lieu, pers.nom
FROM IMPLIQUE i
JOIN CAMPAGNE c ON i.idCamp = c.idCamp
JOIN PERSONNEL pers ON i.idPers = pers.idPers
WHERE c.idCamp = 1;

-- Qui a participé à quel échantillon
SELECT e.fichier_sequence, pers.nom
FROM PARTICIPE pa
JOIN ECHANTILLON e ON pa.idEch = e.idEch
JOIN PERSONNEL pers ON pa.idPers = pers.idPers;

-- Budgets validant les campagnes
SELECT c.idCamp AS campagne_id, c.lieu, b.mois, b.montant
FROM VALIDE v
JOIN BUDGET b ON v.idBudg = b.idBudg
JOIN CAMPAGNE c ON v.idCamp = c.idCamp;

-- Nombre de campagnes par plateforme
SELECT p.nom AS plateforme, COUNT(c.idCamp) AS nb_campagnes
FROM PLATEFORME p
LEFT JOIN CAMPAGNE c ON p.idPl = c.idPl
GROUP BY p.nom;

-- Coût total d’une campagne
SELECT c.id AS campagne_id, c.lieu,
       (c.duree * p.cout_journalier) AS cout_total
FROM Campagne c
JOIN Plateforme p ON c.plateforme_id = p.id;