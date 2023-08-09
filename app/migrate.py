from .database.user_table import create_user_table
from .database.admin_table import create_admin_table
from .database.plant_table import create_plant_table


# RUN MIGRATIONS
create_user_table()
create_admin_table()
create_plant_table()