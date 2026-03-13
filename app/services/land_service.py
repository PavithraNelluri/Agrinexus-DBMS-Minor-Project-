from app.db.database import mysql
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
        "SELECT * FROM lands WHERE aadhar_id=%s AND deleted=FALSE",
        (aadhar_id,)
    )

    lands = cursor.fetchall()

    cursor.close()

    return lands


def search_lands(aadhar_id, location):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM lands WHERE aadhar_id=%s AND location LIKE %s AND deleted=FALSE",
        (aadhar_id, '%' + location + '%')
    )

    lands = cursor.fetchall()

    cursor.close()

    return lands


def add_land(aadhar_id, location, soil_type, land_size):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        INSERT INTO lands (aadhar_id, location, soil_type, land_size)
        VALUES (%s,%s,%s,%s)
        """,
        (aadhar_id, location, soil_type, land_size)
    )

    mysql.connection.commit()

    cursor.close()


def update_land(aadhar_id, land_id, location, soil_type, land_size):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE lands
        SET location=%s, soil_type=%s, land_size=%s
        WHERE aadhar_id=%s AND land_id=%s
        """,
        (location, soil_type, land_size, aadhar_id, land_id)
    )

    mysql.connection.commit()

    cursor.close()


def delete_land(aadhar_id, land_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE lands
        SET deleted=TRUE
        WHERE aadhar_id=%s AND land_id=%s
        """,
        (aadhar_id, land_id)
    )

    mysql.connection.commit()

    cursor.close()