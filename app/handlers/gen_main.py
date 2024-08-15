import sqlite3, keyboards
from typing import Optional
from aiogram import Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from KandinskyAPI import FusionBrainApi, ApiApi

conn = sqlite3.connect("database/databasetg.db")
cursor = conn.cursor()
dp = Dispatcher()
router = Router()


Kandinsky = FusionBrainApi(ApiApi('95FBFE1721C1103FF0C83FDC27C5261E', 'AA7978AFECC4F210E7B4BD9FE854D4B3'))


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
            max_time=120
        )
    except ValueError as e:
        print(f"Error:\t{e}")
    else:
        with open(file_name, "wb") as f:
            f.write(result)
        print("Done!")


class PromptState(StatesGroup):
    waiting_prompt = State()


@router.callback_query(F.data == "gen_main")
async def ask_prompt(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.edit_text("Напишите ваш запрос", reply_markup=keyboards.KeyboardBack())
    await state.set_state(PromptState.waiting_prompt)


@router.message(PromptState.waiting_prompt, F.text)
async def genZ(message:types.Message, state:FSMContext):
    await message.answer("Мы приняли ваш запрос. Ожидайте")
    # try:
    await generate(style='ANIME', width=1024, height=1024,
                         query=message.text,
                         file_name='image.png')
    file = FSInputFile('image.png')

    await message.answer_photo(file, caption=f"{message.text}")
    await message.answer("Готово!", reply_markup=keyboards.KeyboardBack())
    await state.clear()
    # except Kandinsky.:
    #     await message.edit_text("К сожалению, по данному запросу не возможно сгенерировать картинку. Попробуйте еще раз", reply_markup=keyboards.KeyboardBack())
    #     await state.clear()


