from mysql.connector import connect
from ..utils.variables import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER

def get_connection():
  try:
    connection = connect(
      host=MYSQL_HOST,
      user=MYSQL_USER,
      password=MYSQL_PASSWORD,
      database=MYSQL_DB,
      port=MYSQL_PORT,
    )

    cursor = connection.cursor(buffered=True, dictionary=True)

    return connection, cursor
  except Exception as e:
    print("DATABASE ERROR:", str(e))
    return None
    