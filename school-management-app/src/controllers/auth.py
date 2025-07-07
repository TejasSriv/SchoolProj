import mysql.connector
import bcrypt
from .db import get_connection

class AuthManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def _get_db_connection(self):
        return get_connection()
    
    def create_admin_table_if_not_exists(self):
        try:
            self.conn = self._get_db_connection()
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """)
            self.conn.commit()
            print("Admin table checked/created successfully.")

            self.cursor.execute("SELECT COUNT(*) FROM admin")
            if self.cursor.fetchone()[0] == 0:
                print("No admin users found. Adding a default admin user.")
                default_username = "admin"
                default_password = "admin123"

                hashed_password = self.hash_password(default_password)

                self.cursor.execute(
                    "INSERT INTO admin (username, password) VALUES (%s, %s)",
                    (default_username, hashed_password)
                )
                self.conn.commit()
                print(f"Default admin user '{default_username}' created with password 'password123'. Please change this in production!")

        except mysql.connector.Error as err:
            print(f"Error creating admin table or adding default admin: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, username, password):
        user = None
        try:
            self.conn = self._get_db_connection()
            self.cursor = self.conn.cursor(dictionary=True) # Use dictionary=True for easier column access
            self.cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
            user = self.cursor.fetchone()

            if user and self.check_password(password, user['password']):
                return True # Authentication successful
            else:
                return False # Authentication failed

        except mysql.connector.Error as err:
            print(f"Authentication error: {err}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def change_admin_password(self, username, new_password):
        try:
            self.conn = self._get_db_connection()
            self.cursor = self.conn.cursor()
            
            hashed_new_password = self.hash_password(new_password)
            self.cursor.execute(
                "UPDATE admin SET password = %s WHERE username = %s",
                (hashed_new_password, username)
            )
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Password for {username} changed successfully.")
                return True
            else:
                print(f"User {username} not found or password not changed.")
                return False
        except mysql.connector.Error as err:
            print(f"Error changing password: {err}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()