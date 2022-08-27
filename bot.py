import os
from dotenv import find_dotenv, load_dotenv
from coin_parser import CoinlayerParser as clp
from aiogram import Bot, Dispatcher, executor, types


load_dotenv(find_dotenv())
API_ACCESS_KEY = os.getenv('API_ACCESS_KEY')
TOKEN = os.getenv('TOKEN')
BASE_URL = 'http://api.coinlayer.com/'

coin_parser = clp(API_ACCESS_KEY, BASE_URL)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.answer('Hi, i can show you live/historical cryptocurrency rates')

@dp.message_handler(commands='live')
async def get_live_rates(message: types.Message):
    data = coin_parser.get_live_data()


@dp.message_handler(commands='historical')
async def get_historical_rates(message: types.Message):
    date = message.text.split(' ')[1]
    data = coin_parser.get_historical_data(date)
    if isinstance(data, str):
        await message.answer(data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
