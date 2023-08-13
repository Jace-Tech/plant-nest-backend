from flask import Blueprint, render_template, flash, redirect, current_app
from ..database import get_connection
from ..database.order_table import get_all_orders, get_order_by_id
from ..database.user_table import get_one_user
from ..utils.errors import CustomError
from ..utils.mailer import send_mail
from ..utils.decorators import admin_required
from datetime import datetime
from ..utils.variables import APP_LOGO

order = Blueprint("order", __name__)

@order.get("/")
@admin_required
def view_plant_page():
    all_order = None
    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        all_order = get_all_orders()
    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return render_template("orders.html", orders=all_order)


@order.get("/delete/<id>")
def delete_order(id):
    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        conn, cursor = db

        # DELETE ORDER 
        sql = "DELETE FROM orders WHERE order_id = %s"
        cursor.execute(sql, [id]) 
        conn.commit()

        flash("Order deleted!", "success")
    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return redirect("/order")


@order.get("/approve/<id>")
def approve_order(id):
    try:
        db = get_connection()
        if not db: raise CustomError("Failed to connect to database")
        conn, cursor = db

        # GET ORDER
        order = get_order_by_id(id)
        if not order: raise CustomError("Order not found")

        # GET USER
        user = get_one_user(order.get('user_id'))

        # UPDATE ORDER 
        sql = "UPDATE orders SET status = 'delivered' WHERE order_id = %s"
        cursor.execute(sql, [id])
        conn.commit()

        # NOTIFY USER
        message = render_template("email/order-approved.html", 
            APP_LOGO=APP_LOGO,
            year=datetime.now().strftime("%Y"),
            order_id=id
        )
        send_mail(current_app, "Order Status", [user.get('email')], message, True)

        flash("Order status updated!", "success")
    except CustomError as e: 
        flash(e.message, category=e.category)

    except Exception as e:
        flash(str(e), category="error")

    finally:
        return redirect("/order")