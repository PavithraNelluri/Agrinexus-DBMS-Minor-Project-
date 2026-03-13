from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import land_service

land_bp = Blueprint('land', __name__)


@land_bp.route('/manage_lands/<aadhar_id>')
def manage_lands(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    farmer = land_service.get_farmer(aadhar_id)

    if not farmer:
        flash("Farmer not found","error")
        return redirect(url_for('farmer.home'))

    search_land = request.args.get("search_land")

    if search_land:
        lands = land_service.search_lands(aadhar_id, search_land)

        if not lands:
            flash("No lands found for this location","error")
    else:
        lands = land_service.get_lands(aadhar_id)

    return render_template(
        "manage_lands.html",
        farmer=farmer,
        lands=lands
    )


@land_bp.route('/add_land/<aadhar_id>', methods=['POST'])
def add_land(aadhar_id):

    if 'auth_email' not in session:
        flash("Permission denied","error")
        return redirect(url_for('auth.auth_login'))

    location = request.form.get("location")
    soil_type = request.form.get("soil_type")
    land_size = request.form.get("land_size")

    try:

        land_service.add_land(
            aadhar_id,
            location,
            soil_type,
            land_size
        )

        flash("Land added successfully","success")

    except Exception as e:

        flash(f"Error adding land: {str(e)}","error")

    return redirect(url_for("land.manage_lands", aadhar_id=aadhar_id))


@land_bp.route('/update_land/<aadhar_id>/<int:land_id>', methods=['POST'])
def update_land(aadhar_id, land_id):

    if 'auth_email' not in session:
        flash("Permission denied","error")
        return redirect(url_for('auth.auth_login'))

    location = request.form.get("location")
    soil_type = request.form.get("soil_type")
    land_size = request.form.get("land_size")

    try:

        land_service.update_land(
            aadhar_id,
            land_id,
            location,
            soil_type,
            land_size
        )

        flash("Land updated successfully","success")

    except Exception as e:

        flash(f"Error updating land: {str(e)}","error")

    return redirect(url_for("land.manage_lands", aadhar_id=aadhar_id))


@land_bp.route('/delete_land/<aadhar_id>/<int:land_id>', methods=['POST'])
def delete_land(aadhar_id, land_id):

    if 'auth_email' not in session:
        flash("Permission denied","error")
        return redirect(url_for('auth.auth_login'))

    try:

        land_service.delete_land(aadhar_id, land_id)

        flash("Land deleted successfully","success")

    except Exception as e:

        flash(f"Error deleting land: {str(e)}","error")

    return redirect(url_for("land.manage_lands", aadhar_id=aadhar_id))