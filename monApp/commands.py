import click
import yaml
from .app import app, db
from hashlib import sha256
from datetime import datetime, date
from .models import User, Plateforme, Personnel, Budget, Habilitation, Campagne, Echantillon, Maintenance

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Crée les tables et charge les données depuis un fichier YAML."""

    db.drop_all()
    db.create_all()

    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # UTILISATEURS
    for u in data.get('users', []):
        if not User.query.filter_by(username=u['username']).first():
            m = sha256()
            m.update(u['password'].encode())
            user = User(
                username=u['username'],
                password=m.hexdigest()
            )
            db.session.add(user)
    db.session.commit()
    print("Utilisateurs chargés.")

    dict_hab = {}
    dict_pl = {}
    dict_pers = {}
    dict_budg = {}
    dict_camp = {}

    # HABILITATIONS
    for h in data.get('habilitations', []):
        hab = Habilitation(nomHab=h['nom'])
        db.session.add(hab)
        dict_hab[h['id']] = hab
    
    db.session.commit()

    # PLATEFORMES
    for p in data.get('plateformes', []):
        plat = Plateforme(
            nom=p['nom'],
            nb_personnes_necessaires=p['nb_personnes_necessaires'],
            cout_journalier=p['cout_journalier'],
            intervalle_maintenance=p['intervalle_maintenance']
        )
        
        for id_hab in p.get('habilitations_requises', []):
            if id_hab in dict_hab:
                plat.habilitations_requises.append(dict_hab[id_hab])
        
        db.session.add(plat)
        dict_pl[p['id']] = plat
    
    db.session.commit()

    # PERSONNEL
    for pers in data.get('personnel', []):
        personnel = Personnel(nom=pers['nom'])
        
        for id_hab in pers.get('habilitations', []):
            if id_hab in dict_hab:
                personnel.habilitations.append(dict_hab[id_hab])

        db.session.add(personnel)
        dict_pers[pers['id']] = personnel
    
    db.session.commit()

    # BUDGETS
    for b in data.get('budgets', []):
        budget = Budget(
            mois=datetime.strptime(b['mois'], '%Y-%m-%d').date(),
            montant=b['montant']
        )
        db.session.add(budget)
        dict_budg[b['id']] = budget
    
    db.session.commit()

    # CAMPAGNES
    for c in data.get('campagnes', []):
        camp = Campagne(
            date_debut=datetime.strptime(c['date_debut'], '%Y-%m-%d').date(),
            duree=c['duree'],
            lieu=c['lieu']
        )

        if c['id_plateforme'] in dict_pl:
            camp.plateforme = dict_pl[c['id_plateforme']]

        for id_pers in c.get('personnel_implique', []):
            if id_pers in dict_pers:
                camp.personnel_implique.append(dict_pers[id_pers])
        
        if 'id_budget' in c and c['id_budget'] in dict_budg:
             budget_associe = dict_budg[c['id_budget']]
             budget_associe.campagnes_validees.append(camp)

        db.session.add(camp)
        dict_camp[c['id']] = camp

    db.session.commit()

    # ECHANTILLONS
    for e in data.get('echantillons', []):
        ech = Echantillon(
            fichier_sequence=e['fichier_sequence'],
            commentaire=e.get('commentaire')
        )

        if e['id_campagne'] in dict_camp:
            ech.campagne = dict_camp[e['id_campagne']]
        
        for id_pers in e.get('personnel_participant', []):
            if id_pers in dict_pers:
                ech.personnel_participant.append(dict_pers[id_pers])

        db.session.add(ech)
    
    db.session.commit()

    # MAINTENANCES
    for m in data.get('maintenances', []):
        maint = Maintenance(
            date_maintenance=datetime.strptime(m['date_maintenance'], '%Y-%m-%d').date(),
            duree=m['duree'],
            type_operation=m['type_operation']
        )

        if m['id_plateforme'] in dict_pl:
            maint.plateforme = dict_pl[m['id_plateforme']]

        db.session.add(maint)

    db.session.commit()
    print("Base de données initialisée avec succès !")


@app.cli.command()
def syncdb():
    """Crée les tables manquantes."""
    db.create_all()
    print("Tables synchronisées.")

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    """Ajoute un nouvel utilisateur manuellement."""
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    user = User(username=username, password=m.hexdigest())
    db.session.add(user)
    db.session.commit()
    print(f"Utilisateur {username} créé avec succès.")

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newpasswd(username, password):
    """Change le mot de passe d'un utilisateur."""
    from hashlib import sha256
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"Utilisateur {username} introuvable.")
        return
    m = sha256()
    m.update(password.encode())
    user.password = m.hexdigest()
    db.session.commit()
    print(f"Mot de passe mis à jour pour {username}.")