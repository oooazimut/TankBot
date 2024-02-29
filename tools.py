from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from config import NET_DATA

framer = ModbusRtuFramer

mb_client = AsyncModbusTcpClient(
    host=NET_DATA.localhost,
    port=NET_DATA.localport,
    framer=framer
)


class PlotService:
    def show_current_level(self):
        pass

    def show_archive_levels(self):
        pass


plot_service = PlotService()
