from aiogram import Dispatcher, Bot, types ,executor
from config import TELEGRAM_TOKEN
from hhtr.obo1 import generate_image
from hhtr.obo3 import get_response2, get_response3


bot = Bot(token= TELEGRAM_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('/рассказчик')
    button2 = types.KeyboardButton('/помощник')
    button3 = types.KeyboardButton('/генерация')
    keyboard.add(button1, button2, button3)
    await message.reply("Выберите, кем вы хотите, чтобы я был:", reply_markup=keyboard)

@dp.message_handler(commands=['рассказчик'])
async def рассказчик_command(message: types.Message):
    user_text = message.text.replace('/рассказчик ')
    response_text = await get_response2(user_text)
    await message.reply(response_text)

@dp.message_handler(commands=['помощник'])
async def помощник_command(message: types.Message):
    user_text = message.text.replace('/помощник ')
    response_text = await get_response3(user_text)
    await message.reply(response_text)

@dp.message_handler(commands=['генерация'])
async def генерация_command(message: types.Message):
    user_text = message.text.replace('/генерация ')
    await message.reply('Идёт генерация изображения')
    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)


