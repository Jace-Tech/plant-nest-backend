from . import get_connection

def create_category_table():
  db = get_connection()

  if not db: return

  connection, cursor = db
  sql = """CREATE TABLE IF NOT EXISTS categories (
      `category_id` VARCHAR(20) PRIMARY KEY,
      `name` VARCHAR(50)
  )"""

  cursor.execute(sql)
  connection.commit()
  print("TABLE CREATED!")
  connection.close()
