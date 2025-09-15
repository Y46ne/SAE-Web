-- Supprimer les relations
DELETE FROM Valide;
DELETE FROM Participe;
DELETE FROM Implique;

-- Supprimer les entités dépendantes
DELETE FROM Echantillon;
DELETE FROM Maintenance;
DELETE FROM Campagne;

-- Supprimer les tables principales
DELETE FROM Budget;
DELETE FROM Personnel;
DELETE FROM Plateforme;
