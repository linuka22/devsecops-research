from app.database import get_db

class User:
    @staticmethod
    def create(username, password, email, role="customer"):
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            (username, password, email, role)
        )
        db.commit()
        db.close()

    @staticmethod
    def find_by_username(username):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()
        return user

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        db.close()
        return user

class Product:
    @staticmethod
    def get_all():
        db = get_db()
        products = db.execute("SELECT * FROM products").fetchall()
        db.close()
        return products

    @staticmethod
    def get_by_id(product_id):
        db = get_db()
        product = db.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        db.close()
        return product

    @staticmethod
    def create(name, description, price, stock, category):
        db = get_db()
        db.execute(
            "INSERT INTO products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)",
            (name, description, price, stock, category)
        )
        db.commit()
        db.close()

    @staticmethod
    def search(query):
        db = get_db()
        # VULNERABILITY: SQL injection via string formatting
        results = db.execute(
            f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        ).fetchall()
        db.close()
        return results

class Order:
    @staticmethod
    def create(user_id, product_id, quantity, total_price):
        db = get_db()
        db.execute(
            "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)",
            (user_id, product_id, quantity, total_price)
        )
        db.commit()
        db.close()

    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        orders = db.execute(
            "SELECT * FROM orders WHERE user_id = ?", (user_id,)
        ).fetchall()
        db.close()
        return orders

    @staticmethod
    def get_all():
        db = get_db()
        orders = db.execute("SELECT * FROM orders").fetchall()
        db.close()
        return orders