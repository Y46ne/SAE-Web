# SAE-Web

**Contributeurs :** Yassine Belaarous, Ilane Riotte, Corentin Lacoume et Clément Vignon Chaudey

## Présentation
Cette application web a été développée dans le cadre de la SAE 3.01. Elle est destinée à la gestion d'un laboratoire de paléontologie de l'Université d'Orléans. Elle permet de centraliser la gestion des campagnes de fouilles, du matériel technique, du personnel habilité, ainsi que l'analyse algorithmique des échantillons ADN collectés.

## Identifiants de test pour l'application

| Rôle | Identifiant (Username) | Mot de passe |
| :--- | :--- | :--- | :--- |
| **Administrateur** | `admin` | `password`
| **Direction** | `direction` | `password`
| **Technique** | `technique` | `password`
| **Chercheur** | `chercheur` | `password`

### Installation et Lancement
Suivez ces étapes pour exécuter l'application sur votre machine :

1.  **Cloner le dépôt**
    ```bash
    git clone <URL_DU_REPO>
    cd SAE-Web
    ```

2.  **Préparer l'environnement**
    * Créez un environnement virtuel :
        * Windows : `python -m venv venv`
        * macOS/Linux : `python3 -m venv venv`
    * Activez l'environnement :
        * Windows : `venv\Scripts\activate`
        * macOS/Linux : `source venv/bin/activate`
    * Installez les dépendances :
        ```bash
        pip install -r requirements.txt
        ```

3.  **Initialiser la base de données**
    L'application utilise une commande personnalisée pour créer les tables et charger les données de test :
    ```bash
    flask loaddb monApp/data/data.yml
    ```

4.  **Lancer l'application**
    ```bash
    flask run
    ```
    L'application sera accessible à l'adresse : `http://127.0.0.1:5000`

### Lancer les tests
Le projet contient des tests unitaires et de performance pour les algorithmes d'analyse ADN (Levenshtein, Arbres Phylogénétiques).

* **Tests de similarité :**
    ```bash
    pytest source/test_calcul_similarite.py
    ```
* **Tests de performance :**
    ```bash
    python source/test_performance.py
    ```
