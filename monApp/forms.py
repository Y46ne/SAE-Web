from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, DateField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, NumberRange, Optional
from flask_wtf.file import FileField, FileRequired
from .models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur", 
        validators=[DataRequired(), Length(min=4, max=80)]
    )
    password = PasswordField(
        'Mot de passe', 
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe', 
        validators=[DataRequired(), EqualTo('password')]
    )
    role = SelectField(
        'Rôle',
        validators=[DataRequired()]
    )
    submit = SubmitField('Créer le compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')



class HabilitationForm(FlaskForm):
    nomHab = StringField('Nom de l\'habilitation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class BudgetForm(FlaskForm):
    mois = DateField('Mois (AAAA-MM-JJ)', format='%Y-%m-%d', validators=[DataRequired()])
    montant = DecimalField('Montant du budget', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')



class PlateformeForm(FlaskForm):
    nom = StringField('Nom de la plateforme', validators=[DataRequired()])
    nb_personnes_necessaires = IntegerField('Personnel nécessaire', validators=[DataRequired(), NumberRange(min=1)])
    cout_journalier = DecimalField('Coût journalier', validators=[DataRequired()])
    intervalle_maintenance = IntegerField('Intervalle maintenance (jours)', validators=[DataRequired()])
    
    habilitations_requises = SelectMultipleField(
        'Habilitations requises',
        coerce=int,
        validators=[Optional()] 
    )
    submit = SubmitField('Enregistrer')


class PersonnelForm(FlaskForm):
    nom = StringField('Nom du personnel', validators=[DataRequired()])
    
    habilitations = SelectMultipleField(
        'Habilitations possédées',
        coerce=int,
        validators=[Optional()]
    )
    submit = SubmitField('Enregistrer')


class CampagneForm(FlaskForm):
    nom = StringField('Nom de la Campagne', validators=[DataRequired()])
    date_debut = DateField('Date de début', format='%Y-%m-%d', validators=[DataRequired()])
    duree = IntegerField('Durée (jours)', validators=[DataRequired(), NumberRange(min=1, max=365)])
    lieu = StringField('Lieu', validators=[DataRequired()])
    
    plateforme = SelectField( # On garde SelectField, mais on va gérer la validation différemment
        'Plateforme',
        validators=[DataRequired(message="Veuillez sélectionner une plateforme.")],
        coerce=int
    )

    personnel_implique = SelectMultipleField(
        'Personnel impliqué',
        coerce=int,
        validators=[DataRequired(message="Veuillez sélectionner au moins un membre du personnel.")]
    )
    submit = SubmitField('Enregistrer')


class EchantillonForm(FlaskForm):
    fichier_sequence = FileField('Fichier séquence', validators=[FileRequired(message="Veuillez sélectionner un fichier.")])
    commentaire = TextAreaField('Commentaire')
    
    campagne = SelectField(
        'Campagne associée',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Enregistrer')


class MaintenanceForm(FlaskForm):
    date_maintenance = DateField('Date de maintenance', format='%Y-%m-%d', validators=[DataRequired()])
    duree = IntegerField('Durée (jours)', validators=[DataRequired()])
    type_operation = StringField('Type d\'opération', validators=[DataRequired()])
    
    plateforme = SelectField(
        'Plateforme concernée',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Enregistrer')

class ValidationBudgetForm(FlaskForm):
    submit = SubmitField('Valider le budget pour cette campagne')