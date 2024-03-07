from config import TankVars
from db.repo import LosRepo


class LosService:
    @staticmethod
    def check_level(level: float) -> str | None:
        prev_level = LosRepo.get_last_level()[0]['level']
        if not (4 <= prev_level < TankVars.warning):
            return
        if 20 < level < 4:
            return 'Авария датчика уровня!'
        elif level > TankVars.critical:
            return 'Второй критический уровень, ёмкость скоро переполнится!'
        elif level > TankVars.warning:
            return 'Первый критический уровень, необходимо проверить работу насоса!'
        return
