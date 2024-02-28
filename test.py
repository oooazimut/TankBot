import asyncio

from tools import mb_client


async def client_test():
    await mb_client.connect()

    if mb_client.connected:
        await mb_client.write_register(address=515, value=8, slave=16)
        rr = await mb_client.read_holding_registers(address=515, slave=16)
        if not rr.isError():
            print(rr.registers)
        else:
            print(rr)
    mb_client.close()


asyncio.run(client_test())
