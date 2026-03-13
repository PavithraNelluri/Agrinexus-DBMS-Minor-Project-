from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models.forms import LoginForm, RegisterForm
from app.services.auth_service import register_admin, login_admin
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth_register', methods=['GET','POST'])
def auth_register():

    form = RegisterForm()

    if form.validate_on_submit():

        register_admin(
            form.auth_name.data,
            form.auth_email.data,
            form.auth_pass.data,
            form.auth_phone_no.data
        )

        flash("Registration successful!", "success")

        return redirect(url_for('auth.auth_login'))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error,"error")

    return render_template("auth_register.html", form=form)


@auth_bp.route('/auth_login', methods=['GET','POST'])
def auth_login():

    form = LoginForm()

    if form.validate_on_submit():

        auth = login_admin(form.auth_email.data)

        if auth and bcrypt.checkpw(
            form.auth_pass.data.encode('utf-8'),
            auth['auth_pass'].encode('utf-8')
        ):

            session['auth_id'] = auth['auth_id']
            session['auth_email'] = auth['auth_email']
            session['auth_name'] = auth['auth_name']

            flash("Login successful!", "success")

            return redirect(url_for('farmer.existing_farmers'))

        else:
            flash("Invalid credentials","error")

    return render_template("auth_login.html", form=form)


@auth_bp.route('/auth_logout')
def auth_logout():

    session.clear()

    flash("Logged out","success")

    return redirect(url_for('auth.auth_login'))