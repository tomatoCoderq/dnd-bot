import sqlite3

from aiogram import Dispatcher
from aiogram import types
from aiogram import Bot
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from utilits import keyboards, remove
from loguru import logger

conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
logger.info("connected to databasetg.db in send_survey.py")


async def choosing_type_survey(callback:types.CallbackQuery, bot:Bot):
    await callback.message.edit_text("Какой опрос вы хотите отправить?", reply_markup=keyboards.KeyboardSurvey())
    await callback.answer()


async def before_survey(callback:types.CallbackQuery, bot:Bot):

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/hJ169RhnZMmtvSr39")
    )

    ids = [x[0] for x in cursor.execute("SELECT id FROM men").fetchall()]
    users_master = [x[0] for x in cursor.execute("SELECT master FROM men").fetchall()]
    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    roles = [x[0] for x in cursor.execute("SELECT title FROM men").fetchall()]


    for i in range(len(ids)):
        if users_master[i] == callback.from_user.username:
            print(f"{ids[i]}", callback.from_user.id)
            await bot.send_message(chat_id=f"{ids[i]}", text="Пройдите, пожалуйста, опрос <b>до начала игры</b>.\nРезультаты опроса помогут сделать игру качественнее для каждого игрока.", reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
            logger.success(f"Sending to {ids[i]} survey before game")

    for i in range(len(users)):
        if users[i] == callback.from_user.username and roles[i] == 'master':
            for j in range(len(users)):
                if users_master[j] == callback.from_user.username:
                    print(users[j])
                    remove.delete_answers(users[j], "ответы")
                    logger.success(f"Deleting previous answers of {users[j]} before game")

    await callback.answer("Сделано!")
    await callback.message.edit_text("Что будем делать дальше, <b>Мастер</b>?", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)


async def during_survey(callback:types.CallbackQuery, bot:Bot):
    builder_d = InlineKeyboardBuilder()
    builder_d.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/81vPhbsgnfyBZL84A")
    )

    ids = [x[0] for x in cursor.execute("SELECT id FROM men").fetchall()]
    users_master = [x[0] for x in cursor.execute("SELECT master FROM men").fetchall()]
    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    roles = [x[0] for x in cursor.execute("SELECT title FROM men").fetchall()]

    for i in range(len(ids)):
        if users_master[i] == callback.from_user.username:
            await bot.send_message(chat_id=ids[i], text="Пройдите, пожалуйста, опрос.\nРезультаты опроса помогут сделать игру качественнее для каждого игрока.", reply_markup=builder_d.as_markup(), parse_mode=ParseMode.HTML)
            logger.success(f"Sending to {ids[i]} survey during the game")

    for i in range(len(users)):
        if users[i] == callback.from_user.username and roles[i] == 'master':
            for j in range(len(users)):
                if users_master[j] == callback.from_user.username:
                    print(users[j])
                    remove.delete_answers(users[j], "ответы_игры")
                    logger.success(f"Deleting previous answers of {users[j]} during game")


    await callback.answer("Сделано!")
    await callback.message.answer("Что будем делать дальше, <b>Мастер</b>?", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)

async def after_survey(message:types.Message, bot:Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/m1hFQom8G8jmSbwK7")
    )
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]
    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]
    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_message(chat_id=ids[i], text="Пройдите опрос бро", reply_markup=builder.as_markup())
    await message.answer("Сделано!")
    await message.edit_text("Что будем делать дальше, <b>Мастер?</b>", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)

def register_survey_handler(dp: Dispatcher):
    dp.callback_query.register(choosing_type_survey, F.data=="share")
    dp.callback_query.register(before_survey, F.data=="before")
    dp.callback_query.register(during_survey, F.data=="during")
    dp.callback_query.register(after_survey, F.data=="after")

