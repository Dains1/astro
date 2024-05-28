import requests
import base64
import time
from random import randint
from aiogram import Bot, Dispatcher, types, executor
from config import TELEGRAM_TOKEN, TOKENN, TOKEN

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
                "text": "ты помогаешь неросети генерировать картинки делая более подробный промт"
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
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    cansul = result['result']['alternatives'][0]['message']['text']
    return cansul

def generate_image(prompt_text):
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
    response = requests.post(url=url, headers=headers, json=prompt)
    result = response.json()
    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(operation_url, headers=headers)
        operation_result = operation_response.json()
        print(operation_result)
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            time.sleep(5)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)