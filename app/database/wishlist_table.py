from . import get_connection

def create_product_wishlist_table():
    db = get_connection()
    if not db: return

    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS wishlist_items (
        wishlist_item_id INT PRIMARY KEY,
        user_id INT,
        product_id INT,
        quantity INT NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()