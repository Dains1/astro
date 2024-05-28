import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import base64
from random import randint
from config import TELEGRAM_TOKEN, TOKENN, TOKEN
from aiogram import Bot

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def get_response1(message_text):
    prompt = {
        "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "system",
                "text": "ты помогаешь нейросети генерировать картинки, делая более подробный промт"
            },
            {
                "role": "user",
                "text": message_text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {TOKENN}"
    }
    response = await asyncio.to_thread(requests.post, url, headers=headers, json=prompt)
    result = response.json()
    cansul = result['result']['alternatives'][0]['message']['text']
    return cansul

async def generate_image(prompt_text):
    prompt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
            "seed": randint(1, 1000000000)
        },
        "messages": [
            {
                "weight": 1,
                "text": prompt_text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {TOKEN}"
    }
    response = await asyncio.to_thread(requests.post, url, headers=headers, json=prompt)
    result = response.json()
    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = await asyncio.to_thread(requests.get, operation_url, headers=headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            await asyncio.sleep(5)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)