from aiogram import Bot
from hhtr.obo1 import generate_image
from hhtr.obo3 import get_response2, get_response3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import io
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TELEGRAM_TOKEN


bot = Bot(token= TELEGRAM_TOKEN)
dp = Dispatcher(bot)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

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
    await message.reply("Введите тему для рассказа:")
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("рассказчик_state")

@dp.message_handler(state="рассказчик_state")
async def рассказчик_state(message: types.Message):
    user_text = message.text
    response_text = await get_response2(user_text)
    await message.reply(response_text)
    await dp.current_state(user=message.from_user.id).finish()

@dp.message_handler(commands=['помощник'])
async def помощник_command(message: types.Message):
    await message.reply("Введите тему для поиска:")
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("помощник_state")

@dp.message_handler(state="помощник_state")
async def помощник_state(message: types.Message):
    user_text = message.text
    response_text = await get_response3(user_text)
    await message.reply(response_text)
    await dp.current_state(user=message.from_user.id).finish()

@dp.message_handler(commands=['генерация'])
async def генерация_command(message: types.Message):
    await message.reply("Введите тему для генерации:")
    await dp.current_state(user=message.from_user.id).set_state("генерация_state")

@dp.message_handler(state="генерация_state")
async def генерация_state(message: types.Message):
    user_text = message.text
    await message.reply('Идёт генерация изображения')
    try:
        image_bytes = await generate_image(user_text)
        image = types.InputFile(io.BytesIO(image_bytes), filename='generated_image.png')
        await message.reply_photo(photo=image)
    except Exception as e:
        await message.reply(f'Произошла ошибка: {e}')
    await dp.current_state(user=message.from_user.id).finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)


