import sqlite3, keyboards
from aiogram import F, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode


conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
dp = Dispatcher()


async def players(callback:types.CallbackQuery):
    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    str = ''
    k = 0

    for i in range(len(users)):
        if users_master[i] == callback.from_user.username:
            k += 1
            str += f'<i>{k}</i>| <b>{users[i]}</b>\n'
    try:
        await callback.message.edit_text(str, reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
        await callback.answer()
    except TelegramBadRequest as e:
        await callback.message.edit_text("В вашей комнате пока <b>нет игроков</b>.\nНажмите ➕<b>Добавить/Удалить игрока</b>➖, чтобы добавить игроков", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
        await callback.answer()


def register_list_handler(dp: Dispatcher):
    dp.callback_query.register(players, F.data == "players")
