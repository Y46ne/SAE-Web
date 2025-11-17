import click
from .app import app, db
import yaml
from datetime import datetime, date
from decimal import Decimal

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    return True
@app.cli.command()
def syncdb():
    """
    Creates all missin tables
    """
    db.create_all()
    lg.warning("Database sunchronized!")


@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newuser(login, pwd):
    '''Adds a new user''' 
    from .database import User
    from hashlib import sha256
    m = sha256()
    m.update(pwd.encode())
    unUser = User(Login=login ,Password =m.hexdigest())
    db.session.add(unUser)
    db.session.commit()
    lg.warning('User ' + login + ' created!')

import click
from .app import db
from hashlib import sha256 


@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newpassword(login, pwd):
    """Met à jour le mot de passe pour l'utilisateur donné."""
    user = User.query.get(login)
    if not user:
        click.echo(f"Utilisateur '{login}' introuvable.")
        return

    m = sha256()
    m.update(pwd.encode())
    user.Password = m.hexdigest()
    db.session.commit()

    click.echo(f"Mot de passe de l'utilisateur '{login}' mis à jour avec succès.")
