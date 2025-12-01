from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'monApp/uploads'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
app.config['SQLALCHEMY_ECHO'] = True

@login_manager.user_loader
def load_user(user_id):
    from .models import User 
    return User.query.get(int(user_id))


from . import commands
from . import views
