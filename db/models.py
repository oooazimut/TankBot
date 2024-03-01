from abc import ABC, abstractmethod
import sqlite3 as sq



class DataBase(ABC):
    @abstractmethod
    def select_query(self, query, params):
        pass

    @abstractmethod
    def post_query(self, query, params):
        pass


class SqLiteDataBase(DataBase):
    def __init__(self, name, create_script):
        self.name = name
        with sq.connect(self.name) as con:
            con.executescript(create_script)

    def select_query(self, query, params=None) -> list[dict]:
        if params is None:
            params = []
        with sq.connect(self.name, detect_types=sq.PARSE_COLNAMES | sq.PARSE_DECLTYPES) as con:
            con.row_factory = sq.Row
            temp = con.execute(query, params).fetchall()
            result = []
            if temp:
                for i in temp:
                    item = dict(zip(i.keys(), tuple(i)))
                    result.append(item)
            return result

    def post_query(self, query: str, params=None) -> None:
        if params is None:
            params = []
        with sq.connect(self.name, detect_types=sq.PARSE_COLNAMES | sq.PARSE_DECLTYPES) as con:
            con.execute(query, params)
            con.commit()
