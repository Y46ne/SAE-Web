CREATE TABLE Plateforme (
    id INTEGER PRIMARY KEY ,
    nom TEXT,
    nb_personnes_necessaires INTEGER,
    cout_journalier ,
    habilitations_requises TEXT,
    intervalle_maintenance INTEGER
);

CREATE TABLE Personnel (
    id INTEGER PRIMARY KEY ,
    nom TEXT,
    habilitations TEXT
);

CREATE TABLE Campagne (
    id INTEGER PRIMARY KEY ,
    date_debut DATE,
    duree INTEGER,
    lieu TEXT,
    plateforme_id INTEGER,
    FOREIGN KEY (plateforme_id) REFERENCES Plateforme(id)
);

CREATE TABLE Echantillon (
    id INTEGER PRIMARY KEY ,
    fichier_sequence TEXT,
    commentaire TEXT,
    campagne_id INTEGER,
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id)
);

CREATE TABLE Maintenance (
    id INTEGER PRIMARY KEY ,
    date_maintenance DATE,
    duree INTEGER,
    type_operation TEXT,
    plateforme_id INTEGER,
    FOREIGN KEY (plateforme_id) REFERENCES Plateforme(id)
);

CREATE TABLE Budget (
    id INTEGER PRIMARY KEY ,
    mois DATE,
    montant 
);

CREATE TABLE Implique (
    campagne_id INTEGER,
    personnel_id INTEGER,
    PRIMARY KEY (campagne_id, personnel_id),
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(id)
);

CREATE TABLE Participe (
    echantillon_id INTEGER,
    personnel_id INTEGER,
    PRIMARY KEY (echantillon_id, personnel_id),
    FOREIGN KEY (echantillon_id) REFERENCES Echantillon(id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(id)
);

CREATE TABLE Valide (
    budget_id INTEGER,
    campagne_id INTEGER,
    PRIMARY KEY (budget_id, campagne_id),
    FOREIGN KEY (budget_id) REFERENCES Budget(id),
    FOREIGN KEY (campagne_id) REFERENCES Campagne(id)
);
