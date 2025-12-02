-- 1. validation des dates et durée de campagne

DELIMITER |

CREATE OR REPLACE TRIGGER validate_campagne_duree_insert
BEFORE INSERT ON CAMPAGNE
FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La durée doit être comprise entre 1 et 365 jours';
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE OR REPLACE TRIGGER validate_campagne_duree_update
BEFORE UPDATE ON CAMPAGNE
FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La durée doit être comprise entre 1 et 365 jours';
    END IF;
END |

DELIMITER ;

-- 2. contrôle du nombre de personnes par campagne

DELIMITER |
CREATE OR REPLACE TRIGGER check_nb_personnes_insert
AFTER INSERT ON IMPLIQUE
FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE msg TEXT;

    SELECT idPl INTO idPl_camp FROM CAMPAGNE WHERE idCamp = NEW.idCamp;
    SELECT nb_personnes_necessaires INTO nb_requis FROM PLATEFORME WHERE idPl = idPl_camp;
    SELECT COUNT(*) INTO nb_actuel FROM IMPLIQUE WHERE idCamp = NEW.idCamp;

    IF nb_actuel > nb_requis THEN
        SET msg = CONCAT('Il y a trop de personnes assignées à la campagne ', NEW.idCamp);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END |
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER check_nb_personnes_update
AFTER UPDATE ON IMPLIQUE
FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE msg TEXT;

    SELECT idPl INTO idPl_camp FROM CAMPAGNE WHERE idCamp = NEW.idCamp;
    SELECT nb_personnes_necessaires INTO nb_requis FROM PLATEFORME WHERE idPl = idPl_camp;
    SELECT COUNT(*) INTO nb_actuel FROM IMPLIQUE WHERE idCamp = NEW.idCamp;

    IF nb_actuel > nb_requis THEN
        SET msg = CONCAT('Il y a trop de personnes assignées à la campagne ', NEW.idCamp);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END |
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER check_nb_personnes_delete
AFTER DELETE ON IMPLIQUE
FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE msg TEXT;

    SELECT idPl INTO idPl_camp FROM CAMPAGNE WHERE idCamp = OLD.idCamp;
    SELECT nb_personnes_necessaires INTO nb_requis FROM PLATEFORME WHERE idPl = idPl_camp;
    SELECT COUNT(*) INTO nb_actuel FROM IMPLIQUE WHERE idCamp = OLD.idCamp;

    IF nb_actuel > nb_requis THEN
        SET msg = CONCAT('Il y a trop de personnes assignées à la campagne ', OLD.idCamp);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END |
DELIMITER ;

-- 3. contrôle des habilitations du personnel

DELIMITER |
CREATE OR REPLACE TRIGGER check_habilitations_insert
BEFORE INSERT ON IMPLIQUE
FOR EACH ROW
BEGIN
    DECLARE nb_hab_requises INT;
    DECLARE nb_hab_possedees INT;
    DECLARE idPl_camp INT;

    SELECT idPl INTO idPl_camp FROM CAMPAGNE WHERE idCamp = NEW.idCamp;

    SELECT COUNT(*) INTO nb_hab_requises FROM REQUIERT WHERE idPl = idPl_camp;

    SELECT COUNT(*) INTO nb_hab_possedees
    FROM REQUIERT r
    JOIN POSSEDE p ON r.idHab = p.idHab
    WHERE r.idPl = idPl_camp AND p.idPers = NEW.idPers;

    IF nb_hab_possedees < nb_hab_requises THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le personnel n’a pas toutes les habilitations requises pour cette campagne.';
    END IF;
END |
DELIMITER ;

-- 4. contrôle du budget validant

DELIMITER |
CREATE OR REPLACE TRIGGER check_budget_valide
BEFORE INSERT ON VALIDE
FOR EACH ROW
BEGIN
    DECLARE cout_total DECIMAL(10,2);
    DECLARE montant_budget DECIMAL(10,2);

    SELECT c.duree * p.cout_journalier INTO cout_total
    FROM CAMPAGNE c
    JOIN PLATEFORME p ON c.idPl = p.idPl
    WHERE c.idCamp = NEW.idCamp;

    SELECT montant INTO montant_budget FROM BUDGET WHERE idBudg = NEW.idBudg;

    IF montant_budget < cout_total THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le budget est insuffisant pour couvrir le coût total de la campagne';
    END IF;
END |
DELIMITER ;

-- 5. limiter le nombre d’échantillons par campagne 

DELIMITER |
CREATE OR REPLACE TRIGGER limit_echantillons_insert
BEFORE INSERT ON ECHANTILLON
FOR EACH ROW
BEGIN
    DECLARE nb_ech INT;

    SELECT COUNT(*) INTO nb_ech FROM ECHANTILLON WHERE idCamp = NEW.idCamp;

    IF nb_ech >= 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Nombre maximum d’échantillons atteint pour cette campagne';
    END IF;
END |
DELIMITER ;

-- 6. décrémente le budget validé après une campagne

DELIMITER |
CREATE OR REPLACE TRIGGER maj_budget_apres_validation_insert
AFTER INSERT ON VALIDE
FOR EACH ROW
BEGIN
    UPDATE BUDGET
    SET montant = montant - (
        SELECT (p.cout_journalier * c.duree)
        FROM CAMPAGNE c
        JOIN PLATEFORME p ON c.idPl = p.idPl
        WHERE c.idCamp = NEW.idCamp
    )
    WHERE idBudg = NEW.idBudg;
END |
DELIMITER ;


DELIMITER |
CREATE OR REPLACE TRIGGER maj_budget_apres_validation_update
AFTER UPDATE ON VALIDE
FOR EACH ROW
BEGIN
    UPDATE BUDGET
    SET montant = montant - (
        SELECT (p.cout_journalier * c.duree)
        FROM CAMPAGNE c
        JOIN PLATEFORME p ON c.idPl = p.idPl
        WHERE c.idCamp = NEW.idCamp
    )
    WHERE idBudg = NEW.idBudg;
END |
DELIMITER ;