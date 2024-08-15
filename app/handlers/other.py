from aiogram import F, types, Dispatcher
import keyboards


async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardM())


async def back_get_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardCheck())


async def back_more_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardInfo())


async def back_more_info_we(callback: types.CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.KeyboardInfo())


async def back_plot_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboards.KeyboardStoryline())




def register_other_handler(dp: Dispatcher):
    dp.callback_query.register(back, F.data=="back")
    dp.callback_query.register(back_get_info, F.data == "back_get_info")
    dp.callback_query.register(back_plot_info, F.data == "back_plot_info")
    dp.callback_query.register(back_more_info, F.data == "back_more_info")
    dp.callback_query.register(back_more_info_we, F.data == "back_more_info_we")



#AIzaSyAu5kb_xcc0Rqof0KNgFf_-K6rR-kMxso0
