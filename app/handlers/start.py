import sqlite3
from utilits import keyboards
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Bot, F, types, Dispatcher
from loguru import logger


conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
logger.info("connected to databasetg.db in start.py")


async def start(message: types.Message, bot: Bot):

    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    roles = [x[0] for x in cursor.execute("SELECT title FROM men").fetchall()]
    dict = {users[i]: roles[i] for i in range(len(users))}

    if message.from_user.username in users:
        if dict[message.from_user.username] == "master":
            await bot.send_message(chat_id=message.from_user.id, text="С возвращением, <b>Мастер подземелья!</b>", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)
            logger.info(f"Signed in {message.from_user.username} as master")
        else:
            await bot.send_message(chat_id=message.from_user.id, text="С возвращением, <b>дорогой Игрок!</b>", reply_markup=keyboards.KeyboardP(), parse_mode=ParseMode.HTML)
            logger.info(f"Signed in {message.from_user.username} as user")
    else:
        await message.answer(text="Здравствуйте! Мы рады, что вы хотите использовать <i>Tiny Master</i> бота.", parse_mode=ParseMode.HTML)
        await message.answer(text="\nСперва, пожалуйста, выберите роль: ", reply_markup=keyboards.KeyboardStart())
        logger.info(f"{message.from_user.username} Started procces of signing up")


async def add_master(callback: types.CallbackQuery):
    add = [callback.from_user.id, callback.from_user.username, "master", 'None']

    cursor.execute("INSERT INTO men VALUES (?, ?, ?, ?)", add)
    conn.commit()
    logger.success(f"Added {callback.from_user.username} to database as master")

    await callback.message.edit_text("Хороших вам партий, <b>Мастер!</b>", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)
    await callback.answer()


async def add_player(callback: types.CallbackQuery):
    add = [callback.from_user.id, callback.from_user.username, "player", 'None']

    cursor.execute("INSERT INTO men VALUES (?, ?, ?, ?)", add)
    conn.commit()
    logger.success(f"Added {callback.from_user.username} to database as user")


    await callback.message.edit_text("Славных приключений, <b>Игрок!</b>", parse_mode=ParseMode.HTML)
    await callback.message.edit_text("Ожидайте, вскоре <b>Мастер</b> пришлёт вам опросы, которые помогут сделать игровой процесс лучше!", reply_markup=keyboards.KeyboardP(), parse_mode=ParseMode.HTML)
    await callback.answer()


def register_start_handler(dp: Dispatcher):
    dp.message.register(start, Command('start'))
    dp.callback_query.register(add_master, F.data=="master")
    dp.callback_query.register(add_player, F.data=="player")
