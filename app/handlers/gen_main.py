import sqlite3
from utilits import keyboards
from typing import Optional
from aiogram import Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from KandinskyAPI import FusionBrainApi, ApiApi
from aiohttp.client_exceptions import ClientConnectionError
from aiogram.enums import ParseMode
from loguru import logger

conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
logger.info("connected to databasetg.db in gen_main.py")

dp = Dispatcher()
router = Router()


Kandinsky = FusionBrainApi(ApiApi('D5EC5D3E3AEE8388B9AF38C58CE391B7', 'AF5BC121C61198793984DC796FCF6E4C'))
logger.info("Create object Kandinsky, using class FusionBrainApi")

async def generate(
        model: Optional[str] = None,
        style: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        negative_prompt: Optional[str] = None,
        query: Optional[str] = None,
        file_name: str = 'image.png'):
    try:
        result = await Kandinsky.text2image(
            model=model, style=style,
            width=width, height=height,
            negative_prompt=negative_prompt, query=query,
            max_time=240
        )
    except ValueError as e:
        print(f"Error:\t{e}")
    else:
        with open(file_name, "wb") as f:
            f.write(result)
        print("Done!")


class PromptState(StatesGroup):
    waiting_prompt = State()


class PromptStatePlayer(StatesGroup):
    waiting_prompt_player = State()


@router.callback_query(F.data == "gen_main")
async def ask_prompt(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_text("Напишите ваш запрос", reply_markup=keyboards.KeyboardBack())
    await state.set_state(PromptState.waiting_prompt)


@router.message(PromptState.waiting_prompt, F.text)
async def genZ(message:types.Message, state:FSMContext):
    await message.answer("Ваш запрос принят! <i>Ожидайте</i>", parse_mode=ParseMode.HTML)
    try:
        logger.info(f"Begin generating image with caption {message.text}")
        await generate(style='ANIME', width=1024, height=1024,
                             query=message.text,
                             file_name='images/image.png')
        logger.debug("created")
        file = FSInputFile('images/image.png')

        await message.answer_photo(file, caption=f"{message.text}")
        await message.answer("Готово!", reply_markup=keyboards.KeyboardBack())
        logger.success(f"Generated new image in images/image.png with caption: {message.text}")
        await state.clear()
    except (ClientConnectionError, TypeError) as e:
        await message.answer("<b>Произошла ошибка!</b> Попробуйте еще раз", reply_markup=keyboards.KeyboardM(), parse_mode=ParseMode.HTML)
        logger.error(f"{e}")
        return ask_prompt


@router.callback_query(F.data == "gen_main_p")
async def ask_prompt_p(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_text("Напишите ваш запрос")
    await state.set_state(PromptStatePlayer.waiting_prompt_player)


@router.message(PromptStatePlayer.waiting_prompt_player, F.text)
async def genP(message:types.Message, state:FSMContext):
    await message.answer("Ваш запрос принят! <i>Ожидайте</i>", parse_mode=ParseMode.HTML)
    try:
        logger.info(f"Begin generating image with caption {message.text}")

        await generate(style='ANIME', width=1024, height=1024,
                             query=message.text,
                             file_name='images/image_p.png')
        file = FSInputFile('images/image_p.png')

        await message.answer_photo(file, caption=f"{message.text}")
        await message.answer("Готово!", reply_markup=keyboards.KeyboardBackPlayer())
        logger.success(f"Generated new image in images/image_p.png with caption: {message.text}")
        await state.clear()
    except ClientConnectionError as e:
        await message.answer("<b>Произошла ошибка!</b> Попробуйте еще раз", reply_markup=keyboards.KeyboardBackPlayer(), parse_mode=ParseMode.HTML)
        logger.error(f"{e}")
        return ask_prompt_p



