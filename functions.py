import asyncio

from pymodbus.exceptions import ConnectionException, ModbusIOException

from config import _logger
from db.service import LosService
from tools.modbus import ModbusService as MbSrv


def pr_connector(func):
    async def wrapper():
        await asyncio.sleep(3)
        _logger.info('### Коннектимся к ПР...')
        while True:
            await MbSrv.client.connect()
            if MbSrv.client.connected:
                _logger.info('### ПР на связи.')
                await func()
            MbSrv.client.close()
            await asyncio.sleep(15)

    return wrapper


@pr_connector
async def regs_polling():
    while True:
        try:
            data = await MbSrv.client.read_holding_registers(512, 3, 16)
            if not data.isError():
                level = MbSrv.convert_to_float(data.registers[:2])
                LosService.write_level(level)
                bits = bin(data.registers[2])[2:].zfill(2)
                print(bits, type(bits))
                overflow, failure = bits[1], bits[0]
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
    asyncio.run(regs_polling())
