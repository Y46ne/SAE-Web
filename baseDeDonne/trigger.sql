--validation des dates de campagne
DELIMITER |
CREATE TRIGGER validate_campagne_dates_insert BEFORE INSERT ON CAMPAGNE FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La durée doit être entre 1 et 365 jours';
    END IF;
    IF NEW.date_debut < DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La date ne peut pas être dans le passé';
    END IF;
END |

CREATE TRIGGER validate_campagne_dates_update BEFORE UPDATE ON CAMPAGNE FOR EACH ROW
BEGIN
    IF NEW.duree <= 0 OR NEW.duree > 365 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La durée doit être entre 1 et 365 jours';
    END IF;
    IF NEW.date_debut < DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La date ne peut pas être dans le passé';
    END IF;
END |
DELIMITER ;

--contrôle du nombre de personnes par campagne
DELIMITER |
CREATE TRIGGER check_nb_personnes_insert AFTER INSERT ON IMPLIQUE FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE idCamp INT;
    SET idCamp = NEW.idCamp;

    SELECT idPl INTO idPl_camp 
    FROM CAMPAGNE WHERE idCamp = idCamp;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE idPl = idPl_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE idCamp = idCamp;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', idCamp);
    END IF;
END |

CREATE TRIGGER check_nb_personnes_update AFTER UPDATE ON IMPLIQUE FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE idCamp INT;
    SET idCamp = NEW.idCamp;

    SELECT idPl INTO idPl_camp 
    FROM CAMPAGNE WHERE idCamp = idCamp;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE idPl = idPl_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE idCamp = idCamp;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', idCamp);
    END IF;
END |

CREATE TRIGGER check_nb_personnes_delete AFTER DELETE ON IMPLIQUE FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE idPl_camp INT;
    DECLARE idCamp INT;
    SET idCamp = OLD.idCamp;

    SELECT idPl INTO idPl_camp 
    FROM CAMPAGNE WHERE idCamp = idCamp;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE idPl = idPl_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE idCamp = idCamp;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', idCamp);
    END IF;
END |
DELIMITER ;