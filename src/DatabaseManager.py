import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self, dbname, user, password, host='localhost', port=5433):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    def fetch_all(self, table):
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table};")
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return columns, rows
        except Exception as e:
            print(f"Fetch failed: {e}")
            return [], []
    def close(self):
        if self.conn:
            self.conn.close()

