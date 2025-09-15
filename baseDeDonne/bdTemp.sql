CREATE TABLE Plateforme (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100),
    nb_personnes_necessaires INT,
    cout_journalier DECIMAL(10,2),
    habilitations_requises TEXT,
    intervalle_maintenance INT
);

CREATE TABLE Personnel (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100),
    habilitations TEXT
);

CREATE TABLE Campagne (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date_debut DATE,
    duree INT,
    lieu VARCHAR(100),
    plateforme_id INT,
    FOREIGN KEY (plateforme_id) REFERENCES Plateforme(id)
);

CREATE TABLE Echantillon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fichier_sequence VARCHAR(255),
    commentaire TEXT,
    campagne_id INT,
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id)
);

CREATE TABLE Maintenance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date_maintenance DATE,
    duree INT,
    type_operation VARCHAR(100),
    plateforme_id INT,
    FOREIGN KEY (plateforme_id) REFERENCES Plateforme(id)
);

CREATE TABLE Budget (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mois DATE,
    montant DECIMAL(12,2)
);

CREATE TABLE Implique (
    campagne_id INT,
    personnel_id INT,
    PRIMARY KEY (campagne_id, personnel_id),
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(id)
);

CREATE TABLE Participe (
    echantillon_id INT,
    personnel_id INT,
    PRIMARY KEY (echantillon_id, personnel_id),
    FOREIGN KEY (echantillon_id) REFERENCES Echantillon(id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(id)
);

CREATE TABLE Valide (
    budget_id INT,
    campagne_id INT,
    PRIMARY KEY (budget_id, campagne_id),
    FOREIGN KEY (budget_id) REFERENCES Budget(id),
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id)
);
