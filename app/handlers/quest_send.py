# import sqlite3, googleapiclient, httplib2, asyncio, keyboards, pandas as pd
# from aiogram import F, Router, types, Dispatcher
# import googleapiclient.discovery
# from aiogram.filters import ExceptionTypeFilter, state, Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import FSInputFile
# from aiogram.fsm.state import StatesGroup, State
# from oauth2client.service_account import ServiceAccountCredentials
# from GPTAPI import *
# from aiogram.enums import ParseMode
# from openai import RateLimitError
# from app.handlers.get_info import *
#
# from app.handlers.add_players import AliasState
# from app.handlers.gen_main import generate
# from aiohttp.client_exceptions import ClientConnectionError
# #
# client = AsyncOpenAI(
#     api_key='sk-YjPnOdcxcW4myaU5on3f6LcIStlhszBZBhPsfwIXXGT3BlbkFJU4fU2uZ2mkhuAUQ0U1dRx5EeXKLxPPy9ahHmc0a7EA')
#
# router = Router()
# conn = sqlite3.connect("database/databasetg.db")
# cursor = conn.cursor()
# Requestor = RequestAPI(client)
#
# global info_q
# global info_q_2
#
#
# def get_service_sacc():
#     scopes = ['https://www.googleapis.com/auth/spreadsheets']
#     creds_service = ServiceAccountCredentials.from_json_keyfile_name('dnd.json', scopes).authorize(httplib2.Http())
#     return googleapiclient.discovery.build('sheets', 'v4', http=creds_service)
#
# #
# async def make_a_choice(callback: types.CallbackQuery):
#     await callback.message.edit_text("Выбирайте", reply_markup=keyboards.KeyboardQuestGen())
#     await callback.answer()
#
# #
# async def checking_if_ready(callback: types.CallbackQuery):
#     global info_q
#     global info_q_2
#     global info
#
#     info_q = info
#     resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
#                                                           range="ответы_игры!A2:E500").execute()
#
#     pd.DataFrame(resp['values']).to_csv('res_q.csv')
#
#     res_master = cursor.execute("SELECT master FROM men")
#     users_master = [x[0] for x in res_master.fetchall()]
#
#     res_user = cursor.execute("SELECT user FROM men")
#     users = [x[0] for x in res_user.fetchall()]
#
#     myusers = [users[i] for i in range(len(users)) if users_master[i] == callback.from_user.username]
#     print(myusers)
#
#     answer = []
#     for ans in resp['values']:
#         if len(ans) != 0:
#             if ans[-1] in myusers:
#                 print(ans[-1])
#                 answer.append(ans)
#     length = len(answer)
#     print(length, resp['values'])
#
#     res_master = cursor.execute("SELECT master FROM men")
#     users_master = [x[0] for x in res_master.fetchall()]
#
#     k = 0
#
#     for master in users_master:
#         if master == callback.from_user.username:
#             k += 1
#
#     if k != length:
#         await callback.message.edit_text(
#             "К сожалению, еще <b>не все игроки</b> закончили проходить опрос\nВозвращайтесь попозже!",
#             reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
#     else:
#         await callback.message.edit_text(
#             "Мы <b>получили</b> данные! Подождите <i>20 секунд</i>, идет обработка ответов", parse_mode=ParseMode.HTML)
#         try:
#             # info_q = pd.read_csv('res_q.csv').to_string()
#             # info_q = await Requestor.get_request(AnalyzeBF(), info_q)
#             await asyncio.sleep(7)
#             # print("DONE info")
#
#             info_q_2 = await Requestor.get_request(RecommendationsQQ(), str(info_q))
#             await asyncio.sleep(7)
#             print("DONE info_2_й")
#
#             print(info_q_2)
#             await callback.message.edit_text("<b>Ответы готовы!</b>\nПройдите назад и нажмите 🚪Открыть",
#                                              reply_markup=keyboards.KeyboardBackGetInfo(), parse_mode=ParseMode.HTML)
#         except (RateLimitError, NameError) as e:
#             print(e)
#             await callback.message.edit_text("🛑К сожалению, произошла ошибка.\n Попробуйте сперва сгенерировать информацию основной партии. Если это не помогло, то вероятно проблема со стороны библиотеки OpenAI",reply_markup=keyboards.KeyboardBack(), parse_mode=ParseMode.HTML)
#
#
#
#
# #
# def register_quest_handler(dp: Dispatcher):
#     dp.callback_query.register(make_a_choice, F.data == "quest_send")
#     dp.callback_query.register(checking_if_ready, F.data == "check_quest")
