from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import subsidy_service

subsidy_bp = Blueprint('subsidy', __name__)


# =========================
# Manage Subsidies (Admin)
# =========================

@subsidy_bp.route('/manage_subsidies')
def manage_subsidies():

    if 'auth_email' not in session:
        flash("Please login first", "error")
        return redirect(url_for('auth.auth_login'))

    search = request.args.get("subsidy_name")

    subsidies = subsidy_service.get_subsidies(search)

    if search and not subsidies:
        flash("No subsidies found", "error")

    return render_template(
        "manage_subsidies.html",
        subsidies=subsidies
    )


# =========================
# Add Subsidy
# =========================

@subsidy_bp.route('/add_subsidy', methods=['POST'])
def add_subsidy():

    if 'auth_email' not in session:
        flash("Please login first", "error")
        return redirect(url_for('auth.auth_login'))

    data = {
        "name": request.form.get("subsidy_name"),
        "description": request.form.get("description"),
        "eligibility": request.form.get("eligibility"),
        "last_date": request.form.get("last_date_apply")
    }

    result = subsidy_service.add_subsidy(data)

    if result == "exists":
        flash("Subsidy already exists", "error")
    else:
        flash("Subsidy added successfully", "success")

    return redirect(url_for("subsidy.manage_subsidies"))


# =========================
# Update Subsidy
# =========================

@subsidy_bp.route('/update_subsidy/<int:id>', methods=['POST'])
def update_subsidy(id):

    description = request.form.get("description")
    eligibility = request.form.get("eligibility")
    last_date = request.form.get("last_date_apply")

    subsidy_service.update_subsidy(id, description, eligibility, last_date)

    flash("Subsidy updated successfully", "success")

    return redirect(url_for("subsidy.manage_subsidies"))


# =========================
# Delete Subsidy
# =========================

@subsidy_bp.route('/delete_subsidy/<int:subsidy_id>', methods=['POST'])
def delete_subsidy(subsidy_id):

    subsidy_service.delete_subsidy(subsidy_id)

    flash("Subsidy deleted successfully", "success")

    return redirect(url_for("subsidy.manage_subsidies"))


# ====================================
# Manage Subsidies Taken by Farmers
# ====================================

@subsidy_bp.route('/manage_subsidies_taken/<aadhar_id>')
def manage_subsidies_taken(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first", "error")
        return redirect(url_for('auth.auth_login'))

    search = request.args.get("search_subsidy_taken")

    subsidies_taken = subsidy_service.get_subsidies_taken(aadhar_id, search)

    active_subsidies = subsidy_service.get_active_subsidies()

    return render_template(
        "manage_subsidies_taken.html",
        subsidies_taken=subsidies_taken,
        active_subsidies=active_subsidies,
        farmer={"aadhar_id": aadhar_id}
    )


# =========================
# Add Subsidy Taken
# =========================

@subsidy_bp.route('/add_subsidy_taken/<aadhar_id>', methods=['POST'])
def add_subsidy_taken(aadhar_id):

    subsidy_name = request.form.get("subsidy_name")
    sanction_date = request.form.get("sanction_date")

    subsidy_service.add_subsidy_taken(
        aadhar_id,
        subsidy_name,
        sanction_date
    )

    flash("Subsidy taken added successfully", "success")

    return redirect(url_for("subsidy.manage_subsidies_taken", aadhar_id=aadhar_id))


# =========================
# Delete Subsidy Taken
# =========================

@subsidy_bp.route('/delete_subsidy_taken/<aadhar_id>/<subsidy_name>/<sanction_date>', methods=['POST'])
def delete_subsidy_taken(aadhar_id, subsidy_name, sanction_date):

    subsidy_service.delete_subsidy_taken(
        aadhar_id,
        subsidy_name,
        sanction_date
    )

    flash("Subsidy deleted successfully", "success")

    return redirect(url_for("subsidy.manage_subsidies_taken", aadhar_id=aadhar_id))