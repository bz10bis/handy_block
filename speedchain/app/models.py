from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import enum


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<Users {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(40), nullable=False)
    project_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def __repr__(self):
        return f"<Post: self.body>"


class SecretType(enum.Enum):
    SSH = "ssh"
    PROJECT_JSON = "project_json"


class Secret(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stype = db.Column(db.Enum(SecretType), default=SecretType.SSH, nullable=False)
    content = db.Column(db.String(254), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))