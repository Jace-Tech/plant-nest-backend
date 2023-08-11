from .database.user_table import create_user_table
from .database.admin_table import create_admin_table
from .database.plant_table import create_plant_table
from .database.category_table import create_category_table
from .database.notification_table import create_notification_table
from .database.feedback_table import create_feedback_table
from .database.cart_table import create_product_cart_table
from .database.wishlist_table import create_product_wishlist_table


# RUN MIGRATIONS
def run_migrations():
    create_category_table()
    create_user_table()
    create_admin_table()
    create_plant_table()