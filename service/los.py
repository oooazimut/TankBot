import datetime

from aiogram import Bot
from pymodbus import ModbusException, ExceptionResponse

from config import TankVars, _logger
from db.repo import LosRepo, UserRepo
from service.mailing import Mailing
from service.modbus import ModbusService


class LosService:

    @staticmethod
    def check_level(level: float) -> str | None:
        from tankbot import scheduler
        prev_level = LosRepo.get_last_level()[0]['level']
        print(level, prev_level)
        if not (4 <= prev_level < TankVars.warning):
            if 4 <= level < TankVars.warning:
                scheduler.remove_job('informer')
                print('рассылка отключена')
            return
        if 20 < level < 4:
            return 'Авария датчика уровня!'
        elif level > TankVars.critical:
            return 'Второй критический уровень, ёмкость скоро переполнится!'
        elif level > TankVars.warning:
            return 'Первый критический уровень, необходимо проверить работу насоса!'

        return

    @classmethod
    async def poll_registers(cls, bot: Bot):
        from tankbot import scheduler
        await ModbusService.client.connect()
        try:
            data = await ModbusService.client.read_holding_registers(512, 3, 16)
            level = ModbusService.convert_to_float(data.registers[:2])
            notification = cls.check_level(level)
            print(notification)
            if notification:
                print(notification)
                scheduler.add_job(
                    func=Mailing.send_message,
                    trigger='interval',
                    seconds=10,
                    next_run_time=datetime.datetime.now(),
                    id='informer',
                    kwargs={'message': notification, 'users': UserRepo.get_users(), 'bot': bot})
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
