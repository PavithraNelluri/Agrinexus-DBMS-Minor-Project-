from app.db.database import mysql
import MySQLdb


def get_subsidies(search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute(
            "SELECT * FROM subsidies WHERE subsidy_name LIKE %s AND deleted=FALSE",
            ('%' + search + '%',)
        )
    else:
        cursor.execute(
            "SELECT * FROM subsidies WHERE deleted=FALSE"
        )

    subsidies = cursor.fetchall()

    cursor.close()

    return subsidies


def add_subsidy(data):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM subsidies WHERE subsidy_name=%s AND deleted=FALSE",
        (data["name"],)
    )

    if cursor.fetchone():
        cursor.close()
        return "exists"

    cursor.execute(
        """
        INSERT INTO subsidies
        (subsidy_name,description,eligibility,last_date_apply)
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

    return "success"


def update_subsidy(id, description, eligibility, last_date):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE subsidies
        SET description=%s, eligibility=%s, last_date_apply=%s
        WHERE subsidy_id=%s
        """,
        (description, eligibility, last_date, id)
    )

    mysql.connection.commit()

    cursor.close()


def delete_subsidy(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "UPDATE subsidies SET deleted=TRUE WHERE subsidy_id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()

def get_subsidies_taken(aadhar_id, search=None):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if search:
        cursor.execute("""
            SELECT st.*, s.subsidy_name
            FROM subsidies_taken st
            JOIN subsidies s ON st.subsidy_name=s.subsidy_name
            WHERE st.aadhar_id=%s AND s.subsidy_name LIKE %s
        """,(aadhar_id,'%' + search + '%'))
    else:
        cursor.execute("""
            SELECT st.*, s.subsidy_name
            FROM subsidies_taken st
            JOIN subsidies s ON st.subsidy_name=s.subsidy_name
            WHERE st.aadhar_id=%s
        """,(aadhar_id,))

    subsidies = cursor.fetchall()

    cursor.close()

    return subsidies


def get_active_subsidies():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT subsidy_name FROM subsidies WHERE deleted=FALSE"
    )

    subsidies = cursor.fetchall()

    cursor.close()

    return subsidies


def add_subsidy_taken(aadhar_id, subsidy_name, sanction_date):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        INSERT INTO subsidies_taken
        (subsidy_name,aadhar_id,sanction_date)
        VALUES (%s,%s,%s)
        """,
        (subsidy_name, aadhar_id, sanction_date)
    )

    mysql.connection.commit()

    cursor.close()


def delete_subsidy_taken(aadhar_id, subsidy_name, sanction_date):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM subsidies_taken
        WHERE aadhar_id=%s AND subsidy_name=%s AND sanction_date=%s
        """,
        (aadhar_id, subsidy_name, sanction_date)
    )

    mysql.connection.commit()

    cursor.close()