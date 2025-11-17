from flask import render_template, request, url_for, redirect, flash
from hashlib import sha256
from .app import app, db, login_manager
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