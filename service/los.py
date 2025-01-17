import datetime
from enum import StrEnum

from aiogram import Bot
from apscheduler.executors.base import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymodbus import ModbusException, ExceptionResponse

from config import settings 
from db.repo import LosRepo, UserRepo
from service.mailing import send_message
from service.modbus import ModbusService

logger = logging.getLogger(__name__)

class Messages(StrEnum):
    SENSOR_FAILURE = 'Авария датчика уровня!'
    FIRST_CRIT_LEVEL = 'Первый критический уровень, необходимо проверить работу насоса!'
    SECOND_CRIT_LEVEL = 'Второй критический уровень, ёмкость скоро переполнится!'
    CURR_SENSOR_FAILURE = 'Авария датчика тока!'
    HIGH_CURRENT_FAILURE = 'Превышение рабочего тока!'
    POSSIBLY_LACK_OF_POWER = 'Возможно, насос неисправен или на него не подается питание, превышение уровня воды включения насоса!'
    POSSIBLY_DEFECTIVE_PUMP = 'Неисправен насос или засорение водопровода - уровень жидкости не падает при работе насоса!'



def is_warning(level) -> bool:
    return settings.tank.warning < level <= settings.tank.critical

def is_critical(level) -> bool:
    return settings.tank.critical < level <= settings.tank.high_border

def is_failure(level) -> bool:
    return any([level < settings.tank.low_border, level > settings.tank.high_border])

def is_normal(level) -> bool:
    return settings.tank.low_border <= level <= settings.tank.warning

async def check_alarm(bot: Bot, scheduler: AsyncIOScheduler):
    level = LosRepo.get_last_level()
    txt = ''
    match level:
        case l if is_failure(l):
            txt = Messages.SENSOR_FAILURE
        case l if is_warning(l):
            txt = Messages.FIRST_CRIT_LEVEL
        case l if is_critical(l):
            txt = Messages.SECOND_CRIT_LEVEL

    if txt:
        users = UserRepo.get_users()
        await send_message(txt, users, bot) 

def check_level(level: float, prev_level: float, bot: Bot, scheduler: AsyncIOScheduler) -> None:
    txt = ''
    match prev_level, level:
        case p, c if not is_failure(p) and is_failure(c):
            txt = Messages.SENSOR_FAILURE
        case p, c if not is_warning(p) and is_warning(c):
            txt = Messages.FIRST_CRIT_LEVEL
        case p, c if not is_critical(p) and is_critical(c):
            txt = Messages.SECOND_CRIT_LEVEL
    if txt:
        job = scheduler.get_job('alarm')
        if job:
            job.modify(
                next_run_time=datetime.datetime.now(),
                kwargs={'message': txt, 'users': UserRepo.get_users(), 'bot': bot}
            )
        else:
            scheduler.add_job(
                func=Mailing.send_message,
                trigger='interval',
                hours=1,
                next_run_time=datetime.datetime.now(),
                id='alarm',
                kwargs={'message': txt, 'users': UserRepo.get_users(), 'bot': bot}
            )


async def poll_registers(cls, bot: Bot, scheduler: AsyncIOScheduler):
    def dc_accident_notification(data: int):
        match data:
            case 1:
                text = 
        
    await ModbusService.client.connect()
    try:
        data = await ModbusService.client.read_holding_registers(512, 3, 16)
        level = ModbusService.convert_to_float(data.registers[:2])
        prev_level = LosRepo.get_last_level()[0]['level']
        cls.check_level(level, prev_level, bot, scheduler)
        LosRepo.write_level(level)

        match data.registers[-1]:
            case 1:
                pass
            case 2: 
                pass
    except ModbusException as exc:
        logger.error(f'1 {exc}')
        ModbusService.client.close()
        return
    if data.isError():
        logger.error(data)
        ModbusService.client.close()
        return
    if isinstance(data, ExceptionResponse):
        logger.error(f' 2 {data}')
        ModbusService.client.close()
    ModbusService.client.close()
