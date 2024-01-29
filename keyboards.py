from aiogram import types


def start_keyboard():
    start_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn = types.KeyboardButton(text='Почнемо!')
    start_kb.add(btn)
    return start_kb


def markup_menu_locations():
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    location_1 = types.KeyboardButton(text="Локація 1")
    location_2 = types.KeyboardButton(text="Локація 2")
    location_3 = types.KeyboardButton(text="Локація 3")
    location_4 = types.KeyboardButton(text="Локація 4")
    location_5 = types.KeyboardButton(text="Локація 5")
    markup.add(location_1, location_2, location_3, location_4, location_5)
    return markup


def markup_check_list():
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Дуже задоволенний!')
    btn2 = types.KeyboardButton(text='Все чисто')
    btn3 = types.KeyboardButton(text='Посередньо')
    btn4 = types.KeyboardButton(text='Погано')
    btn5 = types.KeyboardButton(text='Не рекомендую')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
