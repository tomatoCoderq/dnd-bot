from aiogram import types

def KeyboardStart():
    buttons = [[types.InlineKeyboardButton(text="Мастер", callback_data="master")],
               [types.InlineKeyboardButton(text="Игрок", callback_data="player")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardPlayer():
    buttons = [[types.KeyboardButton(text="Роль")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def KeyboardM():
    buttons = [[types.InlineKeyboardButton(text="‍👨Мои игроки👩‍🦱", callback_data="players")],
               [types.InlineKeyboardButton(text="➕Добавить/Удалить игрока➖", callback_data="add")],
               [types.InlineKeyboardButton(text="✉️Поделиться опросом✉", callback_data="share")],
               [types.InlineKeyboardButton(text="ℹ️Данные для следующей партииℹ️", callback_data="data")],
               [types.InlineKeyboardButton(text="🍨Генерация картинок🍨", callback_data="gen_main")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardP():
    buttons = [[types.InlineKeyboardButton(text="Кнопка", callback_data="butt")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardSurvey():
    buttons = [[types.InlineKeyboardButton(text="🌆️Опрос перед игрой", callback_data="before")],
               [types.InlineKeyboardButton(text="🏙Опрос в течение игры", callback_data="during")],
               [types.InlineKeyboardButton(text="🌃Опрос после игры", callback_data="after")],
               [types.InlineKeyboardButton(text="◀️Назад", callback_data="back")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def KeyboardInfo():
    buttons = [[types.InlineKeyboardButton(text="🪧Сюжет", callback_data="plot")],
               [types.InlineKeyboardButton(text="📍Локации", callback_data="locations")],
               [types.InlineKeyboardButton(text="👨‍🎤NPC", callback_data="npcs")],
               [types.InlineKeyboardButton(text="🧛‍Враги", callback_data="enemies")],
               [types.InlineKeyboardButton(text="🤴Боссы-Герои", callback_data="bosses_heroes")],
               [types.InlineKeyboardButton(text="⏺Подробнее", callback_data="precisely")],
               [types.InlineKeyboardButton(text="◀️Назад", callback_data="back")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardStoryline():
    buttons = [[types.InlineKeyboardButton(text="🌕Начало", callback_data="beginning")],
               [types.InlineKeyboardButton(text="🌗Центр", callback_data="center")],
               [types.InlineKeyboardButton(text="🌑Финал", callback_data="ending")],
               [types.InlineKeyboardButton(text="◀️Назад", callback_data="back_more_info")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def KeyboardBack():
    buttons = [[types.InlineKeyboardButton(text="◀️Назад", callback_data="back")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardCheck():
    buttons = [[types.InlineKeyboardButton(text="✔️Проверить готовность", callback_data="check_m")],
               [types.InlineKeyboardButton(text="🚪Открыть", callback_data="open")],
               [types.InlineKeyboardButton(text="◀️Назад", callback_data="back")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardBackGetInfo():
    buttons = [[types.InlineKeyboardButton(text="◀️Назад", callback_data="back_get_info")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardBackMoreInfo():
    buttons = [[types.InlineKeyboardButton(text="◀️Назад", callback_data="back_more_info")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def KeyboardBackMoreInfoWithoutEdit():
    buttons = [[types.InlineKeyboardButton(text="◀️Назад", callback_data="back_more_info_we")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def KeyboardBackPlotInfo():
    buttons = [[types.InlineKeyboardButton(text="◀️Назад", callback_data="back_plot_info")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# def reports_inline_keyboard():
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     buttons = [types.InlineKeyboardButton('Отчет за день', callback_data='b1'), types.InlineKeyboardButton('Отчет за неделю', callback_data='b2'),
#                types.InlineKeyboardButton('Отчет за месяц', callback_data='b3')]
#     keyboard.add(*buttons)
#     return keyboard

