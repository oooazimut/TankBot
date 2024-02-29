from db.models import DataBase


class UserService:
    def __init__(self, database: DataBase):
        self.db = database

    def get_user_by_id(self, userid):
        query = 'SELECT * FROM users WHERE id = ?'
        return self.db.select_query(query, [userid])
