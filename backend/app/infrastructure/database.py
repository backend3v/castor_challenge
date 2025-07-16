import pymysql
from pymysql.cursors import DictCursor
from ..config import Config

class DatabaseConnection:
    def __init__(self):
        self.config = Config()
    
    def get_connection(self):
        """Create and return a database connection"""
        try:
            # Validate that all required config values are present
            if not all([self.config.DB_HOST, self.config.DB_PORT, 
                       self.config.DB_USER, self.config.DB_PASSWORD, 
                       self.config.DB_NAME]):
                raise Exception("Missing database configuration values")
            
            # Type assertions to satisfy the linter
            host = str(self.config.DB_HOST)
            port = int(str(self.config.DB_PORT))
            user = str(self.config.DB_USER)
            password = str(self.config.DB_PASSWORD)
            database = str(self.config.DB_NAME)
            
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=DictCursor,
                charset='utf8mb4'
            )
            return connection
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    def test_connection(self):
        """Test the database connection"""
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
            connection.close()
            return {"status": "success", "message": "Database connection successful", "data": result}
        except Exception as e:
            return {"status": "error", "message": f"Database connection failed: {str(e)}"} 