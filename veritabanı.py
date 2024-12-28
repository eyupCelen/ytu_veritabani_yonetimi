import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox,QInputDialog
from PyQt5.QtCore import Qt
import psycopg2

# Singleton for Database Connection
class DatabaseConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection()
        return DatabaseConnection._instance

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                self.conn = psycopg2.connect(
                    dbname="craftmart",
                    user="postgres",
                    password="12345678",
                    host="localhost",
                    port="5432"
                )
                DatabaseConnection._instance = self
            except psycopg2.Error as e:
                QMessageBox.critical(None, "Database Error", f"Error connecting to the database: {e}")
                sys.exit(1)

    def get_connection(self):
        return self.conn

# Login Window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("CraftMart - Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_login(self):       
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both email and password.")
            return

        try:
            conn = DatabaseConnection.get_instance().get_connection()
            cursor = conn.cursor()

            # Check seller table
            cursor.execute(
                "SELECT seller_ssn FROM Seller WHERE mail_address = %s AND password = %s",
                (email, password)
            )
            seller = cursor.fetchone()

            if seller:
                QMessageBox.information(self, "Login Successful", "Welcome, Seller!")
                self.open_role_selection("seller", seller_ssn=seller[0])
                return

            # Check customer table
            cursor.execute(
                "SELECT customer_id FROM Customer WHERE mail_address = %s AND password = %s",
                (email, password)
            )
            customer = cursor.fetchone()

            if customer:
                QMessageBox.information(self, "Login Successful", "Welcome, Customer!")
                self.open_role_selection("customer",customer_id=customer[0])
                return

            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error querying the database: {e}")

    def open_role_selection(self, role, seller_ssn=None,customer_id=None):
        self.role_selection_window = RoleSelectionWindow(role, seller_ssn,customer_id)
        self.role_selection_window.show()
        self.close()


# Role Selection Window
class RoleSelectionWindow(QMainWindow):
    def __init__(self, role, seller_ssn=None,customer_id=None):
        super().__init__()
        self.user_role = role
        self.seller_ssn = seller_ssn
        self.customer_id=customer_id
        self.conn = DatabaseConnection.get_instance().get_connection()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("CraftMart - Select Role")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel(f"Logged in as {self.user_role.capitalize()}.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        proceed_button = QPushButton("Proceed to Dashboard")
        proceed_button.clicked.connect(self.open_main_window)
        layout.addWidget(proceed_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_main_window(self):
        self.main_window = CraftMartApp(self.user_role, self.seller_ssn,self.customer_id)
        self.main_window.show()
        self.close()

# Main Application
class CraftMartApp(QMainWindow):
    def __init__(self, user_role, seller_ssn=None, customer_id=None):
        super().__init__()
        self.user_role = user_role
        self.seller_ssn = seller_ssn  
        self.customer_id = customer_id
        self.conn = DatabaseConnection.get_instance().get_connection()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("CraftMart - Yerel El Sanatları Pazarı")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QHBoxLayout()

        # Left Panel
        left_layout = QVBoxLayout()

        self.category_selector = QComboBox()
        self.category_selector.addItem("Select Category")
        self.load_categories()
        left_layout.addWidget(QLabel("Select Category:"))
        left_layout.addWidget(self.category_selector)

        self.view_all_products_button = QPushButton("View All Products")
        self.view_all_products_button.clicked.connect(self.load_all_products)
        left_layout.addWidget(self.view_all_products_button)

        self.rating_input = QLineEdit()
        self.rating_input.setPlaceholderText("Minimum Rating")
        left_layout.addWidget(self.rating_input)

        self.get_rated_products_button = QPushButton("Get Rated Products")
        self.get_rated_products_button.clicked.connect(self.load_rated_products)
        left_layout.addWidget(self.get_rated_products_button)

        self.get_popular_products_button = QPushButton("Get Popular Products")
        self.get_popular_products_button.clicked.connect(self.load_popular_products)
        left_layout.addWidget(self.get_popular_products_button)

        self.show_reviews_button = QPushButton("Show Reviews for Selected Product")
        self.show_reviews_button.clicked.connect(self.show_reviews_for_selected_product)
        left_layout.addWidget(self.show_reviews_button)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(["Product ID", "Description", "Price", "Category"])
        left_layout.addWidget(self.product_table)

        if self.user_role == "seller":
            add_product_button = QPushButton("Add New Product")
            add_product_button.clicked.connect(self.add_product_ui)
            left_layout.addWidget(add_product_button)

            change_price_button = QPushButton("Change Product Price")
            change_price_button.clicked.connect(self.change_price_ui)
            left_layout.addWidget(change_price_button)

        if self.user_role == "customer":
            order_product_button = QPushButton("Order Product")
            order_product_button.clicked.connect(self.order_product_ui)
            left_layout.addWidget(order_product_button)

            cancel_order_button = QPushButton("Cancel Order")
            cancel_order_button.clicked.connect(self.cancel_order_ui)
            left_layout.addWidget(cancel_order_button)

        main_layout.addLayout(left_layout)

        # Right Panel
        right_layout = QVBoxLayout()

        self.review_table = QTableWidget()
        self.review_table.setColumnCount(3)
        self.review_table.setHorizontalHeaderLabels(["Product ID", "Review", "Rating"])
        right_layout.addWidget(QLabel("Product Reviews:"))
        right_layout.addWidget(self.review_table)

        

            

        main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # Database Queries
    def load_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT category_id, category_name FROM Category")
        categories = cursor.fetchall()
        self.categories_map = {}
        for category_id, category_name in categories:
            self.categories_map[category_name] = category_id
            self.category_selector.addItem(category_name)

    def load_all_products(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Category_products_view")
            products = cursor.fetchall()

            self.product_table.setRowCount(len(products))
            for row_idx, (product_id, description, price, category_name) in enumerate(products):
                self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
                self.product_table.setItem(row_idx, 1, QTableWidgetItem(description))
                self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${price:.2f}"))
                self.product_table.setItem(row_idx, 3, QTableWidgetItem(category_name))
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading products: {e}")
    def show_reviews_for_selected_product(self):
        try:
            selected_row = self.product_table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a product.")
                return

            product_id_item = self.product_table.item(selected_row, 0)
            if not product_id_item:
                QMessageBox.warning(self, "Selection Error", "Selected row does not contain valid product data.")
                return

            product_id = int(product_id_item.text())

            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT review_body, review_rating
                FROM Review
                WHERE product_id = %s
            """, (product_id,))
            reviews = cursor.fetchall()

            self.review_table.setRowCount(len(reviews))
            for row_idx, (review_body, review_rating) in enumerate(reviews):
                self.review_table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
                self.review_table.setItem(row_idx, 1, QTableWidgetItem(review_body))
                self.review_table.setItem(row_idx, 2, QTableWidgetItem(str(review_rating)))

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error retrieving reviews from the database: {e}")

    def load_rated_products(self):
        try:
            cursor = self.conn.cursor()
            category_name = self.category_selector.currentText()
            if category_name == "Select Category":
                QMessageBox.warning(self, "Input Error", "Please select a category.")
                return

            min_rating = self.rating_input.text()
            category_id = self.categories_map.get(category_name)

            if min_rating.strip():  # Check if a rating is provided
                if not min_rating.isdigit() and not min_rating.replace('.', '', 1).isdigit():
                    QMessageBox.warning(self, "Input Error", "Please enter a valid rating.")
                    return

                cursor.execute("""
                    SELECT * FROM get_rated_products(%s, %s)
                """, (float(min_rating), category_id))
            else:
                cursor.execute("""
                    SELECT * FROM get_categorized_products(%s)
                """, (category_id,))

            products = cursor.fetchall()
            self.product_table.setRowCount(len(products))
            for row_idx, (product_id, description, price, category_name) in enumerate(products):
                self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
                self.product_table.setItem(row_idx, 1, QTableWidgetItem(description))
                self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${price:.2f}"))
                self.product_table.setItem(row_idx, 3, QTableWidgetItem(category_name))

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching rated products: {e}")


    def load_popular_products(self):        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.product_id, p.product_description, p.price, c.category_name
                FROM get_most_popular_products() AS pop
                JOIN Product p ON p.product_id = pop.prod_id
                JOIN Category c ON p.category_id = c.category_id
            """)
            products = cursor.fetchall()

            self.product_table.setRowCount(len(products))
            self.product_table.setColumnCount(4)
            self.product_table.setHorizontalHeaderLabels(["Product ID", "Description", "Price", "Category"])
            for row_idx, (product_id, description, price, category_name) in enumerate(products):
                self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
                self.product_table.setItem(row_idx, 1, QTableWidgetItem(description))
                self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${price:.2f}"))
                self.product_table.setItem(row_idx, 3, QTableWidgetItem(category_name))

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching popular products: {e}")

    def load_reviews(self):
        cursor = self.conn.cursor()
        query = """
            SELECT Product.product_id, Review.review_body, Review.review_rating
            FROM Review
            JOIN Product ON Review.product_id = Product.product_id
        """
        cursor.execute(query)
        reviews = cursor.fetchall()
        self.review_table.setRowCount(len(reviews))

        for row_idx, (product_id, review_body, review_rating) in enumerate(reviews):
            self.review_table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
            self.review_table.setItem(row_idx, 1, QTableWidgetItem(review_body))
            self.review_table.setItem(row_idx, 2, QTableWidgetItem(str(review_rating)))

    # Seller-Specific Features
    def add_product_ui(self):
        add_product_window = QMainWindow(self)
        add_product_window.setWindowTitle("Add New Product")
        add_product_window.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()

        product_desc_input = QLineEdit()
        product_desc_input.setPlaceholderText("Product Description")
        layout.addWidget(product_desc_input)

        product_amount_input = QLineEdit()
        product_amount_input.setPlaceholderText("Product Amount")
        layout.addWidget(product_amount_input)

        product_price_input = QLineEdit()
        product_price_input.setPlaceholderText("Product Price")
        layout.addWidget(product_price_input)

        product_category_input = QComboBox()
        product_category_input.addItem("Select Category")
        cursor = self.conn.cursor()
        cursor.execute("SELECT category_id, category_name FROM Category")
        categories = cursor.fetchall()
        category_map = {f"{category_name}": category_id for category_id, category_name in categories}
        for category_name in category_map.keys():
            product_category_input.addItem(category_name)
        layout.addWidget(product_category_input)

        add_button = QPushButton("Add Product")
        add_button.clicked.connect(lambda: self.add_product(
            product_desc_input.text(),
            product_amount_input.text(),
            product_price_input.text(),
            product_category_input.currentText(),
            category_map
        ))
        layout.addWidget(add_button)

        container = QWidget()
        container.setLayout(layout)
        add_product_window.setCentralWidget(container)
        add_product_window.show()

    def add_product(self, description, amount, price, category_name, category_map):
        if not description or not amount or not price or category_name == "Select Category":
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            category_id = category_map[category_name]
            cursor = self.conn.cursor()

            # Determine the next product_id manually if needed
            cursor.execute("SELECT MAX(product_id) FROM Product")
            last_product_id = cursor.fetchone()[0]
            new_product_id = last_product_id + 1 if last_product_id else 1

            # Insert into Product table
            product_query = """
                INSERT INTO Product (product_id, product_description, product_amount, price, category_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(product_query, (new_product_id, description, int(amount), float(price), category_id))

            # Insert into Product_Seller table
            if not hasattr(self, 'seller_ssn') or not self.seller_ssn:
                QMessageBox.critical(self, "Error", "Seller SSN is not set. Please ensure the correct seller is logged in.")
                return

            product_seller_query = """
                INSERT INTO Product_Seller (product_id, seller_ssn)
                VALUES (%s, %s)
            """
            cursor.execute(product_seller_query, (new_product_id, self.seller_ssn))

            self.conn.commit()
            QMessageBox.information(self, "Success", f"Product added successfully with ID: {new_product_id}")
            self.load_rated_products()
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Error adding product: {e}")

    def change_price_ui(self):
        change_price_window = QMainWindow(self)
        change_price_window.setWindowTitle("Change Product Price")
        change_price_window.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        product_selector = QComboBox()
        product_selector.setPlaceholderText("Select Product")
        layout.addWidget(product_selector)

        # Load products owned by the seller into the combobox
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT Product.product_id, Product.product_description
                FROM Product
                JOIN Product_Seller ON Product.product_id = Product_Seller.product_id
                WHERE Product_Seller.seller_ssn = %s
            """, (self.seller_ssn,))
            products = cursor.fetchall()

            for product_id, description in products:
                product_selector.addItem(f"{product_id} - {description}", product_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading products: {e}")
            return

        new_price_input = QLineEdit()
        new_price_input.setPlaceholderText("New Price")
        layout.addWidget(new_price_input)

        change_button = QPushButton("Change Price")
        change_button.clicked.connect(lambda: self.change_price(
            product_selector.currentData(),  # Get product_id from combobox
            new_price_input.text()
        ))
        layout.addWidget(change_button)

        container = QWidget()
        container.setLayout(layout)
        change_price_window.setCentralWidget(container)
        change_price_window.show()

    def change_price(self, product_id, new_price):
        if not product_id or not new_price:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            cursor = self.conn.cursor()

            # Verify that the product belongs to the logged-in seller
            verify_query = """
                SELECT product_id FROM Product_Seller
                WHERE product_id = %s AND seller_ssn = %s
            """
            cursor.execute(verify_query, (product_id, self.seller_ssn))
            product = cursor.fetchone()

            if not product:
                QMessageBox.warning(self, "Authorization Error", "You can only change the price of your own products.")
                return

            # Update the price of the product
            update_query = """
                UPDATE Product
                SET price = %s
                WHERE product_id = %s
            """
            cursor.execute(update_query, (float(new_price), product_id))

            # Commit the changes
            self.conn.commit()

            # Capture PostgreSQL notices
            if self.conn.notices:
                notice_message = self.conn.notices.pop()
                QMessageBox.information(self, "Database Notice", notice_message)

            #QMessageBox.information(self, "Success", f"Price for product ID {product_id} updated to ${new_price}")
            self.load_rated_products()
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Error updating product price: {e}")

    def order_product_ui(self):
        order_window = QMainWindow(self)
        order_window.setWindowTitle("Order Product")
        order_window.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        product_selector = QComboBox()
        product_selector.setPlaceholderText("Select Product")
        layout.addWidget(product_selector)

        # Load available products into the combobox
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT product_id, product_description, price
                FROM Product
            """)
            products = cursor.fetchall()

            for product_id, description, price in products:
                product_selector.addItem(f"{product_id} - {description} - ${price:.2f}", product_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading products: {e}")
            return

        order_button = QPushButton("Place Order")
        order_button.clicked.connect(lambda: self.place_order(
            product_selector.currentData()
        ))
        layout.addWidget(order_button)

        container = QWidget()
        container.setLayout(layout)
        order_window.setCentralWidget(container)
        order_window.show()

    def place_order(self, product_id):
        if not product_id:
            QMessageBox.warning(self, "Input Error", "Please select a product.")
            return

        try:
            # Ask for the quantity to order
            quantity, ok = QInputDialog.getInt(self, "Order Quantity", "Enter the quantity to order:")
            if not ok or quantity <= 0:
                QMessageBox.warning(self, "Input Error", "Please enter a valid quantity.")
                return

            cursor = self.conn.cursor()

            # Check if the user is a customer
            if not hasattr(self, 'user_role') or self.user_role != "customer":
                QMessageBox.critical(self, "Authorization Error", "Only customers can place orders.")
                return

            # Check product stock
            cursor.execute("SELECT product_amount FROM Product WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if not product:
                QMessageBox.warning(self, "Product Error", "Selected product does not exist.")
                return

            available_amount = product[0]
            if quantity > available_amount:
                QMessageBox.warning(self, "Stock Error", f"Insufficient stock. Only {available_amount} items available.")
                return

            # Generate the next order_id
            cursor.execute("SELECT nextval('order_sequence')")
            next_order_id = cursor.fetchone()[0]

            # Ensure customer_id is set
            if not hasattr(self, 'customer_id') or not self.customer_id:
                QMessageBox.critical(self, "Error", "Customer information is missing.")
                return

            # Insert into Order_ table
            order_query = """
                INSERT INTO Order_ (order_id, order_time, customer_id)
                VALUES (%s, NOW(), %s)
            """
            cursor.execute(order_query, (next_order_id, self.customer_id))

            # Insert into Order_Product table
            order_product_query = """
                INSERT INTO Order_Product (order_id, product_id, order_amount)
                VALUES (%s, %s, %s)
            """
            cursor.execute(order_product_query, (next_order_id, product_id, quantity))

            # Update product amount
            update_product_query = """
                UPDATE Product
                SET product_amount = product_amount - %s
                WHERE product_id = %s
            """
            cursor.execute(update_product_query, (quantity, product_id))

            self.conn.commit()
            QMessageBox.information(self, "Success", f"Order placed successfully with Order ID: {next_order_id}")
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Error placing order: {e}")
    def cancel_order_ui(self):
        if self.user_role != "customer":
            QMessageBox.critical(self, "Authorization Error", "Only customers can cancel orders.")
            return

        cancel_window = QMainWindow(self)
        cancel_window.setWindowTitle("Cancel Order")
        cancel_window.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        order_selector = QComboBox()
        order_selector.setPlaceholderText("Select Order to Cancel")
        layout.addWidget(order_selector)

        try:
            cursor = self.conn.cursor()
            # Load orders for the logged-in customer
            cursor.execute("""
                SELECT order_id, order_time
                FROM Order_
                WHERE customer_id = %s
            """, (self.customer_id,))
            orders = cursor.fetchall()

            for order_id, order_time in orders:
                order_selector.addItem(f"Order ID: {order_id}, Time: {order_time}", order_id)
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading orders: {e}")
            return

        cancel_button = QPushButton("Cancel Order")
        cancel_button.clicked.connect(lambda: self.cancel_order(order_selector.currentData()))
        layout.addWidget(cancel_button)

        container = QWidget()
        container.setLayout(layout)
        cancel_window.setCentralWidget(container)
        cancel_window.show()
    
    def cancel_order(self, order_id):
        if not order_id:
            QMessageBox.warning(self, "Input Error", "Please select an order to cancel.")
            return

        try:
            cursor = self.conn.cursor()

            # Delete the order and cascade deletions to Order_Product
            delete_order_query = "DELETE FROM Order_ WHERE order_id = %s RETURNING order_id"
            cursor.execute(delete_order_query, (order_id,))
            deleted_order = cursor.fetchone()

            if deleted_order:
                self.conn.commit()
                #QMessageBox.information(self, "Success", f"Order with ID {deleted_order[0]} has been canceled.")
                
                # Capture PostgreSQL trigger notices
                if self.conn.notices:
                    notice_message = self.conn.notices.pop()
                    QMessageBox.information(self, "Database Notice", notice_message)
            else:
                QMessageBox.warning(self, "Order Error", "Failed to cancel the order. Please try again.")

        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Error canceling order: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
