import sqlite3

from aiogram import Dispatcher
from aiogram import types
from aiogram import Bot
from aiogram.filters import Command, state, StateFilter
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

import keyboards

conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()

async def choosing_type_survey(callback:types.CallbackQuery, bot:Bot):
    await callback.message.edit_text("Какой опрос вы хотите отправить?", reply_markup=keyboards.KeyboardSurvey())
    await callback.answer()

async def before_survey(callback:types.CallbackQuery, bot:Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/hJ169RhnZMmtvSr39")
    )
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]
    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]
    for i in range(len(ids)):
        if users_master[i] == callback.from_user.username:
            print(ids[i])
            await bot.send_message(chat_id=ids[i], text="Пройдите, пожалуйста, опрос <b>до начала игры</b>.\nРезультаты опроса помогут сделать игру качественнее для каждого игрока.", reply_markup=builder.as_markup())
    await callback.answer("Сделано!")
    await callback.message.edit_text("Что будем делать дальше, <b>Мастер</b>?", reply_markup=keyboards.KeyboardM())


async def during_survey(message:types.Message, bot:Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/hJ169RhnZMmtvSr39")
    )

    await message.answer("Сделано!")
    await message.answer("Что будем делать дальше, <b>Мастер</b<?", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)

async def after_survey(message:types.Message, bot:Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Опрос", url="https://forms.gle/6hmE5hcddqwSRBGZ7")
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
    await message.edit_text("Что будем делать дальше, Мастер?", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)

def register_survey_handler(dp: Dispatcher):
    dp.callback_query.register(choosing_type_survey, F.data=="share")
    dp.callback_query.register(before_survey, F.data=="before")
    dp.callback_query.register(during_survey, F.data=="during")
    dp.callback_query.register(after_survey, F.data=="after")

