import requests
from aiogram import Bot, Dispatcher, types, executor
from config import TELEGRAM_TOKEN, TOKENN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def get_response2(message_text):
    prompt = {
        "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты -Виртуальный собеседник на любую тему, но кратко, 2-3 предложения"
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
    return result['result']['alternatives'][0]['message']['text']



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)