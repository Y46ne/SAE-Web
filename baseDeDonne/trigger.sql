DELIMITER |


-- 1. VALIDATION DES DATES & DURÉE DE CAMPAGNE


CREATE TRIGGER validate_campagne_dates_insert
BEFORE INSERT ON CAMPAGNE
FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La durée doit être comprise entre 1 et 365 jours';
    END IF;

    IF NEW.date_debut < DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La date de début ne peut pas être antérieure de plus de 30 jours';
    END IF;
END |

CREATE TRIGGER validate_campagne_dates_update
BEFORE UPDATE ON CAMPAGNE
FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La durée doit être comprise entre 1 et 365 jours';
    END IF;

    IF NEW.date_debut < DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La date de début ne peut pas être antérieure de plus de 30 jours';
    END IF;
END |


-- 2. CONTRÔLE DU NOMBRE DE PERSONNES PAR CAMPAGNE


CREATE TRIGGER check_nb_personnes_insert
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

CREATE TRIGGER check_nb_personnes_update
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

CREATE TRIGGER check_nb_personnes_delete
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


-- 3. CONTRÔLE DES HABILITATIONS DU PERSONNEL


CREATE TRIGGER check_habilitations_insert
BEFORE INSERT ON IMPLIQUE
FOR EACH ROW
BEGIN
    DECLARE reqs TEXT;
    DECLARE habs TEXT;

    SELECT p.habilitations_requises INTO reqs
    FROM PLATEFORME p
    JOIN CAMPAGNE c ON p.idPl = c.idPl
    WHERE c.idCamp = NEW.idCamp;

    SELECT habilitations INTO habs FROM PERSONNEL WHERE idPers = NEW.idPers;

    -- Vérification basique : toutes les habilitations requises doivent apparaître dans habs
    IF NOT FIND_IN_SET(SUBSTRING_INDEX(reqs, ',', 1), habs) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le personnel n’a pas les habilitations requises pour cette campagne';
    END IF;
END |


-- 4. CONTRÔLE DU BUDGET VALIDANT


CREATE TRIGGER check_budget_valide
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


-- 5. LIMITER LE NOMBRE D’ÉCHANTILLONS PAR CAMPAGNE
-- (exemple : max 10 échantillons)


CREATE TRIGGER limit_echantillons_insert
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
