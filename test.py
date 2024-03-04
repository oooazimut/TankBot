import datetime

from db.service import UserService, LosService

print(UserService.get_users())
print(LosService.get_last_level())

moment = datetime.datetime.now().replace(second=0)
print(moment)
LosService.db.post_query('delete from levels')