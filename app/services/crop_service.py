from app.db.database import mysql
from app.ml.predictor import predict_crop
import MySQLdb


def get_farmer(aadhar_id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return farmer


def get_lands(aadhar_id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT land_id FROM lands WHERE aadhar_id=%s AND deleted=FALSE",
        (aadhar_id,)
    )

    lands = cursor.fetchall()

    cursor.close()

    return lands


def get_crops(aadhar_id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM crops WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    crops = cursor.fetchall()

    cursor.close()

    return crops


def search_crops(aadhar_id, crop_name):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM crops WHERE aadhar_id=%s AND crop_name LIKE %s",
        (aadhar_id, "%" + crop_name + "%")
    )

    crops = cursor.fetchall()

    cursor.close()

    return crops


def delete_crop(land_id, crop_name, planting_date):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM crops
        WHERE land_id=%s AND crop_name=%s AND planting_date=%s
        """,
        (land_id, crop_name, planting_date)
    )

    mysql.connection.commit()

    cursor.close()


def add_crop(data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT location FROM lands WHERE land_id=%s",
        (data["land_id"],)
    )

    land = cursor.fetchone()

    location = land["location"]

    suggestion = predict_crop(
        data["N"],
        data["P"],
        data["K"],
        data["ph"],
        location
    )

    cursor.execute("""
        INSERT INTO crops (
            land_id,aadhar_id,crop_name,crop_size,
            N_percent,P_percent,K_percent,soil_ph,
            planting_date,harvest_date,crop_suggestion
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,(
        data["land_id"],
        data["aadhar_id"],
        data["crop_name"],
        data["crop_size"],
        data["N"],
        data["P"],
        data["K"],
        data["ph"],
        data["planting_date"],
        data["harvest_date"],
        suggestion
    ))

    mysql.connection.commit()

    cursor.close()

    return suggestion