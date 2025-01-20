from enum import StrEnum

from aiogram import Bot
from apscheduler.executors.base import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import settings
from db.models import Level
from db.repo import los
from service.mailing import send_message
from service.modbus import poll_registers

logger = logging.getLogger(__name__)
default_accidents = 0


class Messages(StrEnum):
    SENSOR_FAILURE = "Авария датчика уровня!"
    FIRST_CRIT_LEVEL = "Первый критический уровень, необходимо проверить работу насоса!"
    SECOND_CRIT_LEVEL = "Второй критический уровень, ёмкость скоро переполнится!"
    CURR_SENSOR_FAILURE = "Авария датчика тока!"
    HIGH_CURRENT_FAILURE = "Превышение рабочего тока!"
    POSSIBLY_LACK_OF_POWER = "Возможно, насос неисправен или на него не подается питание, превышение уровня воды включения насоса!"
    POSSIBLY_DEFECTIVE_PUMP = "Неисправен насос или засорение водопровода - уровень жидкости не падает при работе насоса!"


def is_warning(level) -> bool:
    return settings.tank.warning < level <= settings.tank.critical


def is_critical(level) -> bool:
    return settings.tank.critical < level <= settings.tank.high_border


def is_failure(level) -> bool:
    return any([level < settings.tank.low_border, level > settings.tank.high_border])


def is_normal(level) -> bool:
    return settings.tank.low_border <= level <= settings.tank.warning


async def check_alarm(bot: Bot, db_pool: async_sessionmaker[AsyncSession]):
    txt = ""
    async with db_pool() as session:
        level = await los.get_last(session)
        if not level:
            return
        match level.level:
            case l if is_failure(l):
                txt = Messages.SENSOR_FAILURE
            case l if is_warning(l):
                txt = Messages.FIRST_CRIT_LEVEL
            case l if is_critical(l):
                txt = Messages.SECOND_CRIT_LEVEL
            case l if l >= settings.tank.pump_on:
                txt = Messages.POSSIBLY_LACK_OF_POWER

        if txt:
            await send_message(txt, session, bot)


async def check_level(
    level: float, prev_level: float, bot: Bot, session: AsyncSession
) -> None:
    txt = ""
    match prev_level, level:
        case p, c if not is_failure(p) and is_failure(c):
            txt = Messages.SENSOR_FAILURE
        case p, c if not is_warning(p) and is_warning(c):
            txt = Messages.FIRST_CRIT_LEVEL
        case p, c if not is_critical(p) and is_critical(c):
            txt = Messages.SECOND_CRIT_LEVEL
        case p, c if p < settings.tank.pump_on and c >= settings.tank.pump_on:
            txt = Messages.POSSIBLY_LACK_OF_POWER

    if txt:
        await send_message(txt, session, bot)


async def check_accidents(accidents: int, session: AsyncSession, bot: Bot):
    txt = ""
    match accidents:
        case 1:
            txt = Messages.HIGH_CURRENT_FAILURE
        case 2:
            txt = Messages.POSSIBLY_DEFECTIVE_PUMP
        case 3:
            txt = (
                Messages.HIGH_CURRENT_FAILURE + "\n" + Messages.POSSIBLY_DEFECTIVE_PUMP
            )
    await send_message(txt, session, bot)


async def poll_and_save(bot: Bot, db_pool: async_sessionmaker[AsyncSession]):
    global default_accidents
    rr = await poll_registers(512, 3)

    if not rr:
        logger.error("Не получены данные по модбас!")
        return

    async with db_pool() as session:
        curr_level = Level(level=rr["level"])
        prev_level = await los.get_last(session)
        if prev_level:
            await check_level(
                curr_level.level,
                prev_level.level,
                bot,
                session,
            )

        if rr["accidents"] and rr["accidents"] != default_accidents:
            await check_accidents(rr["accidents"], session, bot)
            default_accidents = rr["accidents"]

        await los.new(session, curr_level)
