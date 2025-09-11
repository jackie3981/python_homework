import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/lesson.db")

def get_total_prices(conn):
    """ Fetch total prices for the first 5 orders. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.order_id, 
            SUM(p.price * li.quantity) AS total_price
        FROM orders o
        INNER JOIN line_items li ON o.order_id = li.order_id
        INNER JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5;
    """)
    return cursor.fetchall()

def average_customer_price(conn):
    """ Fetch average total price per customer. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.customer_name,
            AVG(sq.total_price) AS average_total_price
        FROM customers c
        LEFT JOIN (
            SELECT 
                o.customer_id AS customer_id_b,
                SUM(p.price * li.quantity) AS total_price
            FROM orders o
            INNER JOIN line_items li ON o.order_id = li.order_id
            INNER JOIN products p ON li.product_id = p.product_id
            GROUP BY o.order_id, o.customer_id
        ) sq ON c.customer_id = sq.customer_id_b
        GROUP BY c.customer_id, c.customer_name;
    """)
    return cursor.fetchall()

def get_customer_id(conn, customer_name):
    """ Fetch customer ID by customer name. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id FROM customers WHERE customer_name = ?;
    """, (customer_name,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Customer '{customer_name}' not found")
    return result[0] if result else None

def get_employee_id(conn, first_name, last_name):
    """ Fetch employee ID by employee name. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?;
    """, (first_name, last_name))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Employee '{first_name} {last_name}' not found")
    return result[0] if result else None

def get_least_expensive(conn):
    """ Returns up to 5 least expensive products. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id FROM products
        ORDER BY price ASC
        LIMIT 5;
    """)
    result = cursor.fetchall()
    if not result:
        raise ValueError("No products found")
    return result

def insert_order(conn, customer_id, employee_id):
    """ Insert a new order with line items. """
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, date)
            VALUES (?, ?, DATE('now'))
            RETURNING order_id;
        """, (customer_id, employee_id))
    order_id = cursor.fetchone()[0]

    least_expensive_products = get_least_expensive(conn)

    for product in least_expensive_products:
        product_id = product[0]
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, 10);
        """, (order_id, product_id))   

    return order_id

def print_order_summary(conn, order_id):
    """ Print a summary of the order. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            o.order_id,
            c.customer_name,
            e.first_name || ' ' || e.last_name AS employee_name,
            o.date,
            SUM(p.price * li.quantity) AS total_price
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.customer_id
        INNER JOIN employees e ON o.employee_id = e.employee_id
        INNER JOIN line_items li ON o.order_id = li.order_id
        INNER JOIN products p ON li.product_id = p.product_id
        WHERE o.order_id = ?
        GROUP BY o.order_id, c.customer_name, e.first_name, e.last_name, o.date;
    """, (order_id,))
    result = cursor.fetchone()
    if result:
        print(f"Order Summary for Order ID {order_id}:")
        print(f"Customer: {result[1]}")
        print(f"Employee: {result[2]}")
        print(f"Order Date: {result[3]}")
        print(f"Total Price: ${result[4]:.2f}")
    else:
        print(f"No summary found for Order ID {order_id}")

def insert_order_unique(conn, customer_name, employee_first, employee_last):
    """Insert a new order only if it doesn't exist today."""
    cursor = conn.cursor()
    
    # Get IDs
    customer_id = get_customer_id(conn, customer_name)
    employee_id = get_employee_id(conn, employee_first, employee_last)

    # Check if an order already exists today for this customer and employee
    cursor.execute("""
        SELECT order_id
        FROM orders
        WHERE customer_id = ? AND employee_id = ? AND date = DATE('now')
        LIMIT 1;
    """, (customer_id, employee_id))
    
    row = cursor.fetchone()
    if row:
        print(f"Order already exists today with order_id {row[0]}. No new order created.")
        return row[0]  # Return existing order_id

    # If not exists, create new order
    order_id = insert_order(conn, customer_id, employee_id)
    print(f"New order created with order_id {order_id}")
    return order_id

def employee_orders(conn):
    """ Fetch all orders for a specific employee. """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.employee_id,
            e.first_name,
            e.last_name,
            COUNT(o.order_id) AS order_count
        FROM employees e 
        INNER JOIN orders o ON o.employee_id = e.employee_id 
        GROUP BY e.employee_id, e.first_name, e.last_name 
        HAVING COUNT(o.order_id) > 5
    """)
    return cursor.fetchall()


try:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1");

        ## Task 1: Complex JOINs with Aggregation
        for order_id, total_price in get_total_prices(conn):
            print(f"Order {order_id}: ${total_price:.2f}")

        ## Task 2: Understanding Subqueries
        for customer_name, avg_price in average_customer_price(conn):
            if avg_price is None:
                print(f"Customer {customer_name}: No orders yet")
            else:
                print(f"Customer {customer_name}: ${avg_price:.2f}")

        ## Task 3: An Insert Transaction Based on Data
        order_id = insert_order_unique(conn, "Perez and Sons", "Miranda", "Harris")
        print_order_summary(conn, order_id)

        # Aggregation with HAVING
        employee_data = employee_orders(conn)

        if not employee_data:
            print("No employees have more than 5 orders.")
        else:
            for emp_id, first_name, last_name, order_count in employee_data:
                print(f"Employee {first_name} {last_name} (ID: {emp_id}) has {order_count} orders.")

        conn.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")