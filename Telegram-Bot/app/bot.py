from aiogram import executor
from app.setup import dp


if __name__ == "__main__":
    from app.handlers import dp
    executor.start_polling(dispatcher=dp, skip_updates=True)
