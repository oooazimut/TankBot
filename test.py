import asyncio

from tools.modbus import ModbusService


async def write_level():
    await ModbusService.client.connect()
    await ModbusService.write_float(516, 4)
    data = await ModbusService.read_float(516)
    print(data)

asyncio.run(write_level())
