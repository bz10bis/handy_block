from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ansi2html import Ansi2HTMLConverter

from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, BuilderForm, SecretForm
from app.models import User, Secret


import subprocess

def load_key():
    return open("../secret.key", "rb").read()

def get_terraform_plan():
    return subprocess.run(["terraform", "plan"], cwd="../terraform-google/", stdout=subprocess.PIPE, check=True, encoding='utf8')


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Credentials")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, you are now registerd on speedchain")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/secrets", methods=["GET", "POST"])
@login_required
def secrets():
    form = SecretForm()
    if form.validate_on_submit():
        secret = Secret(stype=form.secret_type.data, name=form.secret_name.data, content=form.secret_content.data, user_id=current_user.id)
        db.session.add(secret)
        db.session.commit()
        flash("Secret Saved")
        return redirect(url_for("secrets"))
    return render_template("secrets.html", title="Secrets", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    plans = [
        {"created_by": user.username, "body": "plan1"},
        {"created_by": user.username, "body": "plan2"}
    ]
    secrets = Secret.query.filter_by(user_id=user.id)
    return render_template("user.html", user=user, plans=plans, secrets=secrets)

@app.route("/builder", methods=["GET", "POST"])
@login_required
def builder():
    form = BuilderForm()
    user_secrets = Secret.query.filter_by(user_id=current_user.id)
    print(current_user.id)
    print(user_secrets)
    if form.validate_on_submit():
        conv = Ansi2HTMLConverter()
        plan = get_terraform_plan()
        plan = conv.convert(plan.stdout)
        return render_template("plan.html", plan=plan)
    return render_template("builder.html", form=form, secrets=user_secrets)