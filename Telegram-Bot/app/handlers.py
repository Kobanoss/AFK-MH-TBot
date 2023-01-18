from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dp
from app.get_data import load_data
from app.setup import DEPARTMENT_NAME
from app.states import States


# `start` handler
@dp.message_handler(state=None)
async def start(message: types.Message, keyboard=None):
    await States.question.set()
    await message.answer(
        f"Здравствуйте, {message.from_user.username}, "
        f"вы обратились в службу психологической помощи {DEPARTMENT_NAME}.")
    await message.answer("Постарайтесь рассказать нам о вашей проблеме в одном сообщении, "
                         "количество слов неограничено.")


@dp.message_handler(state=States.question)
async def get_question(message: types.Message, state: FSMContext, keyboard=None):
    await States.wait.set()
    await message.answer("Благодарим за то, что поделились вашей проблемой, ожидайте результата обработки!")

    ans_list = await load_data(message.text)
    buttons = [types.InlineKeyboardButton(text=ans, callback_data="Selected") for ans in ans_list]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons, types.InlineKeyboardButton(text='Нет соотвествующей темы', callback_data='Refused'))

    await message.bot.send_message(message.chat.id,
                                   f"{message.from_user.username}, по вашему вопросу мы подготовили следующие темы, "
                                   f"если не одна из них не подходит, выберите "
                                   f"'Нет соотвествующей темы'",
                                   reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda callback: True)
async def select_button(callback: types.CallbackQuery,  state: FSMContext):
    print("Callback get")
    if callback.data == "Selected":
        await dp.bot.send_message(callback.message.chat.id, "В будущем тут будут ссылки тесты, видеоматериал и "
                                                            "сведения для записи к специалистам")
        await dp.bot.send_message(callback.message.chat.id, "При желании вы можете ввести новое обращение, "
                                                            "оно также будет обработано в ближайшее время")
        await States.question.set()
    else:
        await dp.bot.send_message(callback.message.chat.id, "Жаль, что мы не смогли обработать ваш вопрос, "
                                                            "попытайтесь переформулировать его и ввести вновь",
                                  reply_markup=None)
        await States.question.set()


@dp.message_handler(state=States.selecting)
async def select_text(message: types.Message):
    print("message_get")
    pass
