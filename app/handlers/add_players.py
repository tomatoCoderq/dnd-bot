import sqlite3
from utilits import keyboards

from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from loguru import logger


router = Router()


class AliasState(StatesGroup):
    waiting_alias = State()


@router.callback_query(F.data == "add")
async def ask_players_alias(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_text("Напишите <b>Alias</b> пользователя.\nЕсли игрок уже в вашей команде, то он <i>удалится</i> оттуда.", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
    await state.set_state(AliasState.waiting_alias)
    logger.info("Setting first state in adding/deleting user")


@router.message(AliasState.waiting_alias, F.text)
async def alias_adding(message: types.Message, bot:Bot, state: FSMContext):

    conn = sqlite3.connect("database/databasetg.db")
    cursor = conn.cursor()

    logger.info("Go to second state, handle username")

    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    users_master = [x[0] for x in cursor.execute("SELECT master FROM men").fetchall()]
    ids = [x[0] for x in cursor.execute("SELECT id FROM men").fetchall()]

    if message.text in users:
        for i in range(len(users_master)):
            if message.text == users[i] and users_master[i] == message.from_user.username:

                cursor.execute('UPDATE men SET master = ? WHERE user = ?', ("None", message.text))
                conn.commit()

                logger.success(f"Updated column master of {message.text} from {message.from_user.username} to 'None'")
                await message.answer(f"<b>Готово!</b>\n{message.text} удален из вашей комнаты", parse_mode=ParseMode.HTML, reply_markup=keyboards.KeyboardM())
                await bot.send_message(chat_id=ids[i], text=f"Вы были удалены из комнаты <b>Мастера</b> {message.from_user.username}", parse_mode=ParseMode.HTML)
                break

            elif message.text == users[i] and users_master[i] == "None":
                cursor.execute('UPDATE men SET master = ? WHERE user = ?', (message.from_user.username, message.text))
                conn.commit()

                await message.answer(f"<b>Дело сделано!</b>\nТеперь <i>{message.text}</i> в вашей комнате", parse_mode=ParseMode.HTML, reply_markup=keyboards.KeyboardM())
                await bot.send_message(chat_id=ids[i], text=f"Теперь вы в комнате <b>Мастера</b> {message.from_user.username}", parse_mode=ParseMode.HTML)
                logger.success(f"Updated column master of {message.text} from 'None' to {message.from_user.username}")

            elif message.text == users[i] and users_master[i] != message.from_user.username:
                await message.answer("Этот игрок уже <b>привязан</b> к Мастеру. Попробуйте другой Alias!", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
                return alias_adding

        await state.clear()

    else:
        await message.answer("⛔️Такого пользователя нет в нашей системе.\nПопробуйте еще раз или попросите игрока добавиться")
        logger.error(f"User {message.text} not found in system")
        return alias_adding

    conn.commit()
    conn.close()
