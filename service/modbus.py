from apscheduler.executors.base import logging
from pymodbus.framer import FramerType
from config import settings
from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient
from pymodbus.exceptions import ModbusException

logger = logging.getLogger(__name__)


def process_data(client: ModbusBaseClient, data: list):
    result = dict()
    level = data[:2]
    level.reverse()
    result["level"] = client.convert_from_registers(
        level,
        data_type=client.DATATYPE.FLOAT32,
    )
    result["accidents"] = data[-1]

    return result


async def create_modbus_client():
    return AsyncModbusTcpClient(
        settings.modbus.host,
        framer=FramerType.RTU,
        port=settings.modbus.port,
        timeout=3,
        retries=1,
        reconnect_delay=0.5,
        reconnect_delay_max=0.5,
    )


async def poll_registers(address, count) -> dict | None:
    try:
        async with await create_modbus_client() as client:
            if not client.connected:
                logger.error("Нет соединения с ПР")
                return

            try:
                data = await client.read_holding_registers(
                    address, count=count, slave=16
                )
                if data.isError():
                    logger.error(f"Чтение регистров завершилось ошибкой: {data}")
                    return
                return process_data(client, data.registers)
            except ModbusException as exc:
                logger.error(f"Ошибка протокола Modbus: {exc}")
                return

    except Exception as e:
        logger.error(f"Общая ошибка при подключении: {e}")
        return
