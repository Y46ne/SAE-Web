import pytest
from hashlib import sha256
from monApp.app import app as flask_app, db as sqlalchemy_db
from monApp.models import User, UserRole, Personnel, Habilitation, Plateforme


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
        "SERVER_NAME": "localhost.localdomain"
    })

    with flask_app.app_context():
        sqlalchemy_db.create_all()
        populate_db(sqlalchemy_db)
        yield flask_app
        sqlalchemy_db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return sqlalchemy_db


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="admin", password="password"):
        return self._client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)


def populate_db(db):
    users_data = [
        ("admin", "password", UserRole.ADMIN),
        ("direction", "password", UserRole.DIRECTION),
        ("technique", "password", UserRole.TECHNIQUE),
        ("chercheur", "password", UserRole.CHERCHEUR),
    ]
    for username, password, role in users_data:
        hashed_password = sha256(password.encode()).hexdigest()
        user = User(username=username, password=hashed_password, role=role)
        db.session.add(user)

    hab_elec = Habilitation(nomHab="Electrique")
    hab_bio = Habilitation(nomHab="Biologique")
    db.session.add_all([hab_elec, hab_bio])

    pers1 = Personnel(nom="Dupont")
    pers1.habilitations.append(hab_elec)
    pers2 = Personnel(nom="Martin")
    pers2.habilitations.append(hab_bio)
    db.session.add_all([pers1, pers2])

    plat1 = Plateforme(
        nom="Plateforme Alpha",
        nb_personnes_necessaires=2,
        cout_journalier=1000,
        intervalle_maintenance=30
    )
    plat1.habilitations_requises.append(hab_elec)
    db.session.add(plat1)

    db.session.commit()


def login_as(client, username):
    client.post('/login', data={'username': username, 'password': 'password'}, follow_redirects=True)


@pytest.fixture
def admin_client(client):
    with client:
        login_as(client, 'admin')
        yield client


def pytest_configure(config):
    config.addinivalue_line("markers", "auth: tests liés à l'authentification")
    config.addinivalue_line("markers", "roles: tests liés aux permissions des rôles")