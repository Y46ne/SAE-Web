-- Lister toutes les plateformes
SELECT * FROM Plateforme;

-- Lister tout le personnel
SELECT * FROM Personnel;

-- Campagnes et plateforme associée
SELECT c.id, c.date_debut, c.duree, c.lieu, p.nom AS plateforme
FROM Campagne c
JOIN Plateforme p ON c.plateforme_id = p.id;

-- Échantillons d’une campagne (ex: campagne 1)
SELECT e.id, e.fichier_sequence, e.commentaire
FROM Echantillon e
WHERE e.campagne_id = 1;

-- Maintenances prévues
SELECT m.date_maintenance, m.type_operation, p.nom AS plateforme
FROM Maintenance m
JOIN Plateforme p ON m.plateforme_id = p.id;

-- Personnel impliqué dans une campagne
SELECT c.id AS campagne_id, c.lieu, pers.nom
FROM Implique i
JOIN Campagne c ON i.campagne_id = c.id
JOIN Personnel pers ON i.personnel_id = pers.id
WHERE c.id = 1;

-- Qui a participé à quel échantillon
SELECT e.fichier_sequence, pers.nom
FROM Participe pa
JOIN Echantillon e ON pa.echantillon_id = e.id
JOIN Personnel pers ON pa.personnel_id = pers.id;

-- Budgets validant les campagnes
SELECT c.id AS campagne_id, c.lieu, b.mois, b.montant
FROM Valide v
JOIN Budget b ON v.budget_id = b.id
JOIN Campagne c ON v.campagne_id = c.id;

-- Nombre de campagnes par plateforme
SELECT p.nom AS plateforme, COUNT(c.id) AS nb_campagnes
FROM Plateforme p
LEFT JOIN Campagne c ON p.id = c.plateforme_id
GROUP BY p.nom;

-- Coût total d’une campagne
SELECT c.id AS campagne_id, c.lieu,
       (c.duree * p.cout_journalier) AS cout_total
FROM Campagne c
JOIN Plateforme p ON c.plateforme_id = p.id;