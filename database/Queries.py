from dataclasses import dataclass


@dataclass
class Queries:  # TODO: Probably won't need this.
    create_table_query: str

    def __init__(self):
        self.create_table_query = '''
        CREATE TABLE token_table (
            token UUID DEFAULT gen_random_uuid() NOT NULL UNIQUE,
            expiration_time TIMESTAMP NOT NULL
        );
        '''
