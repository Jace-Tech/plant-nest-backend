from . import get_connection

def create_admin_table():
    db = get_connection()

    if not db: return

    connection, cursor = db
    sql = """CREATE TABLE IF NOT EXISTS `admins` (
        `admin_id` VARCHAR(20) PRIMARY KEY,
        `name` VARCHAR(50), 
        `email` VARCHAR(100) UNIQUE NOT NULL,
        `image` VARCHAR(100) DEFAULT NULL,
        `password` VARCHAR(255) NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()


def get_admin():
    db = get_connection()
    if not db: return

    conn, cursor = db
    sql = "SELECT * admins"
    cursor.execute(sql)
    admin = cursor.fetchone()
    conn.close()
    return admin

