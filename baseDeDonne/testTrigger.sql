
-- INSERTIONS DESTINÉES À FAIL


-- 1️Campagne avec date trop ancienne
INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES
(100, '2025-01-01', 10, 'TestVille', 1);

-- 2️campagne avec durée invalide
INSERT INTO CAMPAGNE (idCamp, date_debut, duree, lieu, idPl)
VALUES
(101, CURDATE(), 0, 'TestVille', 1);

-- 3️ Trop de personnes dans une campagne (nb_personnes_necessaires=2)
INSERT INTO IMPLIQUE (idCamp, idPers)
VALUES
(2, 1), (2, 2), (2, 3);

