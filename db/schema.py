DB_NAME = 'tankctrl.db'

CREATE_SCRIPT = '''
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
    );
CREATE TABLE IF NOT EXISTS levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp timestamp,
    level REAL
    );
'''