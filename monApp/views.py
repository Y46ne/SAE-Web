from flask import render_template, request, url_for, redirect, flash
from hashlib import sha256
from .app import app, db, login_manager
from config import *


@app.route('/')
def index():
    return redirect(url_for('tableau_de_bord'))

@app.route('/tableau_de_bord/')
def tableau_de_bord():
    return render_template('tableau_de_bord.html')



# ------------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)