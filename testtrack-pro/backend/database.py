import mysql.connector
from config import Config

class Database:
    """Database connection handler"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✓ Database connected successfully")
            return True
        except mysql.connector.Error as err:
            print(f"✗ Database connection error: {err}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Query error: {err}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Update error: {err}")
            return 0
    
    def get_last_insert_id(self):
        """Get last inserted ID"""
        return self.cursor.lastrowid

db = Database()
