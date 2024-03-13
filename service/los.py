import datetime
from dataclasses import dataclass

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymodbus import ModbusException, ExceptionResponse

from config import TankVars, _logger
from db.repo import LosRepo, UserRepo
from service.mailing import Mailing
from service.modbus import ModbusService


@dataclass
class Messages:
    SENSOR_FAILURE = 'Авария датчика уровня!'
    FIRST_CRIT_LEVEL = 'Первый критический уровень, необходимо проверить работу насоса!'
    SECOND_CRIT_LEVEL = 'Второй критический уровень, ёмкость скоро переполнится!'


class LosService:
    @staticmethod
    def is_warning(level) -> bool:
        return TankVars.warning < level <= TankVars.critical

    @staticmethod
    def is_critical(level) -> bool:
        return TankVars.critical < level <= TankVars.high_border

    @staticmethod
    def is_failure(level) -> bool:
        return any([level < TankVars.low_border, level > TankVars.high_border])

    @staticmethod
    def is_normal(level) -> bool:
        return TankVars.low_border <= level <= TankVars.warning

    @classmethod
    def check_alarm(cls, bot: Bot, scheduler: AsyncIOScheduler):
        job = scheduler.get_job('alarm')
        if not job:
            level = LosRepo.get_last_level()
            txt = ''
            match level:
                case l if cls.is_failure(l):
                    txt = Messages.SENSOR_FAILURE
                case l if cls.is_warning(l):
                    txt = Messages.FIRST_CRIT_LEVEL
                case l if cls.is_critical(l):
                    txt = Messages.SECOND_CRIT_LEVEL

            if txt:
                scheduler.add_job(
                    func=Mailing.send_message,
                    trigger='interval',
                    hours=1,
                    next_run_time=datetime.datetime.now(),
                    id='alarm',
                    kwargs={'message': txt, 'users': UserRepo.get_users(), 'bot': bot}
                )

    @classmethod
    def check_level(cls, level: float, prev_level: float, bot: Bot, scheduler: AsyncIOScheduler) -> None:
        txt = ''
        match prev_level, level:
            case p, c if not cls.is_failure(p) and cls.is_failure(c):
                txt = Messages.SENSOR_FAILURE
            case p, c if not cls.is_warning(p) and cls.is_warning(c):
                txt = Messages.FIRST_CRIT_LEVEL
            case p, c if not cls.is_critical(p) and cls.is_critical(c):
                txt = Messages.SECOND_CRIT_LEVEL
            case p, c if not cls.is_normal(p) and cls.is_normal(c):
                job = scheduler.get_job('alarm')
                if job:
                    job.remove()
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

    @classmethod
    async def poll_registers(cls, bot: Bot, scheduler: AsyncIOScheduler):
        await ModbusService.client.connect()
        try:
            data = await ModbusService.client.read_holding_registers(512, 3, 16)
            level = ModbusService.convert_to_float(data.registers[:2])
            prev_level = LosRepo.get_last_level()[0]['level']
            cls.check_level(level, prev_level, bot, scheduler)
            LosRepo.write_level(level)
        except ModbusException as exc:
            _logger.error(f'1 {exc}')
            ModbusService.client.close()
            return
        if data.isError():
            _logger.error(data)
            ModbusService.client.close()
            return
        if isinstance(data, ExceptionResponse):
            _logger.error(f' 2 {data}')
            ModbusService.client.close()
        ModbusService.client.close()
