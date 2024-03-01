import asyncio

from tools.modbus import ModbusService as Mbs


async def main():
    await Mbs.client.connect()
    if Mbs.client.connected:
        value = float(input('введи число: \n'))
        await Mbs.write_float(516, value)
        result = await Mbs.read_float(516)
        print(result)
    Mbs.client.close()


if __name__ == '__main__':
    asyncio.run(main())
