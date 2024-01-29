import logging
import os
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = "6731815793:AAGL8Fv_NR8DLtnYVK9nbf2KvZzhqikD25Y"

# Конфігуруємо логи
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо бот та дизпатчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# Створюємо хендлер для обробки стартового повідомлення.
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    text = 'Привіт! Почнімо працювати.'
    await message.answer(text=text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
