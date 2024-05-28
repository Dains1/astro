from aiogram import Dispatcher, Bot, types ,executor
from config import TELEGRAM_TOKEN
from hhtr.obo1 import generate_image
from hhtr.obo3 import get_response2
from hhtr.obo4 import get_response3

bot = Bot(token= TELEGRAM_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.answer('Привет!')

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply('Идёт генерация изображения')
    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')

# @dp.message_handler()
# async def analize_message(message:types.Message):
#     response_text2 = await get_response2(message.text)
#     await message.answer(response_text2)
#
# @dp.message_handler()
# async def analize_message(message:types.Message):
#     response_text3 = await get_response3(message.text)
#     await message.answer(response_text3)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)


