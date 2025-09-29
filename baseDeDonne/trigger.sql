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
    DECLARE plateforme_id_camp INT;
    DECLARE campagne_id INT;
    SET campagne_id = NEW.campagne_id;

    SELECT plateforme_id INTO plateforme_id_camp 
    FROM CAMPAGNE WHERE id = campagne_id;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE id = plateforme_id_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE campagne_id = campagne_id;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', campagne_id);
    END IF;
END |

CREATE TRIGGER check_nb_personnes_update AFTER UPDATE ON IMPLIQUE FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE plateforme_id_camp INT;
    DECLARE campagne_id INT;
    SET campagne_id = NEW.campagne_id;

    SELECT plateforme_id INTO plateforme_id_camp 
    FROM CAMPAGNE WHERE id = campagne_id;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE id = plateforme_id_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE campagne_id = campagne_id;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', campagne_id);
    END IF;
END |

CREATE TRIGGER check_nb_personnes_delete AFTER DELETE ON IMPLIQUE FOR EACH ROW
BEGIN
    DECLARE nb_actuel INT;
    DECLARE nb_requis INT;
    DECLARE plateforme_id_camp INT;
    DECLARE campagne_id INT;
    SET campagne_id = OLD.campagne_id;

    SELECT plateforme_id INTO plateforme_id_camp 
    FROM CAMPAGNE WHERE id = campagne_id;

    SELECT nb_personnes_necessaires INTO nb_requis 
    FROM PLATEFORME WHERE id = plateforme_id_camp;

    SELECT COUNT(*) INTO nb_actuel 
    FROM IMPLIQUE WHERE campagne_id = campagne_id;

    IF nb_actuel > nb_requis THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('Il y a trop de personnes assignées à la campagne ', campagne_id);
    END IF;
END |
DELIMITER ;