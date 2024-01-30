import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards as kb
from api_openai import api
from utils import clean_state, add_to_database

# Bot token fron BotFather telegram
BOT_TOKEN = os.getenv('KEY_BOT')

# Configure loging
logging.basicConfig(level=logging.INFO)

# Initial bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Set states for Finite State Machine
class User(StatesGroup):
    location = State()
    feedback = State()
    comment = State()
    photo = State()


# Start handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.answer(text='Привіт! Почнімо працювати?', reply_markup=kb.start_keyboard())


# Message for start
@dp.message_handler(regexp='почнемо')
async def start(message: types.Message) -> None:
    await User.location.set()  # Set start Finite State Machine
    await message.answer(text="Чудово!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='Оберіть локацію!', reply_markup=kb.keyboard_menu_locations())


# Get location
@dp.message_handler(state=User.location)
async def select_location(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:  # Set data in Finite State Machine
        data['location'] = message.text
    await message.answer('Ваше враження?', reply_markup=kb.keyboard_check_list())
    await User.next()  # Continue next state


# Get message feedback
@dp.message_handler(state=User.feedback)
async def select_feedback(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:  # Set data in Finite State Machine
        data['feedback'] = message.text
    await message.answer(text='Дякуюємо!')
    await message.answer(text="Залишіть будь ласка коментар!", reply_markup=types.ReplyKeyboardRemove())
    await User.next()  # Continue next state


# Get comment
@dp.message_handler(state=User.comment)
async def send_comment(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='Дякуємо за коментар!', reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:  # Set data in Finite State Machine
        data['comment'] = message.text
    await message.answer('Будь-ласка відправте фотографію!')
    await User.next()  # Continue next state


# Handler if not a photo is sent
@dp.message_handler(lambda message: not message.photo, state=User.photo)
async def add_photo_check(message: types.Message) -> None:
    await message.answer('Це не фотографія!')


# Get photo
@dp.message_handler(content_types=['photo'], state=User.photo)
async def add_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:  # Set data in Finite State Machine
        data['photo'] = message.photo[0].file_id
    await message.answer('Відгук залишено!')
    await message.answer('Формується аналіз, це може зайняти кілька хвилин.')
    clean_data: dict = await clean_state(state)  # Cleaning data from Finite State Machine
    text_openai: [str | None] = None
    try:
        # Analyzing text with openAI
        text_openai = await api.openai_query(clean_data)
        await message.answer('Аналіз вашого відгуку.')
        await message.answer_photo(photo=clean_data.get('photo'), caption=text_openai)

    except Exception as ex:
        await message.answer(text='Виникла помилка в аналізі відгуку..')
        logging.error(ex)

    finally:
        await add_to_database(user_id=message.from_user.id, clean_data=clean_data,
                              openai_response=text_openai)  # Add feedback to database
        await state.finish()  # Finish Finite State Machine

    await message.answer(text='Бажаєте залишити ще один відгук?', reply_markup=kb.start_keyboard())


# Handler for any message because we use a linear strategy to get feedback
@dp.message_handler()
async def any_message(message: types.Message) -> None:
    await message.answer(text='Я Вас не розумію..')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
