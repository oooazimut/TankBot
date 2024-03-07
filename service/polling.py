import asyncio

from aiogram import Bot
from pymodbus.exceptions import ConnectionException, ModbusIOException

from config import _logger
from db.repo import LosRepo, UserRepo
from service.los import LosService
from service.mailing import Mailing
from service.modbus import ModbusService as MbSrv


class Polling:
    @staticmethod
    def pr_connector(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(3)
            _logger.info('### Коннектимся к ПР...')
            while True:
                await MbSrv.client.connect()
                if MbSrv.client.connected:
                    _logger.info('### ПР на связи.')
                    await func(*args, **kwargs)
                MbSrv.client.close()
                await asyncio.sleep(15)

        return wrapper

    @staticmethod
    @pr_connector
    async def regs_polling(bot: Bot):
        while True:
            try:
                data = await MbSrv.client.read_holding_registers(512, 3, 16)
                if not data.isError():
                    level = MbSrv.convert_to_float(data.registers[:2])
                    notification = LosService.check_level(level)
                    if notification:
                        await Mailing.send_message(notification, UserRepo.get_users(), bot)
                    LosRepo.write_level(level)
                else:
                    _logger.error(f'Ошибка чтения: {data}')
            except ModbusIOException:
                _logger.error('Нет ответа от ПР')
                MbSrv.client.close()
                break
            except ConnectionException:
                _logger.error('Ошибка соединения')
                MbSrv.client.close()
                break

            await asyncio.sleep(15)


if __name__ == '__main__':
    asyncio.run(Polling.regs_polling())
