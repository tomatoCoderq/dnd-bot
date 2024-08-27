import sqlite3

import utilits.remove
from utilits import keyboards
from aiogram import F, types, Dispatcher
from aiogram.filters import Command
from aiogram.enums import ParseMode
from loguru import logger


conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
logger.info("connected to databasetg.db in others.py")


async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardM())
    await callback.answer()
    logger.info("Pressed back button, returns KeyboardM")


async def back_get_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardCheck())
    await callback.answer()
    logger.info("Pressed back_get_info button, returns KeyboardCheck")


async def back_more_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardInfo())
    await callback.answer()
    logger.info("Pressed back_more_info button, returns KeyboardInfo")


async def back_more_info_we(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardInfo())
    await callback.answer()
    logger.info("Pressed back_more_info_without_edit button, returns KeyboardInfo")


async def back_more_info_we_quest(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardQuestInfo())
    await callback.answer()
    logger.info("Pressed back_more_info_without_edit_quest button, returns KeyboardQuestInfo")


async def back_plot_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardStoryline())
    await callback.answer()
    logger.info("Pressed back_plot_info button, returns KeyboardStooryLine")


async def back_player(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardP())
    await callback.answer()
    logger.info("Pressed back_player button, returns KeyboardP")


async def back_quest(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardQuestGen())
    await callback.answer()
    logger.info("Pressed back_quest button, returns KeyboardQuestGen")


async def back_quest_more(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardQuestInfo())
    await callback.answer()
    logger.info("Pressed back_quest_more button, returns KeyboardQuestInfo")


async def help(message: types.Message):
    ans = '''В нашей системе существуют две роли: Мастер и Игрок.\n
Основа работы бота - функция "комнат", где к каждому Мастеру могут быть привязано определенное количество игроков. Если Игрок уже привязан к другому Мастеру, то добавить его не получится.\n
Интерфейс Игрока:
    ▶️Генерация картинок
    Здесь Игрок может свободно генерировать любые запросы(Например, для создания аватара своего персонажа или визуализации своих действий)
    ▶️Дополнительные возможности
    Отдельно игрок может получать различных персонажей и локации до и в течение игры
Интерфейс Мастера:
    ▶️Мои игроки
    Здесь Мастер может посмотреть список игроков, которые находятся в его комнате.\n
    ▶️Добавить/Удалить игрока
    Здесь Мастер может добавить или удалить игроков. Если пользователь уже в комнате Мастера, то, написав его Alias, вы удалите его. 
    ▶️Поделиться опросом
    Здесь Мастер может поделиться опросом с Игроками, которые добавлены в его комнату. Отсылайте запрос до игры и в течение игры.
    ▶️Создание партии
    Основное меню. Здесь Мастер сперва, нажимая Прооверить готовность, а после, нажимая Открыть, получает полный ответ, созданный ChatGPT на основе ответов игроков.
    ▶️Создание квеста
    Здесь Мастер может создавать квик-квесты во время партии, чтобы разнообразить геймплей. Сперва требуется отправить опрос игрокам.
    ▶️Генерация картинок
    Здесь Мастер может свободно генерировать любые запросы, что поможет во время подготовки партии и во время партии.

    '''
    ans_2 = '''Мануал использования:\n 
    1. Добавьте игроков в комнату
    2. Проверьте все ли игроки добавлены
    3. Отправьте всем игрокам опрос
    4. Дождитесь пока все игроки пройдут опрос. Проверить это можно, нажав Проверить готовность
    5. Пройдите в Открыть
    6. Просмотрите все разделы, в некоторых можно сгенерировать карточки локаций/персонажей
    7. Сохраните все, что нужно.
    8. Во время игры отошлите новый опрос
    9. Создайте квик-квест
    '''

    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    roles = [x[0] for x in cursor.execute("SELECT title FROM men").fetchall()]

    await message.answer(ans, parse_mode=ParseMode.HTML)

    for i in range(len(users)):
        if users[i] == message.from_user.username and roles[i] == 'master':
            await message.answer(ans_2, reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
        if users[i] == message.from_user.username and roles[i] == 'player':
            await message.answer(ans_2, reply_markup=keyboards.KeyboardBackPlayer(), parse_mode=ParseMode.HTML)


async def change_role(message: types.Message):

    users_master = [x[0] for x in cursor.execute("SELECT master FROM men").fetchall()]
    roles = [x[0] for x in cursor.execute("SELECT title FROM men").fetchall()]
    users = [x[0] for x in cursor.execute("SELECT user FROM men").fetchall()]
    logger.info("Begin changing role")

    for i in range(len(users)):
        if users[i] == message.from_user.username and roles[i] == 'master':
            for j in range(len(users)):
                if users_master[j] == message.from_user.username:

                    cursor.execute('UPDATE men SET master = ? WHERE user = ?', ("None", users[j]))
                    conn.commit()
                    logger.success(f"Deleted all players in master room")

                    utilits.remove.delete_answers(users[j], "ответы")
                    logger.success(f"Deleted all answers in Google Sheet")

            cursor.execute('UPDATE men SET title = ? WHERE user = ?', ("player", message.from_user.username))
            logger.success(f"Updated role from Master to Player {message.from_user.username}")
            conn.commit()

            cursor.execute('UPDATE men SET id = ? WHERE user = ?', (message.from_user.id, message.from_user.username))
            logger.success(f"Updated ID of {message.from_user.username}")
            conn.commit()
            await message.answer("Поздравляем, ваша роль теперь <b>Игрок!</b>\nДля более подробной информации <i>/help</i>", reply_markup=keyboards.KeyboardP(), parse_mode=ParseMode.HTML)

        if users[i] == message.from_user.username and roles[i] == 'player' and users_master[i] == "None":

            cursor.execute('UPDATE men SET title = ? WHERE user = ?', ("master", message.from_user.username))
            conn.commit()
            logger.success(f"Updated role from Player to Master {message.from_user.username}")

            cursor.execute('UPDATE men SET id = ? WHERE user = ?', (message.from_user.id, message.from_user.username))
            conn.commit()
            logger.success(f"Updated ID of {message.from_user.username}")

            await message.answer("Поздравляем, ваша роль теперь <b>Мастер!</b>\nДля более подробной информации <i>/help</i>", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)

        if users[i] == message.from_user.username and roles[i] == 'player' and users_master[i] != "None":

            await message.answer("Вы находитесь в комнате у <b>Мастера</b>\nСперва попросите удалить вас из комнаты", reply_markup=keyboards.KeyboardP(), parse_mode=ParseMode.HTML)
            logger.warning(f"{message.from_user.username} is part of master's room")


def register_other_handler(dp: Dispatcher):
    dp.callback_query.register(back, F.data == "back")
    dp.callback_query.register(back_get_info, F.data == "back_get_info")
    dp.callback_query.register(back_plot_info, F.data == "back_plot_info")
    dp.callback_query.register(back_more_info, F.data == "back_more_info")
    dp.callback_query.register(back_more_info_we, F.data == "back_more_info_we")
    dp.callback_query.register(back_more_info_we_quest, F.data == "back_more_info_we_quest")
    dp.callback_query.register(back_player, F.data == "back_player")
    dp.callback_query.register(back_quest, F.data == "back_quest_gen")
    dp.callback_query.register(back_quest_more, F.data == "back_quest_more")
    dp.message.register(change_role, Command("change"))
    dp.message.register(help, Command("help"))
