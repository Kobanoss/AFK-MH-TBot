from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from get_data import load_classic_data, load_data
from setup import DEPARTMENT_NAME, BOT_NAME
from states import States


# `start` handler
@dp.message_handler(state=None)
async def start(message: types.Message, keyboard=None):
    await States.question.set()
    await message.answer(
        f"Здравствуйте, {message.from_user.username}, "
        f"вы обратились в службу психологической помощи {DEPARTMENT_NAME}.\n"
        f"Вас приветсвует чат-бот {BOT_NAME}.")
    await message.answer("Постарайтесь рассказать нам о вашей проблеме в одном сообщении, "
                         "количество слов неограничено.")


async def selector(message: types.Message):
    ans_list = await load_data(message.text)
    buttons = [types.InlineKeyboardButton(text=ans, callback_data="ThemeSelected") for ans in ans_list]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons, types.InlineKeyboardButton(text='Нет соотвествующей темы', callback_data='ThemeClassic'))

    await message.bot.send_message(message.chat.id,
                                   f"{message.from_user.username}, по вашему вопросу мы подготовили следующие темы, "
                                   f"если не одна из них не подходит, выберите "
                                   f"'Нет соотвествующей темы'",
                                   reply_markup=keyboard)
    await States.selecting.set()


@dp.message_handler(state=States.question)
async def get_question(message: types.Message, state: FSMContext, keyboard=None):
    await States.wait.set()
    await message.answer("Благодарим за то, что поделились вашей проблемой, ожидайте результата обработки!")

    if 'суицид' in message.text.split():  # TODO: more
        await States.danger.set()
        await message.answer("Ваше текущее состояние достаточно критично, рекомендуем срочно обратиться к специалистам")
        await message.answer("Контакты: ...")
        buttons = [types.InlineKeyboardButton(text='Да', callback_data="Continue"),
                   types.InlineKeyboardButton(text='Нет', callback_data="Stop")]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.bot.send_message(message.chat.id,
                                       f"Вы желаете продолжить первичную консультацию?",
                                       reply_markup=keyboard)
        return

    await selector(message)
    # Добавление стандартных вариантов в случае отсуствия предложений + СПИСОК ПРОБЛЕМ
    # Обработка критичных ситуаций: суицид, шизофрения обострение, ОКР, Диполяр + СПИСОК БОЛЕЗНЕЙ
    #


@dp.callback_query_handler(lambda callback: True, state=States.danger)
async def select_button(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Continue":
        await selector(callback.message)
    else:
        await dp.bot.send_message(callback.message.chat.id, "Благодарим, что обратились к нам за помощью!",
                                  reply_markup=None)
        await state.finish()


@dp.callback_query_handler(lambda callback: True, state=States.selecting)
async def select_button(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "ThemeSelected":
        await dp.bot.send_message(callback.message.chat.id,
                                  "Видеоматериалы по вашей теме:")
        await dp.bot.send_message(callback.message.chat.id,
                                  "https://www.youtube.com/watch?v=hpbtZgOwj0M&feature=youtu.be")
        await dp.bot.send_message(callback.message.chat.id, "Ожидается новый видеоматериал позднее...")
        await dp.bot.send_message(callback.message.chat.id,
                                  "Рекомендуем помимо просмотра видео,"
                                  "также пройти ряд тестов, связанных с вашей темой:\n"
                                  "https://psytests.org/depr/mddds.html\n"
                                  "Ожидаются новые тесты позднее...")

        await dp.bot.send_message(callback.message.chat.id, "Благодарим вас за обращение!")
        await state.finish()
    elif callback.data == "ThemeClassic":

        ans_list = await load_classic_data(callback.message.text)
        buttons = [types.InlineKeyboardButton(text=ans, callback_data="ThemeSelected") for ans in ans_list]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons, types.InlineKeyboardButton(text='Нет соотвествующей темы', callback_data='Stop'))

        await dp.bot.send_message(callback.message.chat.id, "Жаль, что мы не смогли обработать ваш вопрос."
                                                            "Выберите проблему из предложенных",
                                  reply_markup=keyboard)

    elif callback.data == "Stop":
        await dp.bot.send_message(callback.message.chat.id, "Благодарим вас за обращение!\n"
                                                            "Попробуйте переформулировать вопрос и обратиться вновь")
        await state.finish()


@dp.message_handler(state=States.danger)
async def select_text(message: types.Message):
    await selector(message)


@dp.message_handler(state=States.selecting)
async def select_text(message: types.Message):
    print("message_get")
    await message.bot.send_message(message.chat.id, "Выберите пункт меню")
