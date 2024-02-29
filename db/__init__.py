from db.service import UserService
from db.models import SqLiteDataBase
from db.schema import DB_NAME, CREATE_SCRIPT

db = SqLiteDataBase(name=DB_NAME, create_script=CREATE_SCRIPT)
user_service = UserService(db)
