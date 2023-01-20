import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from colorama import Fore

# Enable base logging
logging.basicConfig(level=logging.INFO)
# Bot object
token = getenv('BOT_TOKEN', None)
if token is None:
    print(f'{Fore.RED}No "BOT TOKEN" in the environment!\nExiting!{Fore.RESET}')
    exit(1)

bot = Bot(token=token)

# Dispatcher
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


DEPARTMENT_NAME = 'МГТУ им. Н.Э. Баумана'
BOT_NAME = 'Зигмунд'
