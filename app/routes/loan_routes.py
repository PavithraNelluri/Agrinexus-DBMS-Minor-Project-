from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import loan_service

loan_bp = Blueprint('loan', __name__)


@loan_bp.route('/manage_loans')
def manage_loans():

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    search = request.args.get("loan_type")

    loans = loan_service.get_loans(search)

    if search and not loans:
        flash("No loans found","error")

    return render_template(
        "manage_loans.html",
        loans=loans,
        auth_name=session.get("auth_name")
    )


@loan_bp.route('/add_loan', methods=['POST'])
def add_loan():

    if 'auth_email' not in session:
        return redirect(url_for('auth.auth_login'))

    data = {
        "loan_type":request.form.get("loan_type"),
        "description":request.form.get("description"),
        "eligibility":request.form.get("eligibility")
    }

    result = loan_service.add_loan(data)

    if result == "exists":
        flash("Loan type already exists","error")
    else:
        flash("Loan added successfully","success")

    return redirect(url_for("loan.manage_loans"))


@loan_bp.route('/update_loan/<int:id>', methods=['POST'])
def update_loan(id):

    description = request.form.get("description")
    eligibility = request.form.get("eligibility")

    loan_service.update_loan(id, description, eligibility)

    flash("Loan updated successfully","success")

    return redirect(url_for("loan.manage_loans"))


@loan_bp.route('/delete_loan/<int:loan_id>', methods=['POST'])
def delete_loan(loan_id):

    loan_service.delete_loan(loan_id)

    flash("Loan deleted successfully","success")

    return redirect(url_for("loan.manage_loans"))

@loan_bp.route('/manage_loans_taken/<aadhar_id>')
def manage_loans_taken(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    farmer = loan_service.get_farmer(aadhar_id)

    if not farmer:
        flash("Farmer not found","error")
        return redirect(url_for('farmer.home'))

    search = request.args.get("search_loan_taken")

    loans = loan_service.get_loans_taken(aadhar_id, search)

    active_loans = loan_service.get_active_loans()

    return render_template(
        "manage_loans_taken.html",
        farmer=farmer,
        loans_taken=loans,
        active_loans=active_loans
    )


@loan_bp.route('/add_loan_taken/<aadhar_id>', methods=['POST'])
def add_loan_taken(aadhar_id):

    data = {
        "loan_type":request.form.get("loan_type"),
        "aadhar_id":aadhar_id,
        "bank_name":request.form.get("bank_name"),
        "sanction_date":request.form.get("sanction_date"),
        "due_date":request.form.get("due_date"),
        "amount":request.form.get("amount_taken"),
        "status":request.form.get("status")
    }

    loan_service.add_loan_taken(data)

    flash("Loan taken added successfully","success")

    return redirect(url_for("loan.manage_loans_taken", aadhar_id=aadhar_id))


@loan_bp.route('/update_loan_taken/<aadhar_id>/<loan_type>/<sanction_date>', methods=['POST'])
def update_loan_taken(aadhar_id, loan_type, sanction_date):

    status = request.form.get("status")

    loan_service.update_loan_taken(aadhar_id, loan_type, sanction_date, status)

    flash("Loan status updated","success")

    return redirect(url_for("loan.manage_loans_taken", aadhar_id=aadhar_id))


@loan_bp.route('/delete_loan_taken/<aadhar_id>/<loan_type>/<sanction_date>', methods=['POST'])
def delete_loan_taken(aadhar_id, loan_type, sanction_date):

    loan_service.delete_loan_taken(aadhar_id, loan_type, sanction_date)

    flash("Loan deleted successfully","success")

    return redirect(url_for("loan.manage_loans_taken", aadhar_id=aadhar_id))