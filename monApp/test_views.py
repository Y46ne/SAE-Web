from flask import url_for


def test_login_page(client):
    """
    GIVEN un client Flask configuré pour les tests
    WHEN la page de connexion ('/login') est demandée (GET)
    THEN vérifier que la réponse est valide (code 200)
    """
    response = client.get(url_for('login'))
    response_text = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Nom d'utilisateur" in response_text
    assert "Mot de passe" in response_text


def test_dashboard_unauthenticated(client):
    """
    GIVEN un client Flask
    WHEN la page du tableau de bord ('/tableau_de_bord/') est demandée sans authentification
    THEN vérifier que l'utilisateur est redirigé vers la page de connexion
    """
    response = client.get(url_for('tableau_de_bord'), follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert response.status_code == 200
    # Le message flash par défaut de Flask-Login
    assert "Veuillez vous connecter pour accéder à cette page." in response_text


def test_login_and_access_dashboard(client):
    """Teste la connexion et l'accès à une page protégée."""
    # Utilise l'utilisateur 'admin' créé dans le conftest.py principal
    client.post(url_for('login'), data={'username': 'admin', 'password': 'password'})
    response = client.get(url_for('tableau_de_bord'))
    response_text = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Tableau de Bord" in response_text