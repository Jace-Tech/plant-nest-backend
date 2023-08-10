from . import get_connection

def create_plant_table():
  db = get_connection()

  if not db: return

  connection, cursor = db
  sql = """CREATE TABLE IF NOT EXISTS plants (
    `plant_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(50), 
    `description` TEXT,
    `price` FLOAT,
    `quantity` INT,
    `image_url` VARCHAR(200),
    `category_id` VARCHAR(20),
    FOREIGN KEY (`category_id`) REFERENCES categories(`category_id`)
  )"""

  cursor.execute(sql)
  connection.commit()
  print("TABLE CREATED!")
  connection.close()
