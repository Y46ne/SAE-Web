from flask import render_template, request, url_for, redirect, flash
from hashlib import sha256
from .app import app, db, login_manager
from flask_login import login_user, logout_user, login_required
from config import *

# ------------------- MAIN -------------------
from .models import User
from .forms import LoginForm, RegisterForm

@login_manager.user_loader
def load_user(user_id):
    """Charge un utilisateur à partir de son ID."""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return redirect(url_for('tableau_de_bord'))

@app.route('/tableau_de_bord/')
def tableau_de_bord():
    return render_template('tableau_de_bord.html')

@app.route('/personnel/')
def personnel():
    return render_template('personnel.html')

@app.route('/plateforme/')
def plateforme():
    equipements_fictifs = [
        {'id': 1, 'nom': 'Séquenceur ADN #1', 'statut': 'Opérationnel', 'statut_class': 'success'},
        {'id': 2, 'nom': 'Centrifugeuse Z-2000', 'statut': 'En maintenance', 'statut_class': 'warning'},
        {'id': 3, 'nom': 'Microscope Électronique', 'statut': 'Hors service', 'statut_class': 'danger'},
        {'id': 4, 'nom': 'PCR Thermocycleur', 'statut': 'Opérationnel', 'statut_class': 'success'},
    ]
    return render_template('plateforme.html', equipements=equipements_fictifs)

@app.route('/budget/')
def budget():
    return render_template('budget.html')

@app.route('/analyse/')
def analyse():
    return render_template('analyse.html')

@app.route('/delete_personnel/')
def delete_personnel():
    return render_template('delete_personnel.html')

@app.route('/edit_personnel/')
def edit_personnel():
    return render_template('edit_personnel.html')

@app.route('/edit_plateforme/<int:equipement_id>', methods=['GET', 'POST'])
def edit_plateforme(equipement_id):
    # À remplacer par une requête à la base de données
    equipement_fictif = {'id': equipement_id, 'nom': 'Séquenceur ADN #'+str(equipement_id), 'statut': 'Opérationnel'}
    if request.method == 'POST':
        flash(f"L'équipement {equipement_fictif['nom']} a été mis à jour (simulation).", 'success')
        return redirect(url_for('plateforme'))
    return render_template('edit_plateforme.html', equipement=equipement_fictif)

@app.route('/delete_plateforme/<int:equipement_id>', methods=['GET', 'POST'])
def delete_plateforme(equipement_id):
    equipement_fictif = {'id': equipement_id, 'nom': 'Séquenceur ADN #'+str(equipement_id)}
    return render_template('delete_plateforme.html', equipement=equipement_fictif)

@app.route('/maintenance/')
def maintenance():
    maintenance_adn = [
        {'id': 1, 'plateforme': 'Séquenceur ADN', 'date_prevue': '2024-06-15', 'statut': 'Prévue', 'statut_class': 'primary'},
        {'id': 2, 'plateforme': 'Station de nettoyage', 'date_prevue': '2024-05-20', 'statut': 'Terminée', 'statut_class': 'success'},
    ]
    return render_template('maintenance.html', maintenances=maintenance_adn)

@app.route('/campagnes/')
def campagnes():
    campagnes_adn = [
        {'id': 1, 'nom': 'Fouille du Trias', 'date_debut': '2024-06-01', 'duree': 30, 'lieu': 'Forêt de Sologne', 'statut': 'En cours', 'statut_class': 'warning'},
        {'id': 2, 'nom': 'Exploration du Crétacé', 'date_debut': '2024-07-15', 'duree': 45, 'lieu': 'Sud de la France', 'statut': 'Prévue', 'statut_class': 'primary'},
        {'id': 3, 'nom': 'Recherche du Jurassique', 'date_debut': '2024-04-10', 'duree': 20, 'lieu': 'Normandie', 'statut': 'Terminée', 'statut_class': 'success'},
    ]
    return render_template('campagnes.html', campagnes=campagnes_adn)

@app.route('/sequences_adn/', methods=['GET', 'POST'])
def sequences_adn():
    if request.method == 'POST':
        flash('Ajout de séquence non implémenté.', 'info')
        return redirect(url_for('sequences_adn'))

    sequences_adn = [
        {'id': 1, 'campagne': 'Campagne 1', 'fichier': 'seq1.fasta', 'commentaire': 'Fragment de T-Rex'},
        {'id': 2, 'campagne': 'Campagne 2', 'fichier': 'seq2.fasta', 'commentaire': 'Fragment de Velociraptor'},
        {'id': 3, 'campagne': 'Campagne 1', 'fichier': 'seq3.fasta', 'commentaire': 'Fragment de Triceratops'},
    ]
    return render_template('sequences_adn.html', sequences=sequences_adn)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == sha256(form.password.data.encode()).hexdigest():
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html', form=form)

@app.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = sha256(form.password.data.encode()).hexdigest()
        new_user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('creer_compte.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)