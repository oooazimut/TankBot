import datetime

from db.schema import DB_NAME, CREATE_SCRIPT
from db.models import DataBase
from db.models import SqLiteDataBase

database = SqLiteDataBase(DB_NAME, CREATE_SCRIPT)


class UserRepo:
    db: DataBase = database

    @classmethod
    def get_user_by_id(cls, userid):
        query = 'SELECT * FROM users WHERE id = ?'
        return cls.db.select_query(query, [userid])

    @classmethod
    def get_users(cls):
        query = 'SELECT * FROM users'
        return cls.db.select_query(query, [])

    @classmethod
    def add_user(cls, userid, username):
        query = 'INSERT INTO users (id, username) VALUES (?, ?)'
        cls.db.post_query(query, [userid, username])


class LosRepo:
    db: DataBase = database

    @classmethod
    def write_level(cls, level):
        moment = datetime.datetime.now().replace(microsecond=0)
        query = 'INSERT INTO levels(timestamp, level) VALUES (?, ?)'
        cls.db.post_query(query, [moment, level])

    @classmethod
    def get_last_level(cls):
        query = 'SELECT * FROM levels ORDER BY id DESC LIMIT 1'
        return cls.db.select_query(query, [])

    @classmethod
    def get_first_item(cls):
        query = 'SELECT * FROM levels ORDER BY id LIMIT 1'
        return cls.db.select_query(query, [])

    @classmethod
    def get_levels(cls, date: datetime.date):
        query = 'SELECT * FROM levels WHERE DATE(timestamp) = ?'
        return cls.db.select_query(query, [date])
