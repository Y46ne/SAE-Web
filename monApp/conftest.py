import pytest
from monApp.app import app as flask_app, db
from monApp.models import User, UserRole
from hashlib import sha256


@pytest.fixture(scope='module')
def app():
    """Crée et configure une nouvelle instance de l'application pour chaque session de test."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base de données en mémoire
        "WTF_CSRF_ENABLED": False,  # Désactive les tokens CSRF pour les formulaires
        "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_ECHO": False
    })

    with flask_app.app_context():
        db.create_all()
        # Créer un utilisateur admin pour les tests nécessitant une authentification
        admin_user = User(username='admin_test', password=sha256('password'.encode()).hexdigest(), role=UserRole.ADMIN)
        db.session.add(admin_user)
        db.session.commit()
        yield flask_app
        db.drop_all()


@pytest.fixture()
def client(app):
    """Un client de test pour l'application."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Un runner pour les commandes CLI de l'application."""
    return app.test_cli_runner()