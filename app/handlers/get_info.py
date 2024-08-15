import sqlite3, googleapiclient, httplib2, asyncio, keyboards, pandas as pd
from aiogram import F, Router, types, Dispatcher
import googleapiclient.discovery
from aiogram.filters import ExceptionTypeFilter, state
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from oauth2client.service_account import ServiceAccountCredentials
from GPTAPI import *
from aiogram.enums import ParseMode

from app.handlers.add_players import AliasState
from app.handlers.gen_main import generate

client = AsyncOpenAI(
    api_key='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')

router = Router()
conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
Requestor = RequestAPI(client)

global info
global info_2


def get_service_sacc():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name('dnd.json', scopes).authorize(httplib2.Http())
    return googleapiclient.discovery.build('sheets', 'v4', http=creds_service)


async def make_a_choice(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбирайте", reply_markup=keyboards.KeyboardCheck())
    await callback.answer()


async def checking_if_ready(callback: types.CallbackQuery):
    global info
    global info_2
    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
                                                          range="ответы!A2:K500").execute()

    pd.DataFrame(resp['values']).to_csv('res.csv')

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
            reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
    else:
        await callback.message.edit_text(
            "Мы <b>получили</b> данные! Подождите <i>20 секунд</i>, идет обработка ответов", parse_mode=ParseMode.HTML)

        info = pd.read_csv('res.csv').to_string()
        info = await Requestor.get_request(AnalyzeBF(), info)
        await asyncio.sleep(7)
        print("DONE info")

        info_2 = await Requestor.get_request(RecommendationsBF(), str(info))
        await asyncio.sleep(7)
        print("DONE info_2")

        print(info_2)
        await callback.message.edit_text("<b>Ответы готовы!</b>\nПройдите назад и нажмите 🚪Открыть",
                                         reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)


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
    await callback.message.edit_text("Выберите главу путешествия:", reply_markup=keyboards.KeyboardStoryline())
    await callback.answer()


async def beginning(callback: types.CallbackQuery):
    await callback.message.edit_text(f"{info_2.beginning}", reply_markup=keyboards.KeyboardBackPlotInfo())
    await callback.answer()


async def center(callback: types.CallbackQuery):
    await callback.message.edit_text(f"{info_2.story_itself}", reply_markup=keyboards.KeyboardBackPlotInfo())
    await callback.answer()


async def ending(callback: types.CallbackQuery):
    ans = ""
    for end in info_2.endings:
        ans += f"|<b>{end.type}</b>\n {end.description}\n\n"
    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackPlotInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


# <---------------------------------------------------------------------->


class LocState(StatesGroup):
    waiting_location = State()


@router.callback_query(F.data == "location")
async def locations(callback: types.CallbackQuery, state: FSMContext):
    ans = ""
    for end in info_2.locations:
        ans += f"|<b>{end.name}</b>\n {end.description}\n\n"
    ans += f"<b>Если вы хотите увидеть более подробную информацию о локации, а также ее изображение, напишите <i>название</i> локации</b>\n"
    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()
    await state.set_state(LocState.waiting_location)


@router.message(LocState.waiting_location, F.text)
async def location_sending(callback: types.CallbackQuery, state: FSMContext):
    locs = [loc.name for loc in info_2.locations]
    print(locs)
    if callback.message.text in locs:
        await callback.message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                                      reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.locations:
            if callback.message.text == end.name:
                data = f"setting='{info_2.setting}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsLOC(), data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='image3.png')
                file = FSInputFile('image3.png')
                ans = f"<b>{kand_input.name}</b>\n\n"
                ans += f"{kand_input.appearance}\n\n"
                await callback.message.answer_photo(file, caption=ans,
                                                    reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                                    parse_mode=ParseMode.HTML)
    else:
        await callback.message.answer("Такой локации нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                                      parse_mode=ParseMode.HTML)
        return location_sending
    await state.clear()
    await callback.answer()


# <---------------------------------------------------------------------->


class NpcMoreState(StatesGroup):
    waiting_npc = State()


@router.callback_query(F.data == "npcs")
async def npcs(callback: types.CallbackQuery, state: FSMContext):
    ans = ""
    for npc in info_2.npcs:
        ans += f"|<b>{npc.name}</b> ({npc.type})\n {npc.description}\n <i>Локации</i>: "
        for loc in npc.locations:
            ans += f"{loc}; "
        ans += "\n\n"
    ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"

    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()
    await state.set_state(NpcMoreState.waiting_npc)


@router.message(NpcMoreState.waiting_npc, F.text)
async def npc_sending(callback: types.CallbackQuery, state: FSMContext):
    npcs = [char.name for char in info_2.npcs]
    print(npcs)
    if callback.message.text in npcs:
        await callback.message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                                      reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.npcs:
            if callback.message.text == end.name:
                data = f"setting='{info_2.setting}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='image2.png')
                file = FSInputFile('image2.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await callback.message.answer_photo(file, caption=ans,
                                                    reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                                    parse_mode=ParseMode.HTML)
    else:
        # print('none')
        await callback.message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                                      parse_mode=ParseMode.HTML)
        return npc_sending
    await state.clear()


# <---------------------------------------------------------------------->


class EnemyState(StatesGroup):
    waiting_enemy = State()


@router.callback_query(F.data == "enemies")
async def enemies(callback: types.CallbackQuery, state: FSMContext):
    ans = ""
    for end in info_2.enemies:
        ans += f"|<b>{end.name}</b> ({end.type})\n {end.description}\n\n"
    ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"
    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()
    await state.set_state(EnemyState.waiting_enemy)


@router.message(EnemyState.waiting_enemy, F.text)
async def enemy_sending(message: types.Message, state: FSMContext):
    enemies = [char.name for char in info_2.enemies]
    print(enemies)
    if message.text in enemies:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.enemies:
            if message.text == end.name:
                data = f"setting='{info_2.setting}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='image3.png')
                file = FSInputFile('image3.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await message.answer_photo(file, caption=ans, reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                           parse_mode=ParseMode.HTML)
    else:
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return enemy_sending
    await state.clear()


# <---------------------------------------------------------------------->


class BH_State(StatesGroup):
    waiting_bh = State()


@router.callback_query(F.data == "bosses_heroes")
async def bosses_heroes(callback: types.CallbackQuery, state: FSMContext):
    ans = ""
    for end in info_2.bosses_heroes:
        ans += f"|<b>{end.name}</b> ({end.type})\n {end.description}\n\n"
    ans += f"<b>Если вы хотите увидеть более подробную информацию о персонаже, а также его изображение, напишите <i>имя</i> персонажа</b>\n"
    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()
    await state.set_state(BH_State.waiting_bh)


@router.message(BH_State.waiting_bh, F.text)
async def bh_sending(message: types.Message, state: FSMContext):
    bh = [char.name for char in info_2.bosses_heroes]
    print(bh)
    if message.text in bh:
        await message.answer('<i>Начали генирировать!</i> Подождите 10-15 секунд',
                             reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
        for end in info_2.enemies:
            if message.text == end.name:
                data = f"setting='{info_2.setting}' name='{end.name}', description='{end.description}'"
                kand_input = await Requestor.get_request(RecommendationsAC(
                    phrases_indication='при написании фраз основываться по стилистике на параметры personality и description. Также фраза должна писаться в вот таких скобках «...»'),
                                                         data)
                print(kand_input)
                await generate(style='ANIME', width=1024, height=1024,
                               query=f"{kand_input.kandinsky_appearance}. Stylized: stained glass, watercolor.",
                               file_name='image4.png')
                file = FSInputFile('image4.png')
                ans = f"<b>{kand_input.name}</b> ({kand_input.type}|{kand_input.gender})\n\n"
                ans += f"{kand_input.appearance}\n\n"
                ans += f"<b>Фразы:</b>\n"
                for phr in kand_input.phrases:
                    ans += f"-<i>{phr.theme}</i>. {phr.phrase}\n\n"
                await message.answer_photo(file, caption=ans, reply_markup=keyboards.KeyboardBackMoreInfoWithoutEdit(),
                                           parse_mode=ParseMode.HTML)
    else:
        await message.answer("Такого персонажа нет", reply_markup=keyboards.KeyboardBackMoreInfo(),
                             parse_mode=ParseMode.HTML)
        return bh_sending
    await state.clear()


# <---------------------------------------------------------------------->


async def more_info(callback: types.CallbackQuery):
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
    ans += f"|<b>Аудиовизуальное сопровождение</b>\n {info.ambient}\n\n" \
           f"|<b>Количество локаций</b>\n {info.location_number}\n\n"
    ans += "|Причины игры\n"
    for end in info.purpose_game:
        ans += f"-<i>{end.type}</i>. {end.justification}\n"

    await callback.message.edit_text(ans, reply_markup=keyboards.KeyboardBackMoreInfo(), parse_mode=ParseMode.HTML)
    await callback.answer()


def register_info_handler(dp: Dispatcher):
    dp.callback_query.register(make_a_choice, F.data == "data")
    dp.callback_query.register(checking_if_ready, F.data == "check_m")
    dp.callback_query.register(choosing_type_survey, F.data == "open")
    dp.callback_query.register(more_info, F.data == "precisely")
    dp.callback_query.register(plot, F.data == "plot")
    # dp.callback_query.register(locations, F.data == "locations")
    # dp.callback_query.register(npcs, F.data == "npcs")
    # dp.callback_query.register(enemies, F.data == "enemies")
    # dp.callback_query.register(bosses_heroes, F.data == "bosses_heroes")
    dp.callback_query.register(beginning, F.data == "beginning")
    dp.callback_query.register(center, F.data == "center")
    dp.callback_query.register(ending, F.data == "ending")
