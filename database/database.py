import psycopg2
from settings import Settings
from .Queries import Queries
from datetime import datetime

settings = Settings()


class Database:

    def __init__(self):
        self.host = settings.postgresql_host
        self.port = settings.postgresql_connection_port
        self.databaseName = settings.postgresql_database_name
        self.user = settings.postgresql_username
        self.password = settings.postgresql_password

        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.databaseName,
                user=self.user,
                password=self.password
            )

            self.cursor = self.connection.cursor()
            print("Connected to Database!.")  # TODO: Change this to debugger!

        except psycopg2.Error as e:
            print(f"Error connecting to DB: {e}")  # TODO: Change this to debugger!

    def init_tokens_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS token_table (
            token UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE, 
        expiration_time TIMESTAMP NOT NULL
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.databaseName,
                user=self.user,
                password=self.password
            )
            try:
                self.cursor.execute(Queries.create_table_query)
                self.connection.commit()
            except psycopg2.Error as e:
                print(f"Error creating table 'token_table', {e}")  # TODO: Change to debugger!

            self.cursor = self.connection.cursor()
            print("Connected.")  # TODO: Change this to debugger!

        except psycopg2.Error as e:
            print(f"Error connecting to DB: {e}")  # TODO: Change this to debugger!

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from DB.")  # TODO: Change this to debugger!
        else:
            print("Error while disconnecting from DB.")  # TODO: Change this to debugger!

    def list_tokens(self):  # TODO: This is for DEBUG purposes only. remove in release.
        select_query = """
                    SELECT * FROM token_table
                """

        # Execute the query
        self.cursor.execute(select_query)

        # Fetch all rows from the result set
        rows = self.cursor.fetchall()

        # Print the rows
        return rows

    def store_token(self, token_uuid):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_token_query = "INSERT INTO token_table (token, expiration_time) VALUES (%s, %s);"
        self.cursor.execute(insert_token_query, (token_uuid, current_time))
        self.connection.commit()

    def get_token_timestamp(self, token_uuid: str):
        select_query = """
                    SELECT expiration_time FROM token_table WHERE token = %s
                       """
        self.cursor.execute(select_query, (token_uuid,))

        row = self.cursor.fetchone()[0]
        return row if row else "0"
