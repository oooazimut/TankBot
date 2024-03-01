import asyncio

from pymodbus.exceptions import ConnectionException, ModbusIOException

from config import _logger
from tools.modbus import ModbusService as MbSrv
from db.service import LosService


def pr_connector(func):
    async def wrapper():
        await asyncio.sleep(3)
        _logger.info('### Коннектимся к ПР...')
        while True:
            await MbSrv.client.connect()
            if MbSrv.client.connected:
                _logger.info('### ПР на связи.')
                await func()
            await asyncio.sleep(15)

    return wrapper


@pr_connector
async def regs_polling():
    while True:
        try:
            data = await MbSrv.read_float(516)
            if isinstance(data, float):
                LosService.write_level(data)
            else:
                _logger.error(f'Ошибка чтения: {data}')
        except ConnectionException:
            _logger.error('Ошибка соединения')
            break
        except ModbusIOException:
            _logger.error('Нет ответа от ПР')

        await asyncio.sleep(15)


if __name__ == '__main__':
    asyncio.run(regs_polling())
