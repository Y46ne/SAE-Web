from flask import render_template, request, url_for, redirect, flash, abort, jsonify
from hashlib import sha256
from .app import app, db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Personnel, Habilitation, Plateforme, Campagne, Echantillon, Budget, UserRole, Maintenance, MaintenanceStatus
from .forms import LoginForm, RegisterForm, CampagneForm, BudgetForm, PlateformeForm, EchantillonForm, MaintenanceForm
import random
from source import algoADN, arbresPhylogenetiques, calculSimilarite
from sqlalchemy import func, extract
from functools import wraps
import os
from werkzeug.utils import secure_filename

# -------------------------------------------
# GESTION DE SESSION UTILISATEUR ET AUTHENTIFICATION
# -------------------------------------------


def role_required(*roles):
    """Décorateur pour restreindre l'accès à certains rôles."""

    def wrapper(fn):

        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == sha256(
                form.password.data.encode()).hexdigest():
            login_user(user)
            flash(f'Connexion réussie ! Bienvenue, {user.username}.',
                  'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html', form=form)


@app.route('/creer_compte', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.DIRECTION)
def creer_compte():
    form = RegisterForm()

    if current_user.role == UserRole.ADMIN:
        form.role.choices = [(UserRole.DIRECTION.value, 'Direction'),
                             (UserRole.TECHNIQUE.value, 'Technicien'),
                             (UserRole.CHERCHEUR.value, 'Chercheur')]
    elif current_user.role == UserRole.DIRECTION:
        form.role.choices = [(UserRole.TECHNIQUE.value, 'Technicien'),
                             (UserRole.CHERCHEUR.value, 'Chercheur')]
    else:
        form.role.choices = []

    if form.validate_on_submit():
        hashed_password = sha256(form.password.data.encode()).hexdigest()

        selected_role_value = form.role.data
        selected_role = UserRole(selected_role_value)

        new_user = User(username=form.username.data,
                        password=hashed_password,
                        role=selected_role)
        db.session.add(new_user)
        db.session.commit()
        flash('Le compte a été créé avec succès !', 'success')
        return redirect(url_for('index'))

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
        'active_campaigns':
        Campagne.query.filter(Campagne.statut == 'En cours').count(),
        'total_budget':
        int(db.session.query(func.sum(Budget.montant)).scalar() or 0),
        'total_personnel':
        Personnel.query.count(),
        'total_samples':
        Echantillon.query.count()
    }

    all_campaigns = Campagne.query.order_by(Campagne.date_debut.desc()).all()
    active_campaigns = [c for c in all_campaigns if c.statut == 'En cours'][:5]
    stats['active_campaigns'] = len(active_campaigns)

    budgets_for_chart = Budget.query.order_by(Budget.mois.asc()).all()

    budget_chart_data = {
        'labels': [b.mois.strftime('%B %Y') for b in budgets_for_chart],
        'allocated': [float(b.montant) for b in budgets_for_chart],
        'spent': [float(b.cout_total_campagnes) for b in budgets_for_chart]
    }

    return render_template('tableau_de_bord.html',
                           stats=stats,
                           active_campaigns=active_campaigns,
                           budget_chart_data=budget_chart_data)


# -------------------------------------------
# GESTION DU PERSONNEL
# -------------------------------------------


@app.route('/personnel/', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
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
            db.session.refresh(new_personnel)
            flash(f"Le membre du personnel '{nom}' a été ajouté avec succès.",
                  "success")
        return redirect(url_for('personnel'))

    personnel_list = Personnel.query.order_by(Personnel.nom).all()
    all_habilitations = Habilitation.query.all()
    return render_template('personnel.html',
                           personnel_list=personnel_list,
                           all_habilitations=all_habilitations)


@app.route('/delete_personnel/<int:personnel_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def delete_personnel(personnel_id):
    personne = Personnel.query.get_or_404(personnel_id)
    if request.method == 'POST':
        nom_supprime = personne.nom
        db.session.delete(personne)
        db.session.commit()
        flash(f"Le membre du personnel '{nom_supprime}' a été supprimé.",
              "success")
        return redirect(url_for('personnel'))
    return render_template('delete_personnel.html', personnel=personne)


@app.route('/edit_personnel/<int:personnel_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN)
def edit_personnel(personnel_id):
    personne = Personnel.query.get_or_404(personnel_id)
    all_habilitations = Habilitation.query.all()
    if request.method == 'POST':
        personne.nom = request.form.get('nom')
        habilitation_ids = request.form.getlist('habilitation')
        personne.habilitations = [
            Habilitation.query.get(hab_id) for hab_id in habilitation_ids
        ]
        db.session.commit()
        flash(f"Les informations de '{personne.nom}' ont été mises à jour.",
              "success")
        return redirect(url_for('personnel'))

    personnel_hab_ids = {hab.idHab for hab in personne.habilitations}
    return render_template('edit_personnel.html',
                           personnel=personne,
                           all_habilitations=all_habilitations,
                           personnel_hab_ids=personnel_hab_ids)


# -------------------------------------------
# GESTION DE LA PLATEFORME (ÉQUIPEMENTS)
# -------------------------------------------


@app.route('/plateforme/')
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def plateforme():
    equipements = Plateforme.query.order_by(Plateforme.nom).all()
    return render_template('plateforme.html', equipements=equipements)


@app.route('/plateforme/add', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def add_plateforme():
    form = PlateformeForm()
    form.habilitations_requises.choices = [
        (h.idHab, h.nomHab)
        for h in Habilitation.query.order_by('nomHab').all()
    ]

    if form.validate_on_submit():
        nouvelle_plateforme = Plateforme(
            nom=form.nom.data,
            nb_personnes_necessaires=form.nb_personnes_necessaires.data,
            cout_journalier=form.cout_journalier.data,
            intervalle_maintenance=form.intervalle_maintenance.data)

        for hab_id in form.habilitations_requises.data:
            habilitation = Habilitation.query.get(hab_id)
            if habilitation:
                nouvelle_plateforme.habilitations_requises.append(habilitation)

        db.session.add(nouvelle_plateforme)
        db.session.commit()
        flash("La plateforme a été ajoutée avec succès.", "success")
        return redirect(url_for('plateforme'))

    return render_template('add_plateforme.html', form=form)


@app.route('/plateforme/edit/<int:equipement_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def edit_plateforme(equipement_id):
    equipement = Plateforme.query.get_or_404(equipement_id)
    form = PlateformeForm(obj=equipement)
    form.habilitations_requises.choices = [
        (h.idHab, h.nomHab)
        for h in Habilitation.query.order_by('nomHab').all()
    ]

    if request.method == 'POST' and form.validate_on_submit():
        equipement.nom = form.nom.data
        equipement.nb_personnes_necessaires = form.nb_personnes_necessaires.data
        equipement.cout_journalier = form.cout_journalier.data
        equipement.intervalle_maintenance = form.intervalle_maintenance.data

        # Supprimer les habilitations existantes et ajouter les nouvelles
        equipement.habilitations_requises.clear()
        for hab_id in form.habilitations_requises.data:
            habilitation = Habilitation.query.get(hab_id)
            if habilitation:
                equipement.habilitations_requises.append(habilitation)

        db.session.commit()
        flash(f"L'équipement '{equipement.nom}' a été mis à jour.", "success")
        return redirect(url_for('plateforme'))

    if request.method == 'GET':
        form.habilitations_requises.data = [
            h.idHab for h in equipement.habilitations_requises
        ]

    return render_template('edit_plateforme.html',
                           form=form,
                           equipement=equipement)


@app.route('/delete_plateforme/<int:equipement_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
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
# GESTION DE LA MAINTENANCE
# -------------------------------------------


@app.route('/maintenance/')
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def maintenance():
    maintenances = Maintenance.query.order_by(
        Maintenance.date_maintenance.desc()).all()
    return render_template('maintenance.html', maintenances=maintenances)


@app.route('/maintenance/add', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def add_maintenance():
    form = MaintenanceForm()
    form.plateforme.choices = [
        (p.idPl, p.nom)
        for p in Plateforme.query.order_by(Plateforme.nom).all()
    ]

    if form.validate_on_submit():
        new_maintenance = Maintenance(
            date_maintenance=form.date_maintenance.data,
            duree=form.duree.data,
            type_operation=form.type_operation.data,
            idPl=form.plateforme.data)
        db.session.add(new_maintenance)
        db.session.commit()
        flash("La maintenance a été programmée avec succès.", "success")
        return redirect(url_for('maintenance'))

    return render_template('add_maintenance.html', form=form)


@app.route('/maintenance/validate/<int:maintenance_id>', methods=['POST'])
@login_required
@role_required(UserRole.ADMIN, UserRole.TECHNIQUE)
def validate_maintenance(maintenance_id):
    maintenance = Maintenance.query.get_or_404(maintenance_id)
    maintenance.statut = MaintenanceStatus.TERMINEE
    db.session.commit()
    flash(
        f"La maintenance pour '{maintenance.plateforme.nom}' a été marquée comme terminée.",
        "success")
    return redirect(url_for('maintenance'))


# -------------------------------------------
# GESTION DES CAMPAGNES
# -------------------------------------------


@app.route('/campagnes/')
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def campagnes():
    query = Campagne.query
    search_term = request.args.get('search')
    status_filter = request.args.get('status')

    if search_term:
        query = query.filter(Campagne.nom.ilike(f'%{search_term}%'))

    if status_filter:
        all_campagnes = query.order_by(Campagne.date_debut.desc()).all()
        campagnes_list = [
            c for c in all_campagnes
            if c.statut.lower().replace(' ', '_') == status_filter
        ]
    else:
        campagnes_list = query.order_by(Campagne.date_debut.desc()).all()

    return render_template('campagnes.html', campagnes=campagnes_list)


@app.route('/campagnes/add', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def add_campagne():
    form = CampagneForm()
    form.plateforme.choices = [(0, "Sélectionnez une plateforme...")] + [
        (p.idPl, p.nom)
        for p in Plateforme.query.order_by(Plateforme.nom).all()
    ]

    form.personnel_implique.choices = [
        (pers.idPers, pers.nom)
        for pers in Personnel.query.order_by(Personnel.nom).all()
    ]

    if form.validate_on_submit():
        if not form.plateforme.data:
            flash("Veuillez sélectionner une plateforme.", "danger")
            return render_template('add_campagne.html', form=form)

        plateforme_selectionnee = Plateforme.query.get(form.plateforme.data)

        # Logique de vérification du budget
        campaign_date = form.date_debut.data
        campaign_month = campaign_date.month
        campaign_year = campaign_date.year

        budget = Budget.query.filter(
            extract('month', Budget.mois) == campaign_month,
            extract('year', Budget.mois) == campaign_year).first()

        if not budget:
            flash(
                f"Aucun budget n'est défini pour {campaign_date.strftime('%B %Y')}. Impossible de planifier la campagne.",
                "danger")
            return render_template('add_campagne.html', form=form)

        new_campaign_cost = plateforme_selectionnee.cout_journalier * form.duree.data

        campaigns_in_month = Campagne.query.filter(
            extract('month', Campagne.date_debut) == campaign_month,
            extract('year', Campagne.date_debut) == campaign_year).all()

        spent_in_month = sum(c.plateforme.cout_journalier * c.duree
                             for c in campaigns_in_month if c.plateforme)

        if spent_in_month + new_campaign_cost > budget.montant:
            remaining_budget = budget.montant - spent_in_month
            flash(
                f"Le coût de la campagne ({new_campaign_cost}€) dépasse le budget restant ({remaining_budget}€) pour {campaign_date.strftime('%B %Y')}.",
                "danger")
            return render_template('add_campagne.html', form=form)

        # Fin de la logique de vérification du budget

        # Vérifier la disponibilité de la plateforme et du personnel
        from datetime import timedelta
        date_debut_nouvelle = form.date_debut.data
        date_fin_nouvelle = date_debut_nouvelle + timedelta(
            days=form.duree.data)

        # 1. Vérifier le conflit de plateforme
        campagnes_existantes_plateforme = Campagne.query.filter_by(
            idPl=plateforme_selectionnee.idPl).all()
        for campagne_existante in campagnes_existantes_plateforme:
            date_debut_existante = campagne_existante.date_debut
            date_fin_existante = date_debut_existante + timedelta(
                days=campagne_existante.duree)
            if max(date_debut_nouvelle,
                   date_debut_existante) < min(date_fin_nouvelle,
                                               date_fin_existante):
                flash(
                    f"La plateforme '{plateforme_selectionnee.nom}' est déjà réservée pour la période du {date_debut_existante.strftime('%d/%m/%Y')} au {date_fin_existante.strftime('%d/%m/%Y')}.",
                    "danger")
                return render_template('add_campagne.html', form=form)

        # 2. Vérifier le conflit de personnel
        personnel_selectionne_ids = form.personnel_implique.data
        for pers_id in personnel_selectionne_ids:
            personnel = Personnel.query.get(pers_id)
            for campagne_existante in personnel.campagnes:
                date_debut_existante = campagne_existante.date_debut
                date_fin_existante = date_debut_existante + timedelta(
                    days=campagne_existante.duree)
                if max(date_debut_nouvelle,
                       date_debut_existante) < min(date_fin_nouvelle,
                                                   date_fin_existante):
                    flash(
                        f"Le membre du personnel '{personnel.nom}' est déjà occupé sur une autre campagne durant cette période (du {date_debut_existante.strftime('%d/%m/%Y')} au {date_fin_existante.strftime('%d/%m/%Y')}).",
                        "danger")
                    return render_template('add_campagne.html', form=form)

        # 3. Vérifier l'intervalle de maintenance
        derniere_maintenance = Maintenance.query.filter_by(
            idPl=plateforme_selectionnee.idPl,
            statut=MaintenanceStatus.TERMINEE).order_by(
                Maintenance.date_maintenance.desc()).first()

        if derniere_maintenance:
            intervalle = timedelta(
                days=plateforme_selectionnee.intervalle_maintenance)
            date_expiration_maintenance = derniere_maintenance.date_maintenance + intervalle

            if date_fin_nouvelle > date_expiration_maintenance:
                # Vérifier si une maintenance future est déjà planifiée avant le début de la nouvelle campagne
                maintenance_future_prevue = Maintenance.query.filter(
                    Maintenance.idPl == plateforme_selectionnee.idPl,
                    Maintenance.statut == MaintenanceStatus.PREVUE,
                    Maintenance.date_maintenance
                    < date_debut_nouvelle).first()

                if not maintenance_future_prevue:
                    flash(
                        f"L'intervalle de maintenance pour la plateforme '{plateforme_selectionnee.nom}' sera dépassé. "
                        f"Une maintenance doit être planifiée avant le {date_debut_nouvelle.strftime('%d/%m/%Y')} pour continuer.",
                        "danger")
                    return render_template('add_campagne.html', form=form)
        else:
            # Si aucune maintenance n'a jamais été effectuée, nous ne pouvons pas évaluer l'intervalle.
            flash(
                f"Aucune maintenance terminée n'est enregistrée pour la plateforme '{plateforme_selectionnee.nom}'. "
                f"Impossible de vérifier l'intervalle de maintenance.",
                "danger")
            return render_template('add_campagne.html', form=form)

        personnel_selectionne = [
            Personnel.query.get(id) for id in form.personnel_implique.data
        ]

        new_campagne = Campagne(nom=form.nom.data,
                                date_debut=form.date_debut.data,
                                duree=form.duree.data,
                                lieu=form.lieu.data,
                                plateforme=plateforme_selectionnee)

        for pers in personnel_selectionne:
            new_campagne.personnel_implique.append(pers)

        db.session.add(new_campagne)
        db.session.commit()
        flash(f"La campagne '{form.nom.data}' a été planifiée.", 'success')
        return redirect(url_for('campagnes'))

    return render_template('add_campagne.html', form=form)


@app.route('/api/personnel_for_plateforme/<int:plateforme_id>')
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def personnel_for_plateforme(plateforme_id):
    """
    Point de terminaison de l'API pour obtenir le personnel qualifié pour une plateforme donnée.
    """
    plateforme = Plateforme.query.get_or_404(plateforme_id)
    habilitations_requises_ids = {
        hab.idHab
        for hab in plateforme.habilitations_requises
    }

    if not habilitations_requises_ids:
        personnel_qualifie = Personnel.query.order_by(Personnel.nom).all()
    else:
        personnel_qualifie = []
        for p in Personnel.query.all():
            personnel_habilitations_ids = set()
            for hab in p.habilitations:
                personnel_habilitations_ids.add(hab.idHab)

            if habilitations_requises_ids.issubset(
                    personnel_habilitations_ids):
                personnel_qualifie.append(p)

    return jsonify([{
        'id': p.idPers,
        'nom': p.nom
    } for p in personnel_qualifie])


@app.route('/campagnes/edit/<int:campagne_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def edit_campagne(campagne_id):
    campagne = Campagne.query.get_or_404(campagne_id)
    form = CampagneForm(obj=campagne)

    form.plateforme.choices = [
        (p.idPl, p.nom)
        for p in Plateforme.query.order_by(Plateforme.nom).all()
    ]
    form.personnel_implique.choices = [
        (p.idPers, p.nom)
        for p in Personnel.query.order_by(Personnel.nom).all()
    ]

    if request.method == 'GET':
        form.personnel_implique.data = [
            p.idPers for p in campagne.personnel_implique
        ]
        form.plateforme.data = campagne.idPl

    if form.validate_on_submit():
        campagne.nom = form.nom.data
        campagne.date_debut = form.date_debut.data
        campagne.duree = form.duree.data
        campagne.lieu = form.lieu.data
        campagne.plateforme = Plateforme.query.get(form.plateforme.data)

        personnel_selectionne = [
            Personnel.query.get(id) for id in form.personnel_implique.data
        ]
        campagne.personnel_implique = personnel_selectionne

        db.session.commit()
        flash(f"La campagne '{campagne.nom}' a été mise à jour.", 'success')
        return redirect(url_for('campagnes'))

    form.nom.data = campagne.nom
    form.date_debut.data = campagne.date_debut
    form.duree.data = campagne.duree
    form.lieu.data = campagne.lieu

    return render_template('edit_campagne.html', form=form, campagne=campagne)


@app.route('/campagnes/delete/<int:campagne_id>', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
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
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def sequences_adn():
    form = EchantillonForm()
    form.campagne.choices = [
        (c.idCamp, c.nom) for c in Campagne.query.order_by(Campagne.nom).all()
    ]

    if form.validate_on_submit():
        fichier = form.fichier_sequence.data
        if fichier:
            filename = secure_filename(fichier.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            fichier.save(os.path.join(upload_folder, filename))

            nouvel_echantillon = Echantillon(fichier_sequence=filename,
                                             commentaire=form.commentaire.data,
                                             idCamp=form.campagne.data)
            db.session.add(nouvel_echantillon)
            db.session.commit()
            flash(f"L'échantillon '{filename}' a été ajouté avec succès.",
                  'success')
        else:
            flash("Aucun fichier n'a été sélectionné.", 'danger')

        return redirect(url_for('sequences_adn'))

    query = Echantillon.query
    sequences = query.order_by(Echantillon.idEch.desc()).all()
    all_campaigns = Campagne.query.order_by(Campagne.nom).all()
    return render_template('sequences_adn.html',
                           sequences=sequences,
                           form=form,
                           all_campaigns=all_campaigns)


@app.route('/sequences_adn/delete/<int:echantillon_id>',
           methods=['GET', 'POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def delete_echantillon(echantillon_id):
    echantillon = Echantillon.query.get_or_404(echantillon_id)

    if request.method == 'POST':
        filename = echantillon.fichier_sequence

        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            flash(f"Erreur lors de la suppression du fichier : {e}", "danger")

        db.session.delete(echantillon)
        db.session.commit()
        flash(f"L'échantillon '{filename}' a été supprimé avec succès.",
              'success')
        return redirect(url_for('sequences_adn'))

    return render_template('delete_echantillon.html', echantillon=echantillon)


@app.route('/sequences_adn/view/<int:echantillon_id>')
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def view_echantillon(echantillon_id):
    echantillon = Echantillon.query.get_or_404(echantillon_id)
    sequence_content = ""
    error_message = None

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                 echantillon.fichier_sequence)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sequence_content = f.read()
        else:
            error_message = f"Le fichier '{echantillon.fichier_sequence}' est introuvable sur le serveur."
            flash(error_message, 'danger')
    except Exception as e:
        error_message = f"Erreur lors de la lecture du fichier : {e}"
        flash(error_message, 'danger')

    return render_template('view_echantillon.html',
                           echantillon=echantillon,
                           sequence_content=sequence_content,
                           error_message=error_message)


# -------------------------------------------
# ROUTES POUR L'ANALYSE (BUDGET ET ADN)
# -------------------------------------------


@app.route('/budget/', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.DIRECTION, UserRole.ADMIN)
def budget():
    form = BudgetForm()
    if form.validate_on_submit():
        new_budget = Budget(mois=form.mois.data, montant=form.montant.data)
        db.session.add(new_budget)
        db.session.commit()
        flash(
            f"Le budget de {form.montant.data}€ pour {form.mois.data.strftime('%B %Y')} a été ajouté.",
            "success")
        return redirect(url_for('budget'))

    budgets = Budget.query.order_by(Budget.mois.desc()).all()
    return render_template('budget.html', budgets=budgets, form=form)


@app.route('/analyse/', methods=['GET', 'POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def analyse():
    results = request.args.to_dict()
    return render_template('analyse.html', **results)


@app.route('/analyse/generate', methods=['POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
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
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def analyse_mutate():
    sequence = request.form.get('sequence_to_mutate', '').upper()
    mutation_rate = request.form.get('mutation_rate', '0.1')
    if not sequence:
        flash("Une séquence est requise pour la mutation.", "danger")
        return redirect(url_for('analyse'))
    try:
        rate = float(mutation_rate)
        mutated_sequence = algoADN.muter_complet(sequence,
                                                 p_remplacement=rate,
                                                 p_insertion=rate,
                                                 p_delation=rate)
        return redirect(
            url_for('analyse',
                    mutated_sequence=mutated_sequence,
                    original_for_mutation=sequence))
    except (ValueError, TypeError):
        flash("Veuillez entrer un taux de mutation valide (ex: 0.1).",
              "danger")
        return redirect(url_for('analyse'))


@app.route('/analyse/levenshtein', methods=['POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def analyse_levenshtein():
    seq1 = request.form.get('seq1', '').upper()
    seq2 = request.form.get('seq2', '').upper()
    if not seq1 or not seq2:
        flash("Les deux séquences sont requises pour calculer la distance.",
              "danger")
        return redirect(url_for('analyse'))

    distance = calculSimilarite.distance_levenshtein(seq1, seq2)
    return redirect(
        url_for('analyse', distance=distance, seq1_lev=seq1, seq2_lev=seq2))


@app.route('/analyse/align', methods=['POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def analyse_align():
    seq1 = request.form.get('seq1_align', '').upper()
    seq2 = request.form.get('seq2_align', '').upper()
    if not seq1 or not seq2:
        flash("Les deux séquences sont requises pour l'alignement.", "danger")
        return redirect(url_for('analyse'))

    aligned_seq1, aligned_seq2 = algoADN.aligner_sequences(seq1, seq2)
    return redirect(
        url_for('analyse',
                aligned_seq1=aligned_seq1,
                aligned_seq2=aligned_seq2))


@app.route('/analyse/tree', methods=['POST'])
@login_required
@role_required(UserRole.CHERCHEUR, UserRole.ADMIN)
def analyse_tree():
    species_names = request.form.getlist('species-name')
    species_sequences = request.form.getlist('species-sequence')

    if len(species_names) < 2:
        flash(
            "Veuillez fournir au moins deux espèces pour construire l'arbre.",
            "danger")
        return redirect(url_for('analyse'))

    especes = []
    original_sequences_text = []
    for name, seq in zip(species_names, species_sequences):
        if name.strip() and seq.strip():
            especes.append(
                arbresPhylogenetiques.Espece(nom=name.strip(),
                                             adn=seq.strip().upper()))
            original_sequences_text.append(
                f">{name.strip()}\n{seq.strip().upper()}")

    if len(especes) < 2:
        flash(
            "Veuillez fournir au moins deux espèces valides avec un nom et une séquence.",
            "danger")
        return redirect(url_for('analyse'))

    arbre_racine = arbresPhylogenetiques.reconstruire_arbre(especes)

    lignes_arbre = arbresPhylogenetiques.afficher_arbre_text(arbre_racine)
    arbre_formate = "\n".join(lignes_arbre)

    return redirect(
        url_for('analyse',
                newick_tree=arbre_formate,
                original_sequences_tree="\n".join(original_sequences_text)))
