from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db.database import mysql
from app.services.notification_service import send_notifications
import MySQLdb

farmer_portal_bp = Blueprint('farmer_portal', __name__)


# =========================
# Farmer Login
# =========================
@farmer_portal_bp.route('/farmer_login', methods=['GET','POST'])
def farmer_login():

    if request.method == "POST":

        aadhar_id = request.form.get("aadhar_id")
        phone_no = request.form.get("phone_no")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            "SELECT * FROM farmers WHERE aadhar_id=%s AND phone_no=%s",
            (aadhar_id, phone_no)
        )

        farmer = cursor.fetchone()
        cursor.close()

        if farmer:

            session["aadhar_id"] = farmer["aadhar_id"]
            session["farmer_name"] = farmer["farmer_name"]

            flash("Login successful","success")

            return redirect(url_for("farmer_portal.farmer_details"))

        else:
            flash("Invalid Aadhar or phone number","error")

    return render_template("farmer_login.html")


# =========================
# Farmer Details
# =========================
@farmer_portal_bp.route('/farmer_details')
def farmer_details():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()
    cursor.close()

    return render_template("farmer_details.html", farmer=farmer)


# =========================
# Farmer Lands
# =========================
@farmer_portal_bp.route('/farmer_lands')
def farmer_lands():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    search = request.args.get("search_avail_land")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM lands WHERE aadhar_id=%s AND location LIKE %s AND deleted=FALSE",
            (aadhar_id, "%" + search + "%")
        )
    else:
        cursor.execute(
            "SELECT * FROM lands WHERE aadhar_id=%s AND deleted=FALSE",
            (aadhar_id,)
        )

    lands = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return render_template("farmer_lands.html", lands=lands, farmer=farmer)


# =========================
# Farmer Crops
# =========================
@farmer_portal_bp.route('/farmer_crops')
def farmer_crops():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    search = request.args.get("search_avail_crop")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM crops WHERE aadhar_id=%s AND crop_name LIKE %s",
            (aadhar_id, "%" + search + "%")
        )
    else:
        cursor.execute(
            "SELECT * FROM crops WHERE aadhar_id=%s",
            (aadhar_id,)
        )

    crops = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return render_template("farmer_crops.html", crops=crops, farmer=farmer)


# =========================
# Farmer Loans
# =========================
@farmer_portal_bp.route('/farmer_loans_taken')
def farmer_loans_taken():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    search = request.args.get("search_loan_taken")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM loans_taken WHERE aadhar_id=%s AND loan_type LIKE %s",
            (aadhar_id, "%" + search + "%")
        )
    else:
        cursor.execute(
            "SELECT * FROM loans_taken WHERE aadhar_id=%s",
            (aadhar_id,)
        )

    loans_taken = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    send_notifications()

    return render_template(
        "farmer_loans_taken.html",
        loans_taken=loans_taken,
        farmer=farmer
    )


# =========================
# Farmer Subsidies
# =========================
@farmer_portal_bp.route('/farmer_subsidies_taken')
def farmer_subsidies_taken():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    search = request.args.get("search_subsidy_taken")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM subsidies_taken WHERE aadhar_id=%s AND subsidy_name LIKE %s",
            (aadhar_id, "%" + search + "%")
        )
    else:
        cursor.execute(
            "SELECT * FROM subsidies_taken WHERE aadhar_id=%s",
            (aadhar_id,)
        )

    subsidies_taken = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return render_template(
        "farmer_subsidies_taken.html",
        subsidies_taken=subsidies_taken,
        farmer=farmer
    )


# =========================
# Farmer Schemes
# =========================
@farmer_portal_bp.route('/farmer_schemes_taken')
def farmer_schemes_taken():

    aadhar_id = session.get("aadhar_id")

    if not aadhar_id:
        flash("Please login first","error")
        return redirect(url_for("farmer_portal.farmer_login"))

    search = request.args.get("search_scheme_taken")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM schemes_taken WHERE aadhar_id=%s AND scheme_name LIKE %s",
            (aadhar_id, "%" + search + "%")
        )
    else:
        cursor.execute(
            "SELECT * FROM schemes_taken WHERE aadhar_id=%s",
            (aadhar_id,)
        )

    schemes_taken = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return render_template(
        "farmer_schemes_taken.html",
        schemes_taken=schemes_taken,
        farmer=farmer
    )


# =========================
# Logout
# =========================
@farmer_portal_bp.route('/farmer_logout')
def farmer_logout():

    session.clear()

    flash("Logged out successfully","success")

    return redirect(url_for("farmer_portal.farmer_login"))