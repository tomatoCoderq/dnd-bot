import sqlite3, googleapiclient, httplib2, asyncio, pandas as pd
from utilits import keyboards
from aiogram import F, Router, types, Dispatcher, Bot
import googleapiclient.discovery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from oauth2client.service_account import ServiceAccountCredentials
from GPTAPI import *
from aiogram.enums import ParseMode
from openai import RateLimitError
from openai import AuthenticationError
from aiogram.exceptions import TelegramNetworkError
from openai import PermissionDeniedError, APITimeoutError
from loguru import logger

from app.handlers.gen_main import generate
from aiohttp.client_exceptions import ClientConnectionError
import random
from config.config import *

client = AsyncOpenAI(
    api_key=apiKey)

router = Router()
conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
Requestor = RequestAPI(client)

global info
global info_2
global kand_input
global info_q_2


def get_service_sacc():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name('filestoread/dnd.json', scopes).authorize(httplib2.Http())
    return googleapiclient.discovery.build('sheets', 'v4', http=creds_service)


async def make_a_choice(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбирайте", reply_markup=keyboards.KeyboardCheck())
    await callback.answer()

# <---------------------------------------------------------------------->


async def checking_if_ready(callback: types.CallbackQuery):
    global info
    global info_2
    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
                                                          range="ответы!A2:K500").execute()

    pd.DataFrame(resp['values']).to_csv('filestoread/res.csv')

    #TODO: выбирать в таблицу только те данные, которые относятся к мастеру

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    myusers = [users[i] for i in range(len(users)) if users_master[i] == callback.from_user.username]
    print(myusers)

    answer = []
    for ans in resp['values']:
        if len(ans) != 0:
            if ans[-1] in myusers:
                answer.append(ans)
    length = len(answer)
    print(length, resp['values'])
    print(answer)

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    k = 0
    for master in users_master:
        if master == callback.from_user.username:
            k += 1

    if k != length:
        await callback.message.edit_text(
            "К сожалению, еще <b>не все игроки</b> закончили проходить опрос\nВозвращайтесь попозже!",
            reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
    else:
        try:
            await callback.message.edit_text(
                "Мы <b>получили</b> данные! Подождите <i>20 секунд</i>, идет обработка ответов", parse_mode=ParseMode.HTML)
            info = pd.DataFrame(answer).to_string()
            # info = pd.read_csv('filestoread/res.csv').to_string()
            info = await Requestor.get_request(AnalyzeBF(), info)
            await asyncio.sleep(7)
            print("DONE info")

            info_2 = await Requestor.get_request(RecommendationsBF(npc_indication="Брать данные из пункта npc_number. Если npc_number = 'Много', то сгенерировать npc в диапазоне [7;9]. Если npc_number = 'Мало', то сгенерировать npc в диапазоне [2;4]. Если npc_number = 'Средне', то сгенерировать npc в диапазоне [4;7] "), str(info))
            await asyncio.sleep(7)
            print("DONE info_2")

            await callback.message.edit_text("<b>Ответы готовы!</b>\nПройдите назад и нажмите 🚪Открыть",
                                             reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
        except (RateLimitError, AuthenticationError, TelegramNetworkError, PermissionDeniedError, APITimeoutError) as e:
            print(e)
            await callback.message.edit_text("🛑К сожалению, произошла ошибка со стороны библиотеки OpenAI. Попробуйте снова", reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)


async def salvation(message: types.Message):
    global info
    global info_2
    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
                                                          range="ответы!A2:K500").execute()

    pd.DataFrame(resp['values']).to_csv('filestoread/res.csv')

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    myusers = [users[i] for i in range(len(users)) if users_master[i] == message.from_user.username]
    print(myusers)

    answer = []
    for ans in resp['values']:
        if len(ans) != 0:
            if ans[-1] in myusers:
                print(ans[-1])
                answer.append(ans)
    length = len(answer)
    print(length, resp['values'])
    await message.answer("Мы <b>получили</b> данные! Подождите <i>20 секунд</i>, идет обработка ответов", parse_mode=ParseMode.HTML)

    try:
        info = pd.read_csv('filestoread/res.csv').to_string()
        info = await Requestor.get_request(AnalyzeBF(), info)
        await asyncio.sleep(7)
        print("DONE info")

        info_2 = await Requestor.get_request(RecommendationsBF(), str(info))
        await asyncio.sleep(7)
        print("DONE info_2")

        print(info_2)
        await message.edit_text("<b>Ответы готовы!</b>\nПройдите назад и нажмите 🚪Открыть",
                                reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
    except RateLimitError or AuthenticationError:
        await message.edit_text("🛑К сожалению, произошла ошибка со стороны библиотеки OpenAI", reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)

# <---------------------------------------------------------------------->


async def choosing_type_survey(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(f"   {info_2.setting}", reply_markup=keyboards.KeyboardInfo())
        await callback.answer()
    except NameError as e:
        await callback.message.edit_text("🚷Cюда пока что нельзя. Проверьте готовность, нажав ✔️Проверить готовность ",
                                         reply_markup=keyboards.KeyboardBackGetInfo())
        await callback.answer()


# <---------------------------------------------------------------------->


async def plot(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text("Выберите главу путешествия:", reply_markup=keyboards.KeyboardStoryline())
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()

async def beginning(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(f"{info_2.beginning}", reply_markup=keyboards.KeyboardBackPlotInfo())
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackPlotInfo(), parse_mode=ParseMode.HTML)
        await callback.answer()


async def center(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(f"{info_2.story_itself}", reply_markup=keyboards.KeyboardBackPlotInfo())
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackPlotInfo(), parse_mode=ParseMode.HTML)
        await callback.answer()


async def ending(callback: types.CallbackQuery):
    try:
        ans = ""
        for end in info_2.endings:
            ans += f"|<b>{end.type}</b>\n {end.description}\n\n"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackPlotInfo(), parse_mode=ParseMode.HTML)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackPlotInfo(), parse_mode=ParseMode.HTML)
        await callback.answer()



# <---------------------------------------------------------------------->


class LocState(StatesGroup):
    waiting_location = State()
    waiting_agree = State()


@router.callback_query(F.data == "locations")
async def locations(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for end in info_2.locations:
            ans += f"|<b>{end.name}</b>\n {end.description}\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о локации, а также ее изображение, напишите <i>название</i> локации</b>\n"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        await state.set_state(LocState.waiting_location)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        await callback.answer()


@router.message(LocState.waiting_location, F.text)
async def location_sending(message: types.Message, state: FSMContext):
    global kand_input
    locs = [loc.name for loc in info_2.locations]
    print(locs)
    if message.text in locs:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд', parse_mode=ParseMode.HTML)
        for end in info_2.locations:
            if message.text == end.name:
                try:
                    data = f"setting='{info_2.setting}' name='{end.name}', description='{end.description}'"
                    kand_input = await Requestor.get_request(RecommendationsLOC(), data)
                    print(kand_input)
                    await generate(style='ANIME', width=1024, height=1024,
                                   query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                                   file_name='images/imagel.png')
                    file = FSInputFile('images/imagel.png')
                    ans = f"<b>{kand_input.name}</b>\n\n"
                    ans += f"{kand_input.appearance}\n\n"
                    await message.answer_photo(file, caption=ans,
                                               reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                               parse_mode=ParseMode.HTML)
                    await state.set_state(LocState.waiting_agree)
                except TypeError as e:
                    await message.answer("Произошла ошибка. Попробуйте снова", reply_markup=keyboards.KeyboardBackMoreInfo())


    else:
        await message.answer("Такой локации нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return location_sending


@router.callback_query(LocState.waiting_agree, F.data == "send_players")
async def location_agree(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/imagel.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file, reply_markup=keyboards.KeyboardBackPlayer())
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку локации", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await state.clear()
# <---------------------------------------------------------------------->


class NpcMoreState(StatesGroup):
    waiting_npc = State()
    waiting_agree = State()


@router.callback_query(F.data == "npcs")
async def npcs(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for npc in info_2.npcs:
            ans += f"|<b>{npc.name}</b> ({npc.type})\n {npc.description}\n <i>Локации</i>: "
            for loc in npc.locations:
                ans += f"{loc}; "
            ans += "\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"

        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        await state.set_state(NpcMoreState.waiting_npc)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()



@router.message(NpcMoreState.waiting_npc, F.text)
async def npc_sending(message: types.Message, state: FSMContext):
    global kand_input
    npcs = [char.name for char in info_2.npcs]
    print(npcs)
    if message.text in npcs:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.npcs:
            if message.text == end.name:
                data = f"setting='{info_2.setting}' type='{end.type}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='images/image2.png')
                file = FSInputFile('images/image2.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await message.answer_photo(file, caption=ans,
                                           reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                           parse_mode=ParseMode.HTML)
                await state.set_state(NpcMoreState.waiting_agree)
    else:
        # print('none')
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return npc_sending


@router.callback_query(NpcMoreState.waiting_agree, F.data == "send_players")
async def npc_agree(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/image2.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file)
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку персонажа", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await state.clear()

# <---------------------------------------------------------------------->


class EnemyState(StatesGroup):
    waiting_enemy = State()
    waiting_agree = State()


@router.callback_query(F.data == "enemies")
async def enemies(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for end in info_2.enemies:
            ans += f"|<b>{end.name}</b> ({end.type})\n {end.description}\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        await state.set_state(EnemyState.waiting_enemy)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(EnemyState.waiting_enemy, F.text)
async def enemy_sending(message: types.Message, state: FSMContext):
    global kand_input
    enemies = [char.name for char in info_2.enemies]
    print(enemies)
    if message.text in enemies:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.enemies:
            if message.text == end.name:
                data = f"setting='{info_2.setting}' type='{end.type}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='images/image3.png')
                file = FSInputFile('images/image3.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await message.answer_photo(file, caption=ans, reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                           parse_mode=ParseMode.HTML)
                await state.set_state(EnemyState.waiting_agree)
    else:
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return enemy_sending


@router.callback_query(EnemyState.waiting_agree, F.data == "send_players")
async def enemy_agree(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/image3.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file)
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку персонажа", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await state.clear()

# <---------------------------------------------------------------------->


class BH_State(StatesGroup):
    waiting_bh = State()
    waiting_agree = State()


@router.callback_query(F.data == "bosses_heroes")
async def bosses_heroes(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for end in info_2.bosses_heroes:
            ans += f"|<b>{end.name}</b> ({end.type})\n {end.description}\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        await state.set_state(BH_State.waiting_bh)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(BH_State.waiting_bh, F.text)
async def bh_sending(message: types.Message, state: FSMContext):
    global kand_input
    bh = [char.name for char in info_2.bosses_heroes]
    print(bh)
    if message.text in bh:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.bosses_heroes:
            if message.text == end.name:
                data = f"setting='{info_2.setting}' type='{end.type}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='images/image4.png')
                file = FSInputFile('images/image4.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await message.answer_photo(file, caption=ans, reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                           parse_mode=ParseMode.HTML)
                await state.set_state(BH_State.waiting_agree)
    else:
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return bh_sending


@router.callback_query(BH_State.waiting_agree, F.data == "send_players")
async def bh_agree(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/image4.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file)
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку персонажа", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await state.clear()
# <---------------------------------------------------------------------->


async def more_info(callback: types.CallbackQuery):
    v = ["Да", "Нет"]
    try:
        ans = "|<b>Сеттинг</b>\n"
        for end in info.settings:
            ans += f"-<i>{end.type}</i>. {end.justification}\n"
        ans += "\n"
        ans += f"|<b>Геймплейное разнообразие</b>\n {info.gameplay_style}\n\n" \
               f"|<b>Количество NPC</b>\n {info.npc_number}\n\n" \
               f"|<b>Средняя длительность партии</b>\n {info.days_duration} дня\n\n" \
               f"|<b>Средняя длительность сессий</b>\n {info.session_duration} часа/ов\n\n"
        ans += f"|<b>Предпочтительные враги и NPC</b>\n"
        for end in info.enemy_npc:
            ans += f"-<i>{end.type}</i>. {end.justification}\n"
        ans += "\n"
        ans += f"|<b>Аудиовизуальное сопровождение</b>\n {random.choice(v)}\n\n" \
               f"|<b>Количество локаций</b>\n {info.location_number}\n\n"
        ans += "|Причины игры\n"
        for end in info.purpose_game:
            ans += f"-<i>{end.type}</i>. {end.justification}\n"

        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


# async def send_players(bot: Bot, callback: types.CallbackQuery):





# Quest sending part
# <---------------------------------------------------------------------->


async def make_a_choice_quest(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбирайте", reply_markup=keyboards.KeyboardQuestGen())
    await callback.answer()


async def checking_if_ready_quest(callback: types.CallbackQuery):
    global info_q_2

    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
                                                          range="ответы_игры!A2:E500").execute()

    pd.DataFrame(resp['values']).to_csv('filestoread/res_q.csv')

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    res_user = cursor.execute("SELECT user FROM men")
    users = [x[0] for x in res_user.fetchall()]

    myusers = [users[i] for i in range(len(users)) if users_master[i] == callback.from_user.username]
    print(myusers)

    answer = []
    for ans in resp['values']:
        if len(ans) != 0:
            if ans[-1] in myusers:
                print(ans[-1])
                answer.append(ans)
    length = len(answer)
    print(length, resp['values'])

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    k = 0

    for master in users_master:
        if master == callback.from_user.username:
            k += 1

    if k != length:
        await callback.message.edit_text(
            "К сожалению, еще <b>не все игроки</b> закончили проходить опрос\nВозвращайтесь попозже!",
            reply_markup=keyboards.KeybaordBackQuest(), parse_mode=ParseMode.HTML)
    else:
        await callback.message.edit_text(
            "Мы <b>получили</b> данные! Подождите <i>20 секунд</i>, идет обработка ответов", parse_mode=ParseMode.HTML)
        try:
            await asyncio.sleep(7)
            info_q_2 = await Requestor.get_request(RecommendationsQQ(npc_indication="В квесте должны быть написаны случайно выбранные персонажи из списка npcs входных данных"), str(info_2))
            await asyncio.sleep(7)
            print("DONE info_2_й")

            print(info_q_2)
            await callback.message.edit_text("<b>Квест готов!</b>\nПройдите назад и нажмите 🚪Открыть",
                                             reply_markup=keyboards.KeybaordBackQuest(), parse_mode=ParseMode.HTML)
        except (RateLimitError, NameError) as e:
            print(e)
            await callback.message.edit_text("🛑К сожалению, произошла ошибка.\n Попробуйте сперва сгенерировать информацию основной партии. Если это не помогло, то вероятно проблема со стороны библиотеки OpenAI", reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)


async def sending_quest_info(callback: types.CallbackQuery):
    try:
        ans = f"<b>{info_q_2.quest_name}</b> ({info_q_2.location})\n\n{info_q_2.description}"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardQuestInfo(), parse_mode=ParseMode.HTML)
    except NameError:
        await callback.message.edit_text("🚷Cюда пока что нельзя. Проверьте готовность, нажав ✔️Проверить готовность ",
                                         reply_markup=keyboards.KeybaordBackQuest())
        await callback.answer()



# <---------------------------------------------------------------------->


class NpcMoreQuestState(StatesGroup):
    waiting_npc = State()
    waiting_agree = State()


@router.callback_query(F.data == "npcs_quest")
async def npcs_quest(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for npc in info_q_2.npcs:
            ans += f"|<b>{npc.name}</b> ({npc.type})\n {npc.description}\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"

        await callback.message.edit_text(ans, reply_markup=keyboards.KeybaordBackQuestMore(), parse_mode=ParseMode.HTML)
        await state.set_state(NpcMoreQuestState.waiting_npc)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(NpcMoreQuestState.waiting_npc, F.text)
async def npc_sending_qest(message: types.Message, state: FSMContext):
    global kand_input
    npcs = [char.name for char in info_q_2.npcs]
    print(npcs)
    if message.text in npcs:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeybaordBackQuestMore(), parse_mode=ParseMode.HTML)
        try:
            for end in info_q_2.npcs:
                print(end.name)
                if message.text == end.name:
                    data = f"setting='{info_2.setting}' type='{end.type}' name='{end.name}', description='{end.description}'"
                    kand_input = await Requestor.get_request(RecommendationsAC(
                        phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                             data)
                    print(kand_input)
                    await generate(style='ANIME', width=1024, height=1024,
                                   query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                                   file_name='images/imageNpcQ.png')
                    file = FSInputFile('images/imageNpcQ.png')
                    ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                    ans += f"{kand_input.appearance}\n\n"
                    ans += f"<b>Фразы:</b>\n"
                    for phr in kand_input.phrases:
                        ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                    await message.answer_photo(file, caption=ans,
                                               reply_markup=keyboards.KeyboardBackMoreInfoWithoutEditQuest(),
                                               parse_mode=ParseMode.HTML)
                    await state.set_state(NpcMoreQuestState.waiting_agree)
        except ClientConnectionError as e:
            await message.answer("Ошибка подключения", reply_markup=keyboards.KeybaordBackQuest())
    else:
        # print('none')
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeybaordBackQuestMore(),
                             parse_mode=ParseMode.HTML)
        return npc_sending_qest


@router.callback_query(NpcMoreQuestState.waiting_agree, F.data == "send_players")
async def npc_agree_quest(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/imageNpcQ.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file)
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку персонажа", reply_markup=keyboards.KeybaordBackQuest(), parse_mode=ParseMode.HTML)
    await state.clear()

# <---------------------------------------------------------------------->


class EnemyQuestState(StatesGroup):
    waiting_enemy = State()
    waiting_agree = State()


@router.callback_query(F.data == "enemies_quest")
async def enemies_quest(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for npc in info_q_2.enemies:
            ans += f"|<b>{npc.name}</b> ({npc.type})\n {npc.description}\n\n"
        ans += "-----------------------------------------------------\n\n"
        ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"

        await callback.message.edit_text(ans, reply_markup=keyboards.KeybaordBackQuestMore(), parse_mode=ParseMode.HTML)
        await state.set_state(EnemyQuestState.waiting_enemy)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(EnemyQuestState.waiting_enemy, F.text)
async def enemy_sending_quest(message: types.Message, state: FSMContext):
    global kand_input
    enemies = [char.name for char in info_q_2.enemies]
    print(npcs)
    if message.text in enemies:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeybaordBackQuestMore(), parse_mode=ParseMode.HTML)
        try:
            for end in info_q_2.enemies:
                print(end.name)
                if message.text == end.name:
                    data = f"setting='{info_2.setting}' type='{end.type}' name='{end.name}', description='{end.description}'"
                    kand_input = await Requestor.get_request(RecommendationsAC(
                        phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                             data)
                    print(kand_input)
                    await generate(style='ANIME', width=1024, height=1024,
                                   query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                                   file_name='images/imageEnemyQ.png')
                    file = FSInputFile('images/imageEnemyQ.png')
                    ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                    ans += f"{kand_input.appearance}\n\n"
                    ans += f"<b>Фразы:</b>\n"
                    for phr in kand_input.phrases:
                        ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                    await message.answer_photo(file, caption=ans,
                                               reply_markup=keyboards.KeyboardBackMoreInfoWithoutEditQuest(),
                                               parse_mode=ParseMode.HTML)
                    await state.set_state(EnemyQuestState.waiting_agree)
        except ClientConnectionError as e:
            await message.answer("Ошибка подключения", reply_markup=keyboards.KeyboardQuestInfo())
    else:
        # print('none')
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeybaordBackQuestMore(),
                             parse_mode=ParseMode.HTML)
        return enemy_sending_quest


@router.callback_query(EnemyQuestState.waiting_agree, F.data == "send_players")
async def npc_agree_quest(message: types.Message, bot:Bot, state: FSMContext):
    res_master = cursor.execute("SELECT id FROM men")
    ids = [x[0] for x in res_master.fetchall()]

    res_master = cursor.execute("SELECT master FROM men")
    users_master = [x[0] for x in res_master.fetchall()]

    file = FSInputFile('images/imageEnemyQ.png')
    ans = f"<b>{kand_input.name}</b>\n\n"
    ans += f"{kand_input.appearance}\n\n"

    for i in range(len(ids)):
        if users_master[i] == message.from_user.username:
            print(ids[i])
            await bot.send_photo(chat_id=ids[i], caption=ans, parse_mode=ParseMode.HTML, photo=file)
    await bot.send_message(chat_id=message.from_user.id, text="Игроки получили карточку персонажа", reply_markup=keyboards.KeybaordBackQuest(), parse_mode=ParseMode.HTML)
    await state.clear()


# <---------------------------------------------------------------------->

async def rewards_quest(callback: types.CallbackQuery, state: FSMContext):
    try:
        ans = ""
        for npc in info_q_2.rewards:
            ans += f"|<b>{npc.name}</b>\n {npc.description}\n\n"
        await callback.message.edit_text(ans, reply_markup=keyboards.KeybaordBackQuestMore(), parse_mode=ParseMode.HTML)
    except NameError:
        await callback.message.edit_text(f"<b>Не пытайтесь обмануть систему! Сперва сформируйте ответ</b>", reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


# <---------------------------------------------------------------------->


def register_info_handler(dp: Dispatcher):
    dp.callback_query.register(make_a_choice, F.data == "data")
    dp.callback_query.register(checking_if_ready, F.data == "check_m")
    dp.callback_query.register(choosing_type_survey, F.data == "open")
    dp.callback_query.register(more_info, F.data == "precisely")
    dp.callback_query.register(plot, F.data == "plot")
    dp.callback_query.register(beginning, F.data == "beginning")
    dp.callback_query.register(center, F.data == "center")
    dp.callback_query.register(ending, F.data == "ending")
    dp.message.register(salvation, Command('save'))
    dp.callback_query.register(make_a_choice_quest, F.data == "quest_send")
    dp.callback_query.register(checking_if_ready_quest, F.data == "check_quest")
    dp.callback_query.register(sending_quest_info, F.data == "open_quest")
    dp.callback_query.register(rewards_quest, F.data == "rewards_quest")
