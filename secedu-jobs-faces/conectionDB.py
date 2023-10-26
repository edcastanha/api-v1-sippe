import os
import psycopg2
from loggingMe import logger

class DatabaseConnection:
    def __init__(self, db_url=None, db_user=None, db_pass=None, db_name=None, db_port=None):
        self.db_url = db_url or os.environ.get('DATABASE_URL', 'postgres-server')
        self.db_user = db_user or os.environ.get('DATABASE_USER', 'postgres')
        self.db_pass = db_pass or os.environ.get('DATABASE_PASS', 'secedu123')
        self.db_name = db_name or os.environ.get('DATABASE_NAME', 'secedu')
        self.db_port = db_port or os.environ.get('DATABASE_PORT', '5432')
        self.conn = None
        self.cursor = None

    def connect(self):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_pass,
            host=self.db_url,
            port=self.db_port
        )
        self.cursor = self.conn.cursor()

    def update(self, query, params=None):
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            logger.info(f"<*_ConnectionDB_*> Connection e Commit - OK: {query}")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error executing update query: {e}")
            return False

    def insert(self, query, params=None):
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            logger.info(f"<*_ConnectionDB_*> Connection e Commit - OK: {query}")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            logger.error(f"Error executing insert query: {e}")
            return False

    def close(self):
        logger.info(f"<*_ConnectionDB_*> Close Connection DB")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def is_connected(self):
        return self.conn is not None
