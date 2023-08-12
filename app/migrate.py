from .database.user_table import create_user_table
from .database.admin_table import create_admin_table
from .database.plant_table import create_plant_table
from .database.category_table import create_category_table
from .database.notification_table import create_notification_table
from .database.feedback_table import create_feedback_table
from .database.cart_table import create_product_cart_table
from .database.wishlist_table import create_product_wishlist_table
from .database.accessory_table import create_accessory_table
from .database.cart_table import create_product_cart_table
from .database.order_table import create_orders_table
from .database.wishlist_table import create_product_wishlist_table


# RUN MIGRATIONS
def run_migrations():
    create_user_table()
    create_admin_table()
    create_plant_table()
    create_notification_table()
    create_accessory_table()
    create_product_cart_table()
    create_orders_table()
    create_product_wishlist_table()
    create_feedback_table()