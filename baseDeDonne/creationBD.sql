CREATE TABLE PLATEFORME (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    nb_personnes_necessaires INT,
    cout_journalier DECIMAL(10,2),
    habilitations_requises TEXT,
    intervalle_maintenance INT
);

CREATE TABLE PERSONNEL (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    habilitations TEXT
);

CREATE TABLE CAMPAGNE (
    id INT PRIMARY KEY,
    date_debut DATE,
    duree INT,
    lieu VARCHAR(100),
    plateforme_id INT,
    FOREIGN KEY (plateforme_id) REFERENCES PLATEFORME(id)
);

CREATE TABLE ECHANTILLON (
    id INT PRIMARY KEY,
    fichier_sequence VARCHAR(255),
    commentaire TEXT,
    campagne_id INT,
    FOREIGN KEY (campagne_id) REFERENCES CAMPAGNE(id)
);

CREATE TABLE MAINTENANCE (
    id INT PRIMARY KEY,
    date_maintenance DATE,
    duree INT,
    type_operation VARCHAR(100),
    plateforme_id INT,
    FOREIGN KEY (plateforme_id) REFERENCES PLATEFORME(id)
);

CREATE TABLE BUDGET (
    id INT PRIMARY KEY,
    mois DATE,
    montant DECIMAL(12,2)
);

CREATE TABLE IMPLIQUE (
    campagne_id INT,
    personnel_id INT,
    PRIMARY KEY (campagne_id, personnel_id),
    FOREIGN KEY (campagne_id) REFERENCES CAMPAGNE(id),
    FOREIGN KEY (personnel_id) REFERENCES PERSONNEL(id)
);

CREATE TABLE PARTICIPE (
    echantillon_id INT,
    personnel_id INT,
    PRIMARY KEY (echantillon_id, personnel_id),
    FOREIGN KEY (echantillon_id) REFERENCES ECHANTILLON(id),
    FOREIGN KEY (personnel_id) REFERENCES PERSONNEL(id)
);

CREATE TABLE VALIDE (
    budget_id INT,
    campagne_id INT,
    PRIMARY KEY (budget_id, campagne_id),
    FOREIGN KEY (budget_id) REFERENCES BUDGET(id),
    FOREIGN KEY (campagne_id) REFERENCES CAMPAGNE(id)
);
