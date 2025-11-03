class PostgresDB:
    def load_query(self, filename):
        with open(f'sql/{filename}', 'r') as file:
            return file.read()
        
    def execute_query(self, filename, params=None):
        query = self.load_query(filename)
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            self.conn.commit()

    def execute_bulk_insert(self, filename, data: list):
        query = self.load_query(filename)
        try:
            with self.conn.cursor() as cur:
                cur.executemany(query, data)
                self.conn.commit()
        except Exception as e:
            print(f"Exception {e}")

