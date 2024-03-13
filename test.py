import asyncio

from service.modbus import ModbusService


async def test():
    await ModbusService.client.connect()
    await ModbusService.write_float(515, 40)
    ModbusService.client.close()


if __name__ == '__main__':
    asyncio.run(test())
