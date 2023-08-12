from . import get_connection

def create_product_cart_table():
    db = get_connection()
    if not db: return
    connection, cursor = db

    sql = """CREATE TABLE IF NOT EXISTS cart_items (
        cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id VARCHAR(20),
        product_id VARCHAR(20),
        quantity INT NOT NULL
    )"""

    cursor.execute(sql)
    connection.commit()
    print("TABLE CREATED!")
    connection.close()