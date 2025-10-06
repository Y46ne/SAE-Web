CREATE TABLE PLATEFORME (
    idPl INT PRIMARY KEY,
    nom VARCHAR(100),
    nb_personnes_necessaires INT,
    cout_journalier DECIMAL(10,2),
    habilitations_requises TEXT,
    intervalle_maintenance INT
);

CREATE TABLE PERSONNEL (
    idPers INT PRIMARY KEY,
    nom VARCHAR(100),
    habilitations TEXT
);

CREATE TABLE CAMPAGNE (
    idCamp INT PRIMARY KEY,
    date_debut DATE,
    duree INT,
    lieu VARCHAR(100),
    idPl INT,
    FOREIGN KEY (idPl) REFERENCES PLATEFORME(idPl)
);

CREATE TABLE ECHANTILLON (
    idEch INT PRIMARY KEY,
    fichier_sequence VARCHAR(255),
    commentaire TEXT,
    idCamp INT,
    FOREIGN KEY (idCamp) REFERENCES CAMPAGNE(idCamp)
);

CREATE TABLE MAINTENANCE (
    idMaint INT PRIMARY KEY,
    date_maintenance DATE,
    duree INT,
    type_operation VARCHAR(100),
    idPl INT,
    FOREIGN KEY (idPl) REFERENCES PLATEFORME(idPl)
);

CREATE TABLE BUDGET (
    idBudg INT PRIMARY KEY,
    mois DATE,
    montant DECIMAL(12,2)
);

CREATE TABLE IMPLIQUE (
    idCamp INT,
    idPers INT,
    PRIMARY KEY (idCamp, idPers),
    FOREIGN KEY (idCamp) REFERENCES CAMPAGNE(idCamp),
    FOREIGN KEY (idPers) REFERENCES PERSONNEL(idPers)
);

CREATE TABLE PARTICIPE (
    idEch INT,
    idPers INT,
    PRIMARY KEY (idEch, idPers),
    FOREIGN KEY (idEch) REFERENCES ECHANTILLON(idEch),
    FOREIGN KEY (idPers) REFERENCES PERSONNEL(idPers)
);

CREATE TABLE VALIDE (
    idBudg INT,
    idCamp INT,
    PRIMARY KEY (idBudg, idCamp),
    FOREIGN KEY (idBudg) REFERENCES BUDGET(idBudg),
    FOREIGN KEY (idCamp) REFERENCES CAMPAGNE(idCamp)
);
