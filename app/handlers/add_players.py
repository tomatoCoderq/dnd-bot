import sqlite3, keyboards

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode


router = Router()


class AliasState(StatesGroup):
    waiting_alias = State()


@router.callback_query(F.data == "add")
async def ask_players_alias(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_text("Напишите <b>Alias</b> пользователя.\nЕсли игрок уже в вашей команде, то он <i>удалится</i> оттуда.", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
    await state.set_state(AliasState.waiting_alias)


@router.message(AliasState.waiting_alias, F.text)
async def alias_adding(message: types.Message, state: FSMContext):
    conn = sqlite3.connect("database/databasetg.db")
    cursor = conn.cursor()
    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    if message.text in users:
        for i in range(len(users_master)):
            print(i, message.text, users[i], message.from_user.username)
            if message.text == users[i] and users_master[i] == message.from_user.username:
                cursor.execute('UPDATE men SET master = ? WHERE user = ?', ("None", message.text))
                conn.commit()
                await message.answer(f"<b>Готово!</b>\n{message.text} удален из вашей комнаты", parse_mode=ParseMode.HTML, reply_markup=keyboards.KeyboardM())
                break
            elif message.text == users[i] and users_master[i] == "None":
                cursor.execute('UPDATE men SET master = ? WHERE user = ?', (message.from_user.username, message.text))
                conn.commit()
                await message.answer(f"<b>Дело сделано!</b>\nТеперь <i>{message.text}</i> в вашей комнате", parse_mode=ParseMode.HTML, reply_markup=keyboards.KeyboardM())
            elif message.text == users[i] and users_master[i] != message.from_user.username:
                await message.answer("Этот игрок уже <b>привязан</b> к Мастеру. Попробуйте другой Alias!", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
                return alias_adding
        await state.clear()

    else:
        await message.answer("⛔️Такого пользователя нет в нашей системе.\nПопробуйте еще раз или попросите игрока добавиться")
        return alias_adding

    conn.commit()
    conn.close()
