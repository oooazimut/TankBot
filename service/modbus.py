import itertools

from apscheduler.executors.base import logging
from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient
from pymodbus.exceptions import ModbusException
from pymodbus.framer import FramerType

from config import settings

logger = logging.getLogger(__name__)

mb_ports = itertools.cycle([settings.modbus.port_l2tp, settings.modbus.port_pptp])
curr_port = next(mb_ports)
wrong_connections = 0


def process_data(client: ModbusBaseClient, data: list):
    result = dict()

    level = data[:2]
    level.reverse()
    result["level"] = client.convert_from_registers(
        level,
        data_type=client.DATATYPE.FLOAT32,
    )

    result["accidents"] = data[2]

    current = data[3::]
    current.reverse()
    result["current"] = client.convert_from_registers(
        current,
        data_type=client.DATATYPE.FLOAT32,
    )

    return result


async def create_modbus_client(port: int):
    return AsyncModbusTcpClient(
        settings.modbus.host,
        framer=FramerType.RTU,
        port=port,
        timeout=3,
        retries=1,
        reconnect_delay=0.5,
        reconnect_delay_max=0.5,
    )


async def poll_registers(address, count) -> dict | None:
    global wrong_connections
    global curr_port
    if wrong_connections == 5:
        curr_port = next(mb_ports)
        logger.error('переключаюсь на другой порт...')
        wrong_connections = 0
    try:
        async with await create_modbus_client(curr_port) as client:
            if not client.connected:
                logger.error("Нет соединения с ПР")
                wrong_connections += 1
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
