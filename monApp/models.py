from flask_login import UserMixin
from .app import db
from datetime import date, timedelta
import enum

class UserRole(enum.Enum):
    ADMIN = 'admin'
    DIRECTION = 'direction'
    TECHNIQUE = 'technique'
    CHERCHEUR = 'chercheur'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CHERCHEUR)

    def __repr__(self):
        return f'<User {self.username}>'


implique = db.Table('IMPLIQUE',
    db.Column('idCamp', db.Integer, db.ForeignKey('CAMPAGNE.idCamp'), primary_key=True),
    db.Column('idPers', db.Integer, db.ForeignKey('PERSONNEL.idPers'), primary_key=True)
)

participe = db.Table('PARTICIPE',
    db.Column('idEch', db.Integer, db.ForeignKey('ECHANTILLON.idEch'), primary_key=True),
    db.Column('idPers', db.Integer, db.ForeignKey('PERSONNEL.idPers'), primary_key=True)
)

valide = db.Table('VALIDE',
    db.Column('idBudg', db.Integer, db.ForeignKey('BUDGET.idBudg'), primary_key=True),
    db.Column('idCamp', db.Integer, db.ForeignKey('CAMPAGNE.idCamp'), primary_key=True)
)

possede = db.Table('POSSEDE',
    db.Column('idPers', db.Integer, db.ForeignKey('PERSONNEL.idPers'), primary_key=True),
    db.Column('idHab', db.Integer, db.ForeignKey('HABILITATION.idHab'), primary_key=True)
)

requiert = db.Table('REQUIERT',
    db.Column('idPl', db.Integer, db.ForeignKey('PLATEFORME.idPl'), primary_key=True),
    db.Column('idHab', db.Integer, db.ForeignKey('HABILITATION.idHab'), primary_key=True)
)

class Plateforme(db.Model):
    __tablename__ = 'PLATEFORME'
    
    idPl = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    nb_personnes_necessaires = db.Column(db.Integer)
    cout_journalier = db.Column(db.Numeric(10, 2))
    intervalle_maintenance = db.Column(db.Integer)

    campagnes = db.relationship('Campagne', backref='plateforme', lazy=True)
    maintenances = db.relationship('Maintenance', backref='plateforme', lazy=True)
    
    habilitations_requises = db.relationship('Habilitation', secondary=requiert, 
                                             backref=db.backref('plateformes_requerantes', lazy=True))

    def __repr__(self):
        return f'<Plateforme {self.nom}>'


class Personnel(db.Model):
    __tablename__ = 'PERSONNEL'

    idPers = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))

    habilitations = db.relationship('Habilitation', secondary=possede, 
                                    backref=db.backref('personnel', lazy=True))
    
    campagnes = db.relationship('Campagne', secondary=implique, 
                                backref=db.backref('personnel_implique', lazy=True))
    
    echantillons = db.relationship('Echantillon', secondary=participe, 
                                   backref=db.backref('personnel_participant', lazy=True))

    def __repr__(self):
        return f'<Personnel {self.nom}>'


class Budget(db.Model):
    __tablename__ = 'BUDGET'

    idBudg = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.Date)
    montant = db.Column(db.Numeric(12, 2))

    campagnes_validees = db.relationship('Campagne', secondary=valide, 
                                         backref=db.backref('budgets_validants', lazy=True))

    def __repr__(self):
        return f'<Budget {self.idBudg} - {self.mois}>'

    @property
    def cout_total_campagnes(self):
        total_cost = 0
        for campagne in self.campagnes_validees:
            if campagne.plateforme and campagne.plateforme.cout_journalier is not None and campagne.duree is not None:
                total_cost += campagne.plateforme.cout_journalier * campagne.duree
        return total_cost


class Habilitation(db.Model):
    __tablename__ = 'HABILITATION'

    idHab = db.Column(db.Integer, primary_key=True)
    nomHab = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Habilitation {self.nomHab}>'

class Campagne(db.Model):
    __tablename__ = 'CAMPAGNE'

    idCamp = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    duree = db.Column(db.Integer)
    lieu = db.Column(db.String(100))
    
    idPl = db.Column(db.Integer, db.ForeignKey('PLATEFORME.idPl'))

    echantillons = db.relationship('Echantillon', backref='campagne', lazy=True)

    def __repr__(self):
        return f'<Campagne {self.idCamp} - {self.lieu}>'

    @property
    def statut(self):
        today = date.today()
        if self.date_debut > today:
            return "Prévue"
        elif self.date_debut <= today <= self.date_debut + timedelta(days=self.duree):
            return "En cours"
        else:
            return "Terminée"

    @property
    def statut_class(self):
        if self.statut == "Prévue":
            return "primary"
        elif self.statut == "En cours":
            return "success"
        else:
            return "danger"


class Echantillon(db.Model):
    __tablename__ = 'ECHANTILLON'

    idEch = db.Column(db.Integer, primary_key=True)
    fichier_sequence = db.Column(db.String(255))
    commentaire = db.Column(db.Text)
    
    idCamp = db.Column(db.Integer, db.ForeignKey('CAMPAGNE.idCamp'))

    def __repr__(self):
        return f'<Echantillon {self.idEch}>'


class Maintenance(db.Model):
    __tablename__ = 'MAINTENANCE'

    idMaint = db.Column(db.Integer, primary_key=True)
    date_maintenance = db.Column(db.Date)
    duree = db.Column(db.Integer)
    type_operation = db.Column(db.String(100))

    idPl = db.Column(db.Integer, db.ForeignKey('PLATEFORME.idPl'))

    def __repr__(self):
        return f'<Maintenance {self.type_operation} sur {self.idPl}>'