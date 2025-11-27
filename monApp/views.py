from flask import render_template, request, url_for, redirect, flash, abort
from hashlib import sha256
from .app import app, db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Personnel, Habilitation, Plateforme, Campagne, Maintenance, Echantillon, Budget
from .forms import LoginForm, RegisterForm, CampagneForm, BudgetForm
import random
from source import algoADN, arbresPhylogenetiques, calculSimilarite, constantes
from sqlalchemy import func

# -------------------------------------------
# GESTION DE SESSION UTILISATEUR ET AUTHENTIFICATION
# -------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == sha256(form.password.data.encode()).hexdigest():
            login_user(user)
            flash(f'Connexion réussie ! Bienvenue, {user.username}.', 'success')
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
    nom_utilisateur = current_user.username
    logout_user()
    flash(f'Vous avez été déconnecté, {nom_utilisateur}. À bientôt !', 'info')
    return redirect(url_for('index'))

# -------------------------------------------
# ROUTES PRINCIPALES DE NAVIGATION
# -------------------------------------------

@app.route('/')
@login_required
def index():
    return redirect(url_for('tableau_de_bord'))

@app.route('/tableau_de_bord/')
@login_required
def tableau_de_bord():
    stats = {
        'active_campaigns': Campagne.query.filter(Campagne.statut == 'En cours').count(),
        'total_budget': int(db.session.query(func.sum(Budget.montant)).scalar() or 0),
        'total_personnel': Personnel.query.count(),
        'total_samples': Echantillon.query.count()
    }
    
    # Filtrer les campagnes "En cours" en Python, car 'statut' est une propriété
    all_campaigns = Campagne.query.order_by(Campagne.date_debut.desc()).all()
    active_campaigns = [c for c in all_campaigns if c.statut == 'En cours'][:5]
    stats['active_campaigns'] = len(active_campaigns)

    # Prepare data for the budget chart
    budgets_for_chart = Budget.query.order_by(Budget.mois.asc()).all()
    
    budget_chart_data = {
        'labels': [b.mois.strftime('%B %Y') for b in budgets_for_chart],
        'allocated': [float(b.montant) for b in budgets_for_chart],
        'spent': [float(b.cout_total_campagnes) for b in budgets_for_chart]
    }

    return render_template('tableau_de_bord.html', stats=stats, active_campaigns=active_campaigns, budget_chart_data=budget_chart_data)



# -------------------------------------------
# GESTION DU PERSONNEL
# -------------------------------------------

@app.route('/personnel/', methods=['GET', 'POST'])
@login_required
def personnel():
    if request.method == 'POST':
        nom = request.form.get('nom')
        habilitation_ids = request.form.getlist('habilitation')
        
        if not nom:
            flash("Le nom est obligatoire.", "danger")
        else:
            new_personnel = Personnel(nom=nom)
            for hab_id in habilitation_ids:
                hab = Habilitation.query.get(hab_id)
                if hab:
                    new_personnel.habilitations.append(hab)
            db.session.add(new_personnel)
            db.session.commit()
            db.session.refresh(new_personnel) # Rafraîchir l'objet pour charger les relations
            flash(f"Le membre du personnel '{nom}' a été ajouté avec succès.", "success")
        return redirect(url_for('personnel'))

    personnel_list = Personnel.query.order_by(Personnel.nom).all()
    all_habilitations = Habilitation.query.all()
    return render_template('personnel.html', personnel_list=personnel_list, all_habilitations=all_habilitations)

@app.route('/delete_personnel/<int:personnel_id>', methods=['GET', 'POST'])
@login_required
def delete_personnel(personnel_id):
    personne = Personnel.query.get_or_404(personnel_id)
    if request.method == 'POST':
        nom_supprime = personne.nom
        db.session.delete(personne)
        db.session.commit()
        flash(f"Le membre du personnel '{nom_supprime}' a été supprimé.", "success")
        return redirect(url_for('personnel'))
    return render_template('delete_personnel.html', personnel=personne)

@app.route('/edit_personnel/<int:personnel_id>', methods=['GET', 'POST'])
@login_required
def edit_personnel(personnel_id):
    personne = Personnel.query.get_or_404(personnel_id)
    all_habilitations = Habilitation.query.all()
    if request.method == 'POST':
        personne.nom = request.form.get('nom')
        habilitation_ids = request.form.getlist('habilitation')
        personne.habilitations = [Habilitation.query.get(hab_id) for hab_id in habilitation_ids]
        db.session.commit()
        flash(f"Les informations de '{personne.nom}' ont été mises à jour.", "success")
        return redirect(url_for('personnel'))
    
    personnel_hab_ids = {hab.idHab for hab in personne.habilitations}
    return render_template('edit_personnel.html', personnel=personne, all_habilitations=all_habilitations, personnel_hab_ids=personnel_hab_ids)

# -------------------------------------------
# GESTION DE LA PLATEFORME (ÉQUIPEMENTS)
# -------------------------------------------

@app.route('/plateforme/')
@login_required
def plateforme():
    equipements = Plateforme.query.order_by(Plateforme.nom).all()
    return render_template('plateforme.html', equipements=equipements)

@app.route('/plateforme/add', methods=['GET', 'POST'])
@login_required
def add_plateforme():
    if request.method == 'POST':
        nom = request.form.get('nom')
        if nom:
            new_equipement = Plateforme(nom=nom, cout_journalier=0, nb_personnes_necessaires=0, intervalle_maintenance=30)
            db.session.add(new_equipement)
            db.session.commit()
            flash(f"L'équipement '{nom}' a été ajouté.", 'success')
            return redirect(url_for('plateforme'))
        else:
            flash("Le nom de l'équipement est obligatoire.", 'danger')
    return render_template('add_plateforme.html')

@app.route('/delete_plateforme/<int:equipement_id>', methods=['GET', 'POST'])
@login_required
def delete_plateforme(equipement_id):
    equipement = Plateforme.query.get_or_404(equipement_id)
    if request.method == 'POST':
        nom_supprime = equipement.nom
        db.session.delete(equipement)
        db.session.commit()
        flash(f"L'équipement '{nom_supprime}' a été supprimé.", "success")
        return redirect(url_for('plateforme'))
    return render_template('delete_plateforme.html', equipement=equipement)

# -------------------------------------------
# GESTION DES CAMPAGNES
# -------------------------------------------

@app.route('/campagnes/')
@login_required
def campagnes():
    query = Campagne.query
    search_term = request.args.get('search')
    status_filter = request.args.get('status')

    if search_term:
        query = query.filter(Campagne.nom.ilike(f'%{search_term}%'))

    if status_filter:
        # This requires the status property to work with the query, which it doesn't directly.
        # A more complex solution would be needed for DB-level filtering.
        # For now, we filter in Python after fetching.
        all_campagnes = query.order_by(Campagne.date_debut.desc()).all()
        campagnes_list = [c for c in all_campagnes if c.statut.lower().replace(' ', '_') == status_filter]
    else:
        campagnes_list = query.order_by(Campagne.date_debut.desc()).all()

    return render_template('campagnes.html', campagnes=campagnes_list)

@app.route('/campagnes/add', methods=['GET', 'POST'])
@login_required
def add_campagne():
    form = CampagneForm()
    form.plateforme.choices = [(p.idPl, p.nom) for p in Plateforme.query.order_by(Plateforme.nom).all()]
    form.personnel_implique.choices = [(pers.idPers, pers.nom) for pers in Personnel.query.order_by(Personnel.nom).all()]

    if form.validate_on_submit():
        plateforme_selectionnee = Plateforme.query.get(form.plateforme.data)
        personnel_selectionne = [Personnel.query.get(id) for id in form.personnel_implique.data]

        new_campagne = Campagne(
            nom=form.nom.data,
            date_debut=form.date_debut.data,
            duree=form.duree.data,
            lieu=form.lieu.data,
            plateforme=plateforme_selectionnee
        )

        for pers in personnel_selectionne:
            new_campagne.personnel_implique.append(pers)

        db.session.add(new_campagne)
        db.session.commit()
        flash(f"La campagne '{form.nom.data}' a été planifiée.", 'success')
        return redirect(url_for('campagnes'))
    
    return render_template('add_campagne.html', form=form)

@app.route('/campagnes/edit/<int:campagne_id>', methods=['GET', 'POST'])
@login_required
def edit_campagne(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    form = CampagneForm(obj=campagne)
    
    form.plateforme.choices = [(p.idPl, p.nom) for p in Plateforme.query.order_by(Plateforme.nom).all()]
    form.personnel_implique.choices = [(p.idPers, p.nom) for p in Personnel.query.order_by(Personnel.nom).all()]

    if request.method == 'GET':
        form.personnel_implique.data = [p.idPers for p in campagne.personnel_implique] # Déjà correct, mais je vérifie
        form.plateforme.data = campagne.idPl


    if form.validate_on_submit():
        campagne.nom = form.nom.data
        campagne.date_debut = form.date_debut.data
        campagne.duree = form.duree.data
        campagne.lieu = form.lieu.data
        campagne.plateforme = Plateforme.query.get(form.plateforme.data)
        
        personnel_selectionne = [Personnel.query.get(id) for id in form.personnel_implique.data]
        campagne.personnel_implique = personnel_selectionne
        
        db.session.commit()
        flash(f"La campagne '{campagne.nom}' a été mise à jour.", 'success')
        return redirect(url_for('campagnes'))

    # Pre-fill form data for GET request
    form.nom.data = campagne.nom
    form.date_debut.data = campagne.date_debut
    form.duree.data = campagne.duree
    form.lieu.data = campagne.lieu

    return render_template('edit_campagne.html', form=form, campagne=campagne)

@app.route('/campagnes/delete/<int:campagne_id>', methods=['GET', 'POST'])
@login_required
def delete_campagne(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    if request.method == 'POST':
        db.session.delete(campagne)
        db.session.commit()
        flash(f"La campagne '{campagne.nom}' a été supprimée.", 'success')
        return redirect(url_for('campagnes'))
    return render_template('delete_campagne.html', campagne=campagne)
# -------------------------------------------
# GESTION DES SÉQUENCES ADN
# -------------------------------------------

@app.route('/sequences_adn/', methods=['GET', 'POST'])
@login_required
def sequences_adn():
    if request.method == 'POST':
        flash('Ajout de séquence non implémenté.', 'info')
        return redirect(url_for('sequences_adn'))
    # ...
    return render_template('sequences_adn.html', sequences=[])

# -------------------------------------------
# ROUTES POUR L'ANALYSE (BUDGET ET ADN)
# -------------------------------------------

@app.route('/budget/', methods=['GET', 'POST'])
@login_required
def budget():
    form = BudgetForm()
    if form.validate_on_submit():
        new_budget = Budget(
            mois=form.mois.data,
            montant=form.montant.data
        )
        db.session.add(new_budget)
        db.session.commit()
        flash(f"Le budget de {form.montant.data}€ pour {form.mois.data.strftime('%B %Y')} a été ajouté.", "success")
        return redirect(url_for('budget'))

    budgets = Budget.query.order_by(Budget.mois.desc()).all()
    return render_template('budget.html', budgets=budgets, form=form)

@app.route('/analyse/', methods=['GET', 'POST'])
@login_required
def analyse():
    results = request.args.to_dict()
    return render_template('analyse.html', **results)

@app.route('/analyse/generate', methods=['POST'])
def analyse_generate():
    try:
        length = int(request.form.get('length', 0))
        if length <= 0:
            flash("La longueur doit être un nombre positif.", "danger")
            return redirect(url_for('analyse'))
        bases = ['A', 'C', 'G', 'T']
        sequence = ''.join(random.choice(bases) for _ in range(length))
        return redirect(url_for('analyse', generated_sequence=sequence))
    except (ValueError, TypeError):
        flash("Veuillez entrer une longueur valide.", "danger")
        return redirect(url_for('analyse'))

@app.route('/analyse/mutate', methods=['POST'])
def analyse_mutate():
    sequence = request.form.get('sequence_to_mutate', '').upper()
    mutation_rate = request.form.get('mutation_rate', '0.1')
    if not sequence:
        flash("Une séquence est requise pour la mutation.", "danger")
        return redirect(url_for('analyse'))
    try:
        mutated_sequence = algoADN.muter_complet(sequence, float(mutation_rate))
        return redirect(url_for('analyse', mutated_sequence=mutated_sequence, original_for_mutation=sequence))
    except (ValueError, TypeError):
        flash("Veuillez entrer un taux de mutation valide (ex: 0.1).", "danger")
        return redirect(url_for('analyse'))

@app.route('/analyse/levenshtein', methods=['POST'])
def analyse_levenshtein():
    seq1 = request.form.get('seq1', '').upper()
    seq2 = request.form.get('seq2', '').upper()
    if not seq1 or not seq2:
        flash("Les deux séquences sont requises pour calculer la distance.", "danger")
        return redirect(url_for('analyse'))
    
    distance = calculSimilarite.distance_levenshtein(seq1, seq2)
    return redirect(url_for('analyse', distance=distance, seq1_lev=seq1, seq2_lev=seq2))

@app.route('/analyse/align', methods=['POST'])
def analyse_align():
    seq1 = request.form.get('seq1_align', '').upper()
    seq2 = request.form.get('seq2_align', '').upper()
    if not seq1 or not seq2:
        flash("Les deux séquences sont requises pour l'alignement.", "danger")
        return redirect(url_for('analyse'))
    
    aligned_seq1, aligned_seq2 = algoADN.aligner_sequences(seq1, seq2)
    return redirect(url_for('analyse', aligned_seq1=aligned_seq1, aligned_seq2=aligned_seq2))

@app.route('/analyse/tree', methods=['POST'])
def analyse_tree():
    sequences_text = request.form.get('sequences_tree', '')
    if not sequences_text:
        flash("Au moins deux séquences sont requises pour construire l'arbre.", "danger")
        return redirect(url_for('analyse'))
    
    sequences = [s.strip().upper() for s in sequences_text.splitlines() if s.strip()]
    if len(sequences) < 2:
        flash("Veuillez fournir au moins deux séquences valides.", "danger")
        return redirect(url_for('analyse'))
        
    newick_tree = arbresPhylogenetiques.construire_arbre(sequences)
    return redirect(url_for('analyse', newick_tree=newick_tree, original_sequences_tree=sequences_text))