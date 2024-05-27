import requests
import base64
import time
from random import randint
from aiogram import Dispatcher, Bot, types ,executor
from config import TELEGRAM_TOKEN, TOKEN


bot = Bot(token= TELEGRAM_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.answer('Привет!')

@dp.message_handler()
async def analize_massage(massage: types.Message):
    response_text = await get_response(massage.text)
    await massage.text(f' : {response_text}')
    await massage.text('')
    try:
        image_data = get_response(massage.text)
        await massage.reply()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)


