import asyncio

from tools.modbus import ModbusService


async def test():
    await ModbusService.client.connect()
    data = await ModbusService.client.read_holding_registers(512, 3, 16)
    if not data.isError():
        print(data.registers[:2])


asyncio.run(test())
