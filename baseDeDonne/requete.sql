-- FICHIER D'EXPLORATION DE LA BASE DE DONNÉES

-- 1Coût total d'une campagne
SELECT idCamp, lieu, (duree * cout_journalier) AS cout_total
FROM CAMPAGNE
NATURAL JOIN PLATEFORME;

-- 2Lister tout le personnel avec leurs campagnes
SELECT nom AS personnel, idCamp, lieu AS campagne
FROM PERSONNEL
NATURAL JOIN IMPLIQUE
NATURAL JOIN CAMPAGNE;

-- 3Tous les échantillons avec leur campagne et plateforme
SELECT idEch, fichier_sequence, commentaire, lieu AS campagne, nom AS plateforme
FROM ECHANTILLON
NATURAL JOIN CAMPAGNE
NATURAL JOIN PLATEFORME;

-- 4Qui a participé à quel échantillon
SELECT pers.nom AS personnel, e.fichier_sequence, c.lieu AS campagne
FROM PARTICIPE
NATURAL JOIN ECHANTILLON e
NATURAL JOIN CAMPAGNE c
NATURAL JOIN PERSONNEL pers;

-- 5Budgets validant les campagnes
SELECT c.idCamp, c.lieu, b.mois, b.montant
FROM VALIDE
NATURAL JOIN BUDGET b
NATURAL JOIN CAMPAGNE c;

-- 6Nombre de campagnes par plateforme
SELECT nom AS plateforme, COUNT(idCamp) AS nb_campagnes
FROM PLATEFORME
NATURAL LEFT JOIN CAMPAGNE
GROUP BY nom;

-- 7Maintenances planifiées avec la plateforme
SELECT date_maintenance, type_operation, nom AS plateforme
FROM MAINTENANCE
NATURAL JOIN PLATEFORME;

-- 8Personnel et budgets validés pour ses campagnes
SELECT pers.nom AS personnel, c.idCamp, c.lieu, b.montant
FROM PERSONNEL pers
NATURAL JOIN IMPLIQUE
NATURAL JOIN CAMPAGNE c
NATURAL JOIN VALIDE
NATURAL JOIN BUDGET b;

-- 9oût total des campagnes par plateforme
SELECT nom AS plateforme, SUM(duree * cout_journalier) AS cout_total
FROM PLATEFORME
NATURAL JOIN CAMPAGNE
GROUP BY nom;

-- Échantillons d’une campagne spécifique (ex: campagne 1)
SELECT e.idEch, e.fichier_sequence, e.commentaire
FROM ECHANTILLON e
WHERE e.idCamp = 1;

-- 11Personnel impliqué dans une campagne spécifique
SELECT c.idCamp AS campagne_id, c.lieu, pers.nom
FROM IMPLIQUE i
JOIN CAMPAGNE c ON i.idCamp = c.idCamp
JOIN PERSONNEL pers ON i.idPers = pers.idPers
WHERE c.idCamp = 1;

-- 12Total des budgets validés par campagne
SELECT c.idCamp, c.lieu, SUM(b.montant) AS total_budget
FROM VALIDE
NATURAL JOIN BUDGET b
NATURAL JOIN CAMPAGNE c
GROUP BY c.idCamp, c.lieu;

-- 13Nombre d'échantillons par campagne
SELECT c.idCamp, c.lieu, COUNT(e.idEch) AS nb_echantillons
FROM CAMPAGNE c
LEFT JOIN ECHANTILLON e ON c.idCamp = e.idCamp
GROUP BY c.idCamp, c.lieu;

-- 14Personnes ayant participé à plusieurs échantillons
SELECT pers.nom, COUNT(pa.idEch) AS nb_echantillons
FROM PARTICIPE pa
NATURAL JOIN PERSONNEL pers
GROUP BY pers.nom
HAVING COUNT(pa.idEch) > 1;

-- 15Campagnes sans maintenance prévue
SELECT c.idCamp, c.lieu
FROM CAMPAGNE c
LEFT JOIN MAINTENANCE m ON c.idPl = m.idPl
WHERE m.idMaint IS NULL;

-- 16Campagnes avec budget supérieur à 50 000
SELECT c.idCamp, c.lieu, b.montant
FROM VALIDE
NATURAL JOIN BUDGET b
NATURAL JOIN CAMPAGNE c
WHERE b.montant > 50000;

-- 17Personnel avec habilitations spécifiques (ex: HAB2)
SELECT nom, habilitations
FROM PERSONNEL
WHERE FIND_IN_SET('HAB2', habilitations);

-- 18 Coût moyen par jour des plateformes
SELECT nom AS plateforme, cout_journalier
FROM PLATEFORME;

-- 19 Toutes les campagnes et leur nombre de participants
SELECT c.idCamp, c.lieu, COUNT(i.idPers) AS nb_personnes
FROM CAMPAGNE c
LEFT JOIN IMPLIQUE i ON c.idCamp = i.idCamp
GROUP BY c.idCamp, c.lieu;

-- 20 Échantillons et la personne qui y a participé (toutes campagnes)
SELECT e.idEch, e.fichier_sequence, pers.nom AS participant
FROM ECHANTILLON e
LEFT JOIN PARTICIPE pa ON e.idEch = pa.idEch
LEFT JOIN PERSONNEL pers ON pa.idPers = pers.idPers;
