from aiogram import executor
from setup import dp


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dispatcher=dp, skip_updates=True)
