import pytest
from flask import url_for
from monApp.models import Personnel


@pytest.mark.auth
class TestAuth:

    def test_login_logout(self, client, auth):
        response = client.get("/login")
        response_text = response.data.decode('utf-8')
        assert response.status_code == 200
        assert "Nom d'utilisateur" in response_text

        response = auth.login(username="admin", password="password")
        response_text = response.data.decode('utf-8')
        assert response.status_code == 200
        assert "Connexion réussie !" in response_text
        assert "Tableau de Bord" in response_text

        response = auth.logout()
        response_text = response.data.decode('utf-8')
        assert response.status_code == 200
        assert "Vous avez été déconnecté" in response_text

    def test_login_invalid_credentials(self, auth):
        response = auth.login(username="admin", password="wrongpassword")
        response_text = response.data.decode('utf-8')
        assert "Nom d'utilisateur ou mot de passe incorrect." in response_text

    def test_access_protected_route_unauthenticated(self, client):
        response = client.get("/tableau_de_bord/", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.location


@pytest.mark.roles
class TestRoles:

    @pytest.mark.parametrize("username, expected_status", [
        ("admin", 200),
        ("direction", 403),
        ("technique", 403),
        ("chercheur", 403),
    ])
    def test_personnel_page_access(self, client, auth, username, expected_status):
        auth.login(username=username, password="password")
        response = client.get("/personnel/")
        assert response.status_code == expected_status
        auth.logout()

    @pytest.mark.parametrize("username, expected_status", [
        ("admin", 200),
        ("direction", 200),
        ("technique", 403),
        ("chercheur", 403),
    ])
    def test_budget_page_access(self, client, auth, username, expected_status):
        auth.login(username=username, password="password")
        response = client.get("/budget/")
        assert response.status_code == expected_status
        auth.logout()


class TestPersonnel:

    def test_add_personnel(self, admin_client, db):
        response = admin_client.post('/personnel/', data={
            'nom': 'Nouveau Membre',
            'habilitation': []
        }, follow_redirects=True)
        response_text = response.data.decode('utf-8')

        assert response.status_code == 200
        assert "a été ajouté avec succès" in response_text
        
        new_personnel = db.session.query(Personnel).filter_by(nom='Nouveau Membre').first()
        assert new_personnel is not None

    def test_delete_personnel(self, admin_client, db):
        personnel_to_delete = db.session.query(Personnel).filter_by(nom='Dupont').first()
        assert personnel_to_delete is not None
        response = admin_client.post(f'/delete_personnel/{personnel_to_delete.idPers}', follow_redirects=True)
        response_text = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'a été supprimé' in response_text
        assert db.session.query(Personnel).filter_by(nom='Dupont').first() is None