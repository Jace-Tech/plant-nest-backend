from . import get_connection

def create_product_wishlist_table():
    db = get_connection()

    if not db: return

    connection, cursor = db

    sql = """CREATE TABLE wishlist_items (
    wishlist_item_id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()