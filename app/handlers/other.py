from aiogram import F, types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command

import keyboards


async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardM())


async def back_get_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardCheck())


async def back_more_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardInfo())


async def back_more_info_we(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardInfo())
    await callback.answer()


async def back_more_info_we_quest(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardQuestInfo())
    await callback.answer()


async def back_plot_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardStoryline())


async def back_player(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardP())
    await callback.answer()


async def back_quest(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardQuestGen())
    await callback.answer()


async def back_quest_more(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardQuestInfo())
    await callback.answer()

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
    await message.answer(ans, parse_mode=ParseMode.HTML)
    await message.answer(ans_2, reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)





def register_other_handler(dp: Dispatcher):
    dp.callback_query.register(back, F.data=="back")
    dp.callback_query.register(back_get_info, F.data == "back_get_info")
    dp.callback_query.register(back_plot_info, F.data == "back_plot_info")
    dp.callback_query.register(back_more_info, F.data == "back_more_info")
    dp.callback_query.register(back_more_info_we, F.data == "back_more_info_we")
    dp.callback_query.register(back_more_info_we_quest, F.data == "back_more_info_we_quest")
    dp.callback_query.register(back_player, F.data == "back_player")
    dp.callback_query.register(back_quest, F.data == "back_quest_gen")
    dp.callback_query.register(back_quest_more, F.data == "back_quest_more")
    dp.message.register(help,  Command("help"))
