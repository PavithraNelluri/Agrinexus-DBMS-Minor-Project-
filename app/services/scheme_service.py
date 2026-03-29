from app.db.database import mysql
import MySQLdb


# Get Schemes

def get_schemes(search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM schemes WHERE scheme_name LIKE %s AND deleted = FALSE",
            ('%' + search + '%',)
        )
    else:
        cursor.execute(
            "SELECT * FROM schemes WHERE deleted = FALSE"
        )

    schemes = cursor.fetchall()

    cursor.close()

    return schemes


# Add Scheme

def add_scheme(data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM schemes WHERE scheme_name = %s AND deleted = FALSE",
        (data["name"],)
    )

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return "exists"

    cursor.execute(
        """
        INSERT INTO schemes (scheme_name, description, eligibility, last_date_apply)
        VALUES (%s,%s,%s,%s)
        """,
        (
            data["name"],
            data["description"],
            data["eligibility"],
            data["last_date"]
        )
    )

    mysql.connection.commit()

    cursor.close()

    return "added"


# Update Scheme

def update_scheme(id, description, eligibility, last_date):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE schemes
        SET description=%s, eligibility=%s, last_date_apply=%s
        WHERE scheme_id=%s
        """,
        (description, eligibility, last_date, id)
    )

    mysql.connection.commit()

    cursor.close()


# Delete Scheme

def delete_scheme(scheme_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "UPDATE schemes SET deleted=TRUE WHERE scheme_id=%s",
        (scheme_id,)
    )

    mysql.connection.commit()

    cursor.close()


# Get Schemes Taken (Farmer)

def get_schemes_taken(aadhar_id, search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute("""
            SELECT sct.*, sc.scheme_name
            FROM schemes_taken sct
            JOIN schemes sc ON sct.scheme_name = sc.scheme_name
            WHERE sct.aadhar_id = %s AND sc.scheme_name LIKE %s
        """, (aadhar_id, "%" + search + "%"))
    else:
        cursor.execute("""
            SELECT sct.*, sc.scheme_name
            FROM schemes_taken sct
            JOIN schemes sc ON sct.scheme_name = sc.scheme_name
            WHERE sct.aadhar_id = %s
        """, (aadhar_id,))

    schemes_taken = cursor.fetchall()

    cursor.close()

    return schemes_taken


# Get Active Schemes

def get_active_schemes():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT scheme_name FROM schemes WHERE deleted = FALSE"
    )

    schemes = cursor.fetchall()

    cursor.close()

    return schemes


# Add Scheme Taken

def add_scheme_taken(aadhar_id, scheme_name, approval_date):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT * FROM schemes_taken
        WHERE scheme_name = %s AND approval_date = %s AND aadhar_id = %s
    """, (scheme_name, approval_date, aadhar_id))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return "exists"

    cursor.execute("""
        INSERT INTO schemes_taken (scheme_name, aadhar_id, approval_date)
        VALUES (%s,%s,%s)
    """, (scheme_name, aadhar_id, approval_date))

    mysql.connection.commit()

    cursor.close()

    return "added"


# Delete Scheme Taken

def delete_scheme_taken(aadhar_id, scheme_name, approval_date):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM schemes_taken
        WHERE aadhar_id = %s AND scheme_name = %s AND approval_date = %s
    """, (aadhar_id, scheme_name, approval_date))

    mysql.connection.commit()

    cursor.close()