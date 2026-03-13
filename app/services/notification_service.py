from app.db.database import mysql
import MySQLdb
from twilio.rest import Client

account_sid = "YOUR_ACCOUNT_SID"
auth_token = "YOUR_AUTH_TOKEN"

client = Client(account_sid, auth_token)


def send_notifications():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT notification_id, aadhar_id, message FROM notifications WHERE is_sent = FALSE"
    )

    notifications = cursor.fetchall()

    for notification in notifications:

        notification_id = notification["notification_id"]
        aadhar_id = notification["aadhar_id"]
        message_content = notification["message"]

        cursor.execute(
            "SELECT phone_no FROM farmers WHERE aadhar_id=%s",
            (aadhar_id,)
        )

        farmer = cursor.fetchone()

        if farmer:

            phone_no = farmer["phone_no"]

            try:

                client.messages.create(
                    body=message_content,
                    from_="YOUR_TWILIO_NUMBER",
                    to=f"+91{phone_no}"
                )

                cursor.execute(
                    "UPDATE notifications SET is_sent=TRUE WHERE notification_id=%s",
                    (notification_id,)
                )

                mysql.connection.commit()

            except Exception as e:

                print(f"SMS failed: {e}")

    cursor.close()