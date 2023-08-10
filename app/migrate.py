from .database.user_table import create_user_table
from .database.admin_table import create_admin_table
from .database.plant_table import create_plant_table
from .database.category_table import create_category_table


# RUN MIGRATIONS
create_category_table()
create_user_table()
create_admin_table()
create_plant_table()