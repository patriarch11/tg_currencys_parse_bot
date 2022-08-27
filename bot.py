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
    if message.text == '/start':
        await message.answer('Hi, i can show you live/historical cryptocurrency rates')
    if message.text == '/help':
        await message.answer('For get live rate currency use /live currency\n'
                             'Example: /live usdt\n'
                             'For get all live rates use /live all\n'
                             'Example: /live all\n'
                             'For get historical rate use /historical YYYY-MM-DD currency\n'
                             'Example: /historical 2020-12-01 btc\n'
                             'For get all historical rates use /historical YYYY-MM-DD all\n'
                             'Example: /historical 2020-12-01 all')


@dp.message_handler(commands='live')
async def get_live_rates(message: types.Message):
    data = coin_parser.get_live_data()
    currency = message.text.split(' ')[1].upper()
    print(data)
    if currency == 'ALL':
        with open('all.txt', 'w') as file:
            data_gen = (f'{key} --- {value} USD' for key, value in data['rates'].items())
            for i in data_gen:
                file.writelines(f'{i}\n')
        await message.reply_document(open('all.txt', 'rb'))
    else:
        await message.answer(f'{currency} --- {data["rates"].get(currency)} USD')


@dp.message_handler(commands='historical')
async def get_historical_rates(message: types.Message):
    date = message.text.split(' ')[1]
    currency = message.text.split(' ')[2].upper()
    data = coin_parser.get_historical_data(date)
    if isinstance(data, str):
        await message.answer(data)
    if currency == 'ALL':
        with open('all_historical.txt', 'w') as file:
            data_gen = (f'{key} --- {value} USD' for key, value in data['rates'].items())
            for i in data_gen:
                file.writelines(f'{i}\n')
        await message.reply_document(open('all_historical.txt', 'rb'))
    else:
        await message.answer(f'{date}\n{currency} --- {data["rates"].get(currency)} USD')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
