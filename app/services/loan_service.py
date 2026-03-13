from app.db.database import mysql
import MySQLdb


def get_loans(search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM loans WHERE loan_type LIKE %s AND deleted=FALSE",
            ('%' + search + '%',)
        )
    else:
        cursor.execute(
            "SELECT * FROM loans WHERE deleted=FALSE"
        )

    loans = cursor.fetchall()

    cursor.close()

    return loans


def add_loan(data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM loans WHERE loan_type=%s AND deleted=FALSE",
        (data["loan_type"],)
    )

    if cursor.fetchone():
        cursor.close()
        return "exists"

    cursor.execute(
        """
        INSERT INTO loans (loan_type,description,eligibility)
        VALUES (%s,%s,%s)
        """,
        (
            data["loan_type"],
            data["description"],
            data["eligibility"]
        )
    )

    mysql.connection.commit()

    cursor.close()

    return "success"


def update_loan(id, description, eligibility):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE loans
        SET description=%s, eligibility=%s
        WHERE loan_id=%s
        """,
        (description, eligibility, id)
    )

    mysql.connection.commit()

    cursor.close()


def delete_loan(loan_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "UPDATE loans SET deleted=TRUE WHERE loan_id=%s",
        (loan_id,)
    )

    mysql.connection.commit()

    cursor.close()

def get_farmer(aadhar_id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM farmers WHERE aadhar_id=%s",
        (aadhar_id,)
    )

    farmer = cursor.fetchone()

    cursor.close()

    return farmer


def get_loans_taken(aadhar_id, search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:

        cursor.execute("""
            SELECT lt.*, l.loan_type
            FROM loans_taken lt
            JOIN loans l ON lt.loan_type = l.loan_type
            WHERE lt.aadhar_id=%s AND l.loan_type LIKE %s
        """,(aadhar_id, '%' + search + '%'))

    else:

        cursor.execute("""
            SELECT lt.*, l.loan_type
            FROM loans_taken lt
            JOIN loans l ON lt.loan_type = l.loan_type
            WHERE lt.aadhar_id=%s
        """,(aadhar_id,))

    loans = cursor.fetchall()

    cursor.close()

    return loans


def get_active_loans():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT loan_type FROM loans WHERE deleted=FALSE"
    )

    loans = cursor.fetchall()

    cursor.close()

    return loans


def add_loan_taken(data):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO loans_taken
        (loan_type,aadhar_id,bank_name,sanction_date,due_date,amount_taken,status)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,(
        data["loan_type"],
        data["aadhar_id"],
        data["bank_name"],
        data["sanction_date"],
        data["due_date"],
        data["amount"],
        data["status"]
    ))

    mysql.connection.commit()

    cursor.close()


def update_loan_taken(aadhar_id, loan_type, sanction_date, status):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE loans_taken
        SET status=%s
        WHERE aadhar_id=%s AND loan_type=%s AND sanction_date=%s
    """,(status,aadhar_id,loan_type,sanction_date))

    mysql.connection.commit()

    cursor.close()


def delete_loan_taken(aadhar_id, loan_type, sanction_date):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM loans_taken
        WHERE aadhar_id=%s AND loan_type=%s AND sanction_date=%s
    """,(aadhar_id,loan_type,sanction_date))

    mysql.connection.commit()

    cursor.close()