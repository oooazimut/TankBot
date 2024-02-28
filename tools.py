from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from config import NET_DATA

mb_client = AsyncModbusTcpClient(
    host=NET_DATA.localhost,
    port=NET_DATA.localport,
    framer=ModbusRtuFramer
)
