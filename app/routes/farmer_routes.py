from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import farmer_service
from app.db.database import mysql
import MySQLdb
farmer_bp = Blueprint('farmer', __name__)


@farmer_bp.route('/existing_farmers', methods=['GET', 'POST'])
def existing_farmers():

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # STEP 1: handle POST (search request)
    if request.method == 'POST':
        search_aadhar_id = request.form.get('search_f_aadharId')

        return redirect(url_for(
            'farmer.existing_farmers',
            search_f_aadharId=search_aadhar_id
        ))

    # STEP 2: handle GET (after redirect OR normal load)
    search_aadhar_id = request.args.get('search_f_aadharId')

    if search_aadhar_id:
        cursor.execute(
            "SELECT aadhar_id, farmer_name FROM farmers WHERE aadhar_id LIKE %s",
            ('%' + search_aadhar_id + '%',)
        )
        farmers = cursor.fetchall()

        if not farmers:
            flash("Farmer with this Aadhar ID does not exist","error")
    else:
        cursor.execute(
            "SELECT aadhar_id, farmer_name FROM farmers"
        )
        farmers = cursor.fetchall()

    cursor.close()

    return render_template(
        "existingfarmers.html",
        farmers=farmers,
        auth_name=session.get('auth_name')
    )

@farmer_bp.route('/add_farmer', methods=['GET','POST'])
def add_farmer():

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    if request.method == 'POST':

        data = {
            "name": request.form.get('f_name'),
            "dob": request.form.get('f_dob'),
            "gender": request.form.get('f_gender'),
            "phone": request.form.get('f_phone'),
            "address": request.form.get('f_address'),
            "aadhar": request.form.get('f_aadharId')
        }

        # check aadhar conflict
        if farmer_service.check_aadhar_exists(data["aadhar"]):
            flash("Aadhar ID already exists","error")
            return render_template(
                "addfarmer.html",
                auth_name=session.get('auth_name')
            )

        # check phone conflict
        if farmer_service.check_phone_exists(data["phone"]):
            flash("Phone number already exists","error")
            return render_template(
                "addfarmer.html",
                auth_name=session.get('auth_name')
            )

        farmer_service.add_farmer(data)

        flash("Farmer registered successfully!","success")

        return redirect(url_for("farmer.existing_farmers"))

    return render_template(
        "addfarmer.html",
        auth_name=session.get('auth_name')
    )

@farmer_bp.route('/edit_farmer/<aadhar_id>', methods=['GET','POST'])
def edit_farmer(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    farmer = farmer_service.get_farmer(aadhar_id)

    if request.method == 'POST':

        data = {
            "name":request.form.get('f_name'),
            "dob":request.form.get('f_dob'),
            "gender":request.form.get('f_gender'),
            "phone":request.form.get('f_phone'),
            "address":request.form.get('f_address'),
            "aadhar":request.form.get('f_aadharId')
        }

        if data["aadhar"] != farmer["aadhar_id"]:
            if farmer_service.check_aadhar_conflict(data["aadhar"],aadhar_id):
                flash("Aadhar already exists","error")
                return render_template("editfarmer.html",farmer=farmer)

        if data["phone"] != farmer["phone_no"]:
            if farmer_service.check_phone_conflict(data["phone"],aadhar_id):
                flash("Phone number already exists","error")
                return render_template("editfarmer.html",farmer=farmer)

        farmer_service.update_farmer(aadhar_id,data)

        flash("Farmer updated successfully","success")

        return redirect(url_for("farmer.existing_farmers"))

    return render_template("editfarmer.html",farmer=farmer)



@farmer_bp.route('/deletefarmer/<aadhar_id>', methods=['POST'])
def delete_farmer(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    try:

        farmer_service.delete_farmer(aadhar_id)

        flash("Farmer deleted successfully","success")

    except Exception as e:

        flash(f"Error deleting farmer: {str(e)}","error")

    return redirect(url_for("farmer.existing_farmers"))

@farmer_bp.route('/available_loans')
def available_loans():

    loan_type = request.args.get('loan_type')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if loan_type:

        cursor.execute(
            "SELECT * FROM loans WHERE loan_type LIKE %s AND deleted=FALSE",
            ('%' + loan_type + '%',)
        )

        loans = cursor.fetchall()

        if not loans:
            flash("No loans found for this type","error")

    else:

        cursor.execute(
            "SELECT * FROM loans WHERE deleted=FALSE"
        )

        loans = cursor.fetchall()

    cursor.close()

    return render_template(
        "available_loans.html",
        loans=loans
    )

@farmer_bp.route('/available_subsidies')
def available_subsidies():

    subsidy_name = request.args.get('subsidy_name')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if subsidy_name:

        cursor.execute(
            "SELECT * FROM subsidies WHERE subsidy_name LIKE %s AND deleted=FALSE",
            ('%' + subsidy_name + '%',)
        )

        subsidies = cursor.fetchall()

    else:

        cursor.execute(
            "SELECT * FROM subsidies WHERE deleted=FALSE"
        )

        subsidies = cursor.fetchall()

    cursor.close()

    return render_template(
        "available_subsidies.html",
        subsidies=subsidies
    )

@farmer_bp.route('/available_schemes')
def available_schemes():

    scheme_name = request.args.get('scheme_name')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if scheme_name:

        cursor.execute(
            "SELECT * FROM schemes WHERE scheme_name LIKE %s AND deleted=FALSE",
            ('%' + scheme_name + '%',)
        )

        schemes = cursor.fetchall()

    else:

        cursor.execute(
            "SELECT * FROM schemes WHERE deleted=FALSE"
        )

        schemes = cursor.fetchall()

    cursor.close()

    return render_template(
        "available_schemes.html",
        schemes=schemes
    )

