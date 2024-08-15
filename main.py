import sqlite3
from aiogram import Bot, types, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
import asyncio
from aiogram.enums import ParseMode

from app.config_reader import load_config
from app.handlers.start import register_start_handler
from app.handlers.list_players import register_list_handler
from app.handlers import add_players
from app.handlers.send_survey import register_survey_handler
from app.handlers.other import register_other_handler
from app.handlers import gen_main
from app.handlers.get_info import register_info_handler
from app.handlers import get_info



# from app.handlers.get_photo import register_getphoto_handler
# from app.handlers.report_archive import register_report_archive_handler

async def main():
    logger.add("logs.log", format="{time} {message}", rotation="10MB")
    logger.info("Starting bot")
    config = load_config('config/main.ini')

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=MemoryStorage())

    conn = sqlite3.connect("database/databasetg.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS men(id, user, title, master)")

    dp.include_router(add_players.router)
    dp.include_router(gen_main.router)
    dp.include_router(get_info.router)

    # register_common_handler(dp)
    # register_getphoto_handler(dp)
    # register_report_archive_handler(dp)
    register_info_handler(dp)
    register_start_handler(dp)
    register_list_handler(dp)
    register_survey_handler(dp)
    register_other_handler(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
