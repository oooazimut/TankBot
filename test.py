from enum import StrEnum


class Alarms(StrEnum):
    SENSOR_FAILURE = "Авария датчика уровня!"
    FIRST_CRIT_LEVEL = "Первый критический уровень, необходимо проверить работу насоса!"
    SECOND_CRIT_LEVEL = "Второй критический уровень, ёмкость скоро переполнится!"
    CURR_SENSOR_FAILURE = "Авария датчика тока!"
    HIGH_CURRENT_FAILURE = "Превышение рабочего тока, проверьте насос!"
    POSSIBLY_LACK_OF_POWER = "Возможно, насос неисправен или на него не подается питание, превышение уровня воды включения насоса!"
    POSSIBLY_DEFECTIVE_PUMP = "Неисправен насос или засорение водопровода - уровень жидкости не падает при работе насоса!"

ALARMS = Alarms

