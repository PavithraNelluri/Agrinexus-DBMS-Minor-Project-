from app.db.database import mysql
import MySQLdb


def get_farmer(aadhar_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM farmers WHERE aadhar_id=%s",(aadhar_id,))
    farmer = cursor.fetchone()
    cursor.close()
    return farmer


def update_farmer(old_aadhar, data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        UPDATE farmers
        SET farmer_name=%s,
            date_of_birth=%s,
            gender=%s,
            phone_no=%s,
            address=%s,
            aadhar_id=%s
        WHERE aadhar_id=%s
    """,(
        data["name"],
        data["dob"],
        data["gender"],
        data["phone"],
        data["address"],
        data["aadhar"],
        old_aadhar
    ))

    mysql.connection.commit()
    cursor.close()


def delete_farmer(aadhar_id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "DELETE FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    mysql.connection.commit()
    cursor.close()

def add_farmer(data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        INSERT INTO farmers
        (farmer_name,date_of_birth,gender,phone_no,address,aadhar_id)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,(
        data["name"],
        data["dob"],
        data["gender"],
        data["phone"],
        data["address"],
        data["aadhar"]
    ))

    mysql.connection.commit()
    cursor.close()


def check_aadhar_exists(aadhar):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar,)
    )

    result = cursor.fetchone()
    cursor.close()

    return result


def check_phone_exists(phone):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM farmers WHERE phone_no=%s",
        (phone,)
    )

    result = cursor.fetchone()
    cursor.close()

    return result