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
    def convert_to_float(cls, registers: list):
        decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        result = decoder.decode_32bit_float()
        return result
