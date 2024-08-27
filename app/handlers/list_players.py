import sqlite3
from utilits import keyboards
from aiogram import F, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode
from loguru import logger

conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
dp = Dispatcher()
logger.info("connected to databasetg.db in list_players.py")


async def players(callback:types.CallbackQuery):

    users_master = [x[0] for x in cursor.execute("SELECT master FROM men").fetchall()]
    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]

    str = ''
    k = 0

    for i in range(len(users)):
        if users_master[i] == callback.from_user.username:
            k += 1
            str += f'<i>{k}</i>| <b>{users[i]}</b>\n'
    try:
        await callback.message.edit_text(str, reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
        await callback.answer()
        logger.info(f"Formed and send list of players {callback.from_user.username} {str}")

    except TelegramBadRequest as e:
        await callback.message.edit_text("В вашей комнате пока <b>нет игроков</b>.\nНажмите ➕<b>Добавить/Удалить игрока</b>➖, чтобы добавить игроков", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
        await callback.answer()
        logger.error(f"{e}: No players in master's room")


def register_list_handler(dp: Dispatcher):
    dp.callback_query.register(players, F.data == "players")
