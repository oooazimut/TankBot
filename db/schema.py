import sqlite3 as sq

DB_NAME = 'tankctrl.db'

CREATE_SCRIPT = '''
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
    );
'''