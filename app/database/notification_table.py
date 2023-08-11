from . import get_connection
from ..utils.helpers import generate_id

def create_notification_table():
    db = get_connection()

    if not db: return

    connection, cursor = db
    sql = """CREATE TABLE IF NOT EXISTS notifications (
        `notification_id` VARCHAR(20) PRIMARY KEY,
        `title` VARCHAR(255), 
        `content` TEXT,
        `is_seen` TINYINT DEFAULT 0,
        `user_id` VARCHAR(20),
        FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()

def create_notification(title, message, user_id):
    try:
        db = get_connection()

        if not db: return

        connection, cursor = db
        sql = "INSERT INTO notifications (notification_id, title, content, user_id) VALUES (%s, %s, %s, %s)"

        cursor.execute(sql, (generate_id(), title, message, user_id))
        connection.commit()
        if not cursor.rowcount:
            raise Exception("Error occurred.")
        connection.close()
        return True
    except Exception as e:
        print(e)
        return None
