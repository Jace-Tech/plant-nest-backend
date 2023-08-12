from . import get_connection

def create_product_wishlist_table():
    db = get_connection()
    if not db: return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS wishlist_items (
        wishlist_item_id INT PRIMARY KEY,
        user_id VARCHAR(20),
        product_id  VARCHAR(20),
        quantity INT NOT NULL,
        `date` DATETIME
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()