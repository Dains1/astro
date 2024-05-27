import requests
from aiogram import  Bot,  Dispatcher, types, executor
from config import TELEGRAM_TOKEN, TOKENN


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)



async def get_response(message_text):
    prompt = {
        "modelUri": "gpt://b1gf5pfjsd0phsrq2ldh/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "придумай детальное описание для картины какая погода, место, время, и так далее, из 2-3 предложений"
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
        "Authorization": f"Api-key ${TOKENN}"
    }
    # ${IAM_TOKEN}
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message:types.Message):
    response_text = await get_response(message.text)
    await message.answer(response_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
