import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)


def _is_admin_signup(admin_key_input: str | None) -> bool:
    """Return True if the provided admin key matches the configured key."""
    expected = current_app.config.get("ADMIN_SIGNUP_KEY") or os.environ.get(
        "ADMIN_SIGNUP_KEY", ""
    )
    if not expected:
        return False
    return (admin_key_input or "") == expected


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html", user=current_user)

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Email does not exist.", category="error")
        return render_template("sign_in.html", user=current_user)

    if not check_password_hash(user.password, password):
        flash("Incorrect password, try again.", category="error")
        return render_template("sign_in.html", user=current_user)

    login_user(user, remember=True)
    flash("Logged in successfully!", category="success")

    return redirect(url_for("views.product_management" if user.admin else "views.home"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html", user=current_user)

    email = (request.form.get("email") or "").strip().lower()
    first_name = (request.form.get("firstName") or "").strip()
    password1 = request.form.get("password1") or ""
    password2 = request.form.get("password2") or ""
    admin_key_input = request.form.get("adminKey")

    # Basic validation
    if len(email) < 4:
        flash("Email must be greater than 3 characters.", category="error")
        return render_template("sign_up.html", user=current_user)

    if len(first_name) < 1:
        flash("First name must be at least 1 character.", category="error")
        return render_template("sign_up.html", user=current_user)

    if password1 != password2:
        flash("Passwords do not match.", category="error")
        return render_template("sign_up.html", user=current_user)

    if len(password1) < 6:
        flash("Password must be at least 6 characters.", category="error")
        return render_template("sign_up.html", user=current_user)

    if User.query.filter_by(email=email).first():
        flash("Email already exists.", category="error")
        return render_template("sign_up.html", user=current_user)

    admin = _is_admin_signup(admin_key_input)

    new_user = User(
        email=email,
        first_name=first_name,
        admin=admin,
        password=generate_password_hash(password1, method="pbkdf2:sha256"),
    )
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=True)
    flash("Account created!", category="success")

    return redirect(url_for("views.product_management" if admin else "auth.sign_in"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.sign_in"))
