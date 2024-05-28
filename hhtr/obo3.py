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
            "temperature": 1,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты - рассказчик, рассказываешь истории на любую тему, но не превышающие 30 предложений"
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

async def get_response3(message_text):
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
                "text": "Ты - помогаешь людям находить по их предпочтениям игры, аниме и сериалы"
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