from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient
from pymodbus.constants import Endian
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from config import NET_DATA

framer = ModbusRtuFramer

mb_client = AsyncModbusTcpClient(
    host=NET_DATA.localhost,
    port=NET_DATA.localport,
    framer=framer
)


class ModbusService:
    client: ModbusBaseClient = mb_client
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

    @classmethod
    async def write_float(cls, register, value):
        cls.builder.add_32bit_float(value)
        payload = cls.builder.build()
        await cls.client.write_registers(address=register, values=payload, slave=16, skip_encode=True)

    @classmethod
    async def read_float(cls, register):
        data = await cls.client.read_holding_registers(register, 2, 16)
        result = data
        if not data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
            result = decoder.decode_32bit_float()
        return result
