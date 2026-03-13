import bcrypt
import MySQLdb
from app.db.database import mysql


def register_admin(auth_name, auth_email, auth_pass, auth_phone_no):

    hashed_pass = bcrypt.hashpw(
        auth_pass.encode('utf-8'),
        bcrypt.gensalt()
    )

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        INSERT INTO auths
        (auth_name, auth_email, auth_pass, auth_phone_no)
        VALUES (%s,%s,%s,%s)
    """, (auth_name,auth_email,hashed_pass,auth_phone_no))

    mysql.connection.commit()
    cursor.close()


def login_admin(auth_email):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM auths WHERE auth_email=%s",
        (auth_email,)
    )

    auth = cursor.fetchone()
    cursor.close()

    return auth