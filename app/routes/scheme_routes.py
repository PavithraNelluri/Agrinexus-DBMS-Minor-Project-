from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import scheme_service

scheme_bp = Blueprint('scheme', __name__)

# Manage Schemes

@scheme_bp.route('/manage_schemes')
def manage_schemes():

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    search = request.args.get("scheme_name")

    schemes = scheme_service.get_schemes(search)

    return render_template(
        "manage_schemes.html",
        schemes=schemes
    )


# Add Scheme

@scheme_bp.route('/add_scheme', methods=['POST'])
def add_scheme():

    data = {
        "name":request.form.get("scheme_name"),
        "description":request.form.get("description"),
        "eligibility":request.form.get("eligibility"),
        "last_date":request.form.get("last_date_apply")
    }

    result = scheme_service.add_scheme(data)

    if result == "exists":
        flash("Scheme already exists","error")
    else:
        flash("Scheme added successfully","success")

    return redirect(url_for("scheme.manage_schemes"))


# Update Scheme

@scheme_bp.route('/update_scheme/<int:id>', methods=['POST'])
def update_scheme(id):

    description = request.form.get("description")
    eligibility = request.form.get("eligibility")
    last_date = request.form.get("last_date_apply")

    scheme_service.update_scheme(id,description,eligibility,last_date)

    flash("Scheme updated successfully","success")

    return redirect(url_for("scheme.manage_schemes"))


# Delete Scheme

@scheme_bp.route('/delete_scheme/<int:scheme_id>', methods=['POST'])
def delete_scheme(scheme_id):

    scheme_service.delete_scheme(scheme_id)

    flash("Scheme deleted successfully","success")

    return redirect(url_for("scheme.manage_schemes"))


# Schemes Taken

@scheme_bp.route('/manage_schemes_taken/<aadhar_id>')
def manage_schemes_taken(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    search = request.args.get("search_scheme_taken")

    schemes_taken = scheme_service.get_schemes_taken(aadhar_id,search)

    active_schemes = scheme_service.get_active_schemes()

    return render_template(
        "manage_schemes_taken.html",
        schemes_taken=schemes_taken,
        active_schemes=active_schemes,
        farmer={"aadhar_id":aadhar_id}
    )


# Add Scheme Taken

@scheme_bp.route('/add_scheme_taken/<aadhar_id>', methods=['POST'])
def add_scheme_taken(aadhar_id):

    scheme_name = request.form.get("scheme_name")
    approval_date = request.form.get("approval_date")

    scheme_service.add_scheme_taken(
        aadhar_id,
        scheme_name,
        approval_date
    )

    flash("Scheme taken added successfully","success")

    return redirect(url_for("scheme.manage_schemes_taken", aadhar_id=aadhar_id))


# Delete Scheme Taken

@scheme_bp.route('/delete_scheme_taken/<aadhar_id>/<scheme_name>/<approval_date>', methods=['POST'])
def delete_scheme_taken(aadhar_id,scheme_name,approval_date):

    scheme_service.delete_scheme_taken(
        aadhar_id,
        scheme_name,
        approval_date
    )

    flash("Scheme deleted successfully","success")

    return redirect(url_for("scheme.manage_schemes_taken", aadhar_id=aadhar_id))