import datetime

from db.schema import DB_NAME, CREATE_SCRIPT
from db.models import DataBase
from db.models import SqLiteDataBase

database = SqLiteDataBase(DB_NAME, CREATE_SCRIPT)


class UserService:
    db: DataBase = database

    @classmethod
    def get_user_by_id(cls, userid):
        query = 'SELECT * FROM users WHERE id = ?'
        return cls.db.select_query(query, [userid])


class LosService:
    db: DataBase = database

    @classmethod
    def write_level(cls, level):
        moment = datetime.datetime.now().replace(microsecond=0)
        query = 'INSERT INTO levels(timestamp, level) VALUES (?, ?)'
        cls.db.post_query(query, [moment, level])
