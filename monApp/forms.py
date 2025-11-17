from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    """Formulaire de création de compte."""
    username = StringField(
        "Nom d'utilisateur", 
        validators=[DataRequired(), Length(min=4, max=80, message="Le nom d'utilisateur doit contenir entre 4 et 80 caractères.")]
    )
    password = PasswordField(
        'Mot de passe', 
        validators=[DataRequired(), Length(min=6, message='Le mot de passe doit faire au moins 6 caractères.')]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe', 
        validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')]
    )
    submit = SubmitField('Créer le compte')

    def validate_username(self, username):
        """Vérifie si le nom d'utilisateur n'est pas déjà pris."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")

class LoginForm(FlaskForm):
    """Formulaire de connexion."""
    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired()]
    )
    submit = SubmitField('Se connecter')