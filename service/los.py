import datetime

from aiogram import Bot
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers import SchedulerAlreadyRunningError
from pymodbus import ModbusException, ExceptionResponse

from config import TankVars, _logger
from db.repo import LosRepo, UserRepo
from service.mailing import Mailing
from service.modbus import ModbusService


class LosService:

    @staticmethod
    def check_level(level: float, prev_level: float, bot: Bot) -> None:
        from tankbot import scheduler
        txt = ''
        match prev_level, level:
            case p, c if (TankVars.low_border <= p <= TankVars.high_border) and (
                          c < TankVars.low_border or c > TankVars.high_border):
                txt = 'Авария датчика уровня!'
            case p, c if p <= TankVars.warning < c:
                txt = 'Первый критический уровень, необходимо проверить работу насоса!'
            case p, c if p <= TankVars.critical < c:
                txt = 'Второй критический уровень, ёмкость скоро переполнится!'
            case p, c if (p < TankVars.low_border or p > TankVars.warning) and (
                        TankVars.low_border <= c <= TankVars.warning):
                try:
                    scheduler.remove_job('alarm')
                except JobLookupError:
                    pass
        if txt:
            job = scheduler.get_job('alarm')
            if job:
                job.modify(kwargs={'message': txt, 'users': UserRepo.get_users(), 'bot': bot})
            else:
                try:
                    scheduler.add_job(
                        func=Mailing.send_message,
                        trigger='interval',
                        seconds=10,
                        next_run_time=datetime.datetime.now(),
                        id='alarm',
                        kwargs={'message': txt, 'users': UserRepo.get_users(), 'bot': bot}
                    )
                    scheduler.start()
                except SchedulerAlreadyRunningError:
                    pass

    @classmethod
    async def poll_registers(cls, bot: Bot):
        await ModbusService.client.connect()
        try:
            data = await ModbusService.client.read_holding_registers(512, 3, 16)
            level = ModbusService.convert_to_float(data.registers[:2])
            prev_level = LosRepo.get_last_level()[0]['level']
            cls.check_level(level, prev_level, bot)
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
