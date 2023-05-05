from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

lm = LoginManager()
db = SQLAlchemy()

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
