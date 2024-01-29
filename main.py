import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api_openai import api

import keyboards as kb

BOT_TOKEN = os.getenv('KEY_BOT')

# Конфігуруємо логи
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо бот та дизпатчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class User(StatesGroup):
    location = State()
    feedback = State()
    comment = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    text = 'Привіт! Почнімо працювати?'
    await message.answer(text=text, reply_markup=kb.start_keyboard())


@dp.message_handler(regexp='почнемо')
async def start(message: types.Message) -> None:
    await User.location.set()
    await message.answer(text="Чудово!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='Оберіть локацію!', reply_markup=kb.markup_menu_locations())


@dp.message_handler(state=User.location)
async def select_location(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['location'] = message.text
    await state.update_data(feedback=message.text)
    await message.answer('Ваше враження?', reply_markup=kb.markup_check_list())
    await User.next()


@dp.message_handler(state=User.feedback)
async def select_feedback(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['feedback'] = message.text
    await state.update_data(feedback=message.text)
    await message.answer(text='Дякуюємо!')
    await message.answer(text="Залишіть будь-ласка коментар!", reply_markup=types.ReplyKeyboardRemove())
    await User.next()


@dp.message_handler(state=User.comment)
async def send_comment(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='Дякуємо за коментар!', reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:
        data['comment'] = message.text
    await message.answer('Будь-ласка відправте фотографію!')
    await User.next()


@dp.message_handler(lambda message: not message.photo, state=User.photo)
async def add_photo_check(message: types.Message) -> None:
    await message.answer('Це не фотографія!')


@dp.message_handler(content_types=['photo'], state=User.photo)
async def add_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.answer('Відгук залишено!')
    text = await api.openai_query(state)
    await state.finish()
    await message.answer('Аналіз вашого відгуку.')
    await message.answer(text=text)


@dp.message_handler()
async def any_message(message: types.Message) -> None:
    await message.answer(text='Я Вас не розумію..')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
