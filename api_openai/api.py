import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def openai_query(response):
    prompt = (
        "Тебе звати 'Бот помічник' представляйся в кожному повідомленні. "
        "Ти дуже досвідченний аналітик, потрібно відповісти на відзив людини "
        "подякувати їй за нього та дати коротку але честну відповідь. В повідомлені є локація, вказуй її ")

    text = (f"Локація: {response.get('location')}, "
            f"Враження кліента: {response.get('feedback')}, "
            f"Коментар кліента: {response.get('comment')}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
    )
    return response.choices[0].message.content
