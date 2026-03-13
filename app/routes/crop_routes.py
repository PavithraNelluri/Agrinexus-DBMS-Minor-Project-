from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import crop_service

crop_bp = Blueprint('crop', __name__)


@crop_bp.route('/manage_crops/<aadhar_id>')
def manage_crops(aadhar_id):

    if 'auth_email' not in session:
        flash("Please login first","error")
        return redirect(url_for('auth.auth_login'))

    farmer = crop_service.get_farmer(aadhar_id)

    if not farmer:
        flash("Farmer not found","error")
        return redirect(url_for('home.home'))

    lands = crop_service.get_lands(aadhar_id)

    search_crop = request.args.get("search_crop")

    if search_crop:
        crops = crop_service.search_crops(aadhar_id, search_crop)

        if not crops:
            flash("No crops found","error")
    else:
        crops = crop_service.get_crops(aadhar_id)

    return render_template(
        "manage_crops.html",
        farmer=farmer,
        crops=crops,
        available_lands=lands
    )


@crop_bp.route('/add_crop/<aadhar_id>', methods=['POST'])
def add_crop(aadhar_id):

    if 'auth_email' not in session:
        flash("Permission denied","error")
        return redirect(url_for('auth.auth_login'))

    data = {
        "land_id":request.form.get("land_id"),
        "aadhar_id":aadhar_id,
        "crop_name":request.form.get("crop_name"),
        "crop_size":request.form.get("crop_size"),
        "N":float(request.form.get("N_percent")),
        "P":float(request.form.get("P_percent")),
        "K":float(request.form.get("K_percent")),
        "ph":float(request.form.get("soil_ph")),
        "planting_date":request.form.get("planting_date"),
        "harvest_date":request.form.get("harvest_date")
    }

    try:

        suggestion = crop_service.add_crop(data)

        if suggestion:
            flash(f"Suggested crop: {suggestion}","success")

        flash("Crop added successfully","success")

    except Exception as e:

        flash(f"Error adding crop: {str(e)}","error")

    return redirect(url_for("crop.manage_crops", aadhar_id=aadhar_id))


@crop_bp.route('/delete_crop/<aadhar_id>/<land_id>/<crop_name>/<planting_date>', methods=['POST'])
def delete_crop(aadhar_id, land_id, crop_name, planting_date):

    if 'auth_email' not in session:
        flash("Permission denied","error")
        return redirect(url_for('auth.auth_login'))

    try:

        crop_service.delete_crop(
            land_id,
            crop_name,
            planting_date
        )

        flash("Crop deleted successfully","success")

    except Exception as e:

        flash(f"Error deleting crop: {str(e)}","error")

    return redirect(url_for("crop.manage_crops", aadhar_id=aadhar_id))