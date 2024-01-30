# OPENAI Api File
import logging
import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Request to openAi
async def openai_query(response: dict) -> str:
    # Prompt of artificial intelligence behavior
    prompt = (
        "Ваше ім'я - 'Бот-помічник', представляйтеся в кожному повідомленні. "
        "Ви дуже досвідчений аналітик, вам потрібно проаналізувати відгук людини"
        "подякувати їй за нього та дати коротку але честну відповідь. В повідомлені є локація по цій зроби аналіз, "
        "опиши настрій відзиву, чи все добре с локацією, проаналізуй чи є рекомендації в відгукі та напиши їх в "
        "кінці повідомлення"
    )

    # Prompt of user
    text = (f"Локація: {response.get('location')}, "
            f"Враження кліента: {response.get('feedback')}, "
            f"Коментар кліента: {response.get('comment')}")
    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Set model gpt
            messages=[  # Set prompts
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ]
        )
        return response.choices[0].message.content  # return response
    except Exception as ex:
        # Print error
        logging.error(ex)
        raise Exception
