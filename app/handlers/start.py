import sqlite3, keyboards
from aiogram.enums import ParseMode
from aiogram.filters import Command, state
from aiogram import Bot, F, types, Dispatcher


conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()


async def start(message: types.Message, bot: Bot):
    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    res_role = cursor.execute("SELECT title FROM men")
    roles = [x[0] for x in res_role.fetchall()]

    dict = {users[i]: roles[i] for i in range(len(users))}
    if message.from_user.username in users:
        if dict[message.from_user.username] == "master":
            await bot.send_message(chat_id=message.from_user.id, text="С возвращением, <b>Мастер подземелья!</b>", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(chat_id=message.from_user.id, text="С возвращением, <b>дорогой Игрок!</b>", reply_markup=keyboards.KeyboardP(), parse_mode=ParseMode.HTML)
    else:
        await message.answer(text="Здравствуйте! Мы рады, что вы хотите использовать <i>Tiny Master</i> бота.", parse_mode=ParseMode.HTML)
        await message.answer(text="\nСперва, пожалуйста, выберите роль: ", reply_markup=keyboards.KeyboardStart())


async def add_master(callback: types.CallbackQuery):
    add = [callback.from_user.id, callback.from_user.username, "master", 'None']

    cursor.execute("INSERT INTO men VALUES (?, ?, ?, ?)", add)
    conn.commit()

    await callback.message.edit_text("Хороших вам партий, <b>Мастер!</b>", reply_markup=keyboards.KeyboardM())
    await callback.answer()


async def add_player(callback: types.CallbackQuery):
    add = [callback.from_user.id, callback.from_user.username, "player", 'None']

    cursor.execute("INSERT INTO men VALUES (?, ?, ?, ?)", add)
    conn.commit()

    await callback.message.edit_text("Славных приключений, <b>Игрок!</b>")
    await callback.message.edit_text("Ожидайте, вскоре <b>Мастер</b> пришлёт вам опросы, которые помогут сделать игровой процесс лучше!", parse_mode=ParseMode.HTML)
    await callback.answer()


def register_start_handler(dp: Dispatcher):
    dp.message.register(start, Command('start'))
    dp.callback_query.register(add_master, F.data=="master")
    dp.callback_query.register(add_player, F.data=="player")
