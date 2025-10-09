
-- 1. Coût total de chaque campagne
SELECT idCamp, lieu, (duree * cout_journalier) AS cout_total
FROM CAMPAGNE
NATURAL JOIN PLATEFORME;

-- 2. Lister le personnel impliqué dans chaque campagne
SELECT nom AS personnel, idCamp, lieu AS campagne
FROM PERSONNEL
NATURAL JOIN IMPLIQUE
NATURAL JOIN CAMPAGNE;

-- 3. Tous les échantillons avec leur campagne et plateforme
SELECT idEch, fichier_sequence, lieu AS campagne, nom AS plateforme
FROM ECHANTILLON
NATURAL JOIN CAMPAGNE
NATURAL JOIN PLATEFORME;

-- 4. Qui a participé à la collecte de quel échantillon
SELECT pers.nom AS personnel, e.fichier_sequence, c.lieu AS campagne
FROM PARTICIPE
NATURAL JOIN ECHANTILLON e
NATURAL JOIN PERSONNEL pers
NATURAL JOIN CAMPAGNE c;

-- 5. Budgets validant les campagnes
SELECT idCamp, lieu, mois, montant
FROM VALIDE
NATURAL JOIN BUDGET
NATURAL JOIN CAMPAGNE;

-- 6. Nombre de campagnes par plateforme
SELECT nom AS plateforme, COUNT(idCamp) AS nb_campagnes
FROM PLATEFORME
NATURAL LEFT JOIN CAMPAGNE
GROUP BY nom;

-- 7. Maintenances planifiées avec la plateforme associée
SELECT date_maintenance, type_operation, nom AS plateforme
FROM MAINTENANCE
NATURAL JOIN PLATEFORME;

-- 8. Lister les habilitations requises pour chaque plateforme
SELECT nom AS plateforme, nomHab AS habilitation_requise
FROM PLATEFORME
NATURAL JOIN REQUIERT
NATURAL JOIN HABILITATION
ORDER BY nom;

-- 9. Lister les habilitations de chaque membre du personnel
SELECT nom, nomHab AS habilitation
FROM PERSONNEL
NATURAL JOIN POSSEDE
NATURAL JOIN HABILITATION
ORDER BY nom;

-- 10. Coût total des campagnes regroupées par plateforme
SELECT nom AS plateforme, SUM(duree * cout_journalier) AS cout_total_par_plateforme
FROM PLATEFORME
NATURAL JOIN CAMPAGNE
GROUP BY nom;

-- 11. Échantillons d’une campagne spécifique (ex: campagne 1)
SELECT idEch, fichier_sequence, commentaire
FROM ECHANTILLON
WHERE idCamp = 1;

-- 12. Personnel impliqué dans une campagne spécifique (ex: campagne 3)
SELECT lieu, nom AS personnel
FROM IMPLIQUE
NATURAL JOIN CAMPAGNE
NATURAL JOIN PERSONNEL
WHERE idCamp = 3;

-- 13. Personnel ayant l'habilitation 'Biologique'
SELECT nom
FROM PERSONNEL
NATURAL JOIN POSSEDE
NATURAL JOIN HABILITATION
WHERE nomHab = 'Biologique';

-- 14. Plateformes qui requièrent l'habilitation 'Electrique'
SELECT nom AS plateforme
FROM PLATEFORME
NATURAL JOIN REQUIERT
NATURAL JOIN HABILITATION
WHERE nomHab = 'Electrique';

-- 15. Personnel qui n'est impliqué dans AUCUNE campagne
SELECT nom
FROM PERSONNEL
NATURAL LEFT JOIN IMPLIQUE
WHERE idCamp IS NULL;