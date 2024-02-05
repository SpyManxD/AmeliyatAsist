import sqlite3

class DatabaseManager:
    """Handles database operations for the application."""

    def __init__(self, db_name):
        """
        Initializes the DatabaseManager with the given database name.
        :param db_name: Name of the database file.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes a database connection if not already connected."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

    def close(self):
        """Commits changes and safely closes the database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_query(self, query, params=None, commit=False):
        """
        Executes a given SQL query with optional parameters and commits if specified.
        :param query: SQL query string.
        :param params: Optional parameters for the query.
        :param commit: Boolean indicating if changes should be committed.
        :return: The cursor object after execution or None if execution fails.
        """
        try:
            self.connect()  # Ensure the connection is open
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if commit:
                self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def initialize_db(self):
        """Initializes the database with required tables."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS ameliyatlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT,
            hasta_adi_soyadi TEXT,
            ameliyat_tanisi TEXT,
            firma TEXT,
            teknisyen TEXT,
            malzeme_markasi TEXT,
            gerekli_malzeme TEXT,
            fatura_dosyasi TEXT
        )'''
        self.execute_query(create_table_query, commit=True)

    def insert_ameliyat(self, data):
        """Inserts a new record into the ameliyatlar table."""
        insert_query = '''
        INSERT INTO ameliyatlar (tarih, hasta_adi_soyadi, ameliyat_tanisi, firma, teknisyen, malzeme_markasi, gerekli_malzeme, fatura_dosyasi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(insert_query, data, commit=True)

    def fetch_all_ameliyatlar(self):
        """Fetches all records from the ameliyatlar table."""
        select_query = "SELECT * FROM ameliyatlar"
        cursor = self.execute_query(select_query)
        return cursor.fetchall() if cursor else []

    def initialize_db(self):
        create_table_query = '''
        ALTER TABLE ameliyatlar ADD COLUMN durum TEXT DEFAULT 'Incomplete',
        ADD COLUMN sebep TEXT,
        ADD COLUMN yeni_tarih TEXT
        '''
        self.execute_query(create_table_query, commit=True)
