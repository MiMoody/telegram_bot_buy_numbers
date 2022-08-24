from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_1 = KeyboardButton(text = 'Номер', callback_data = "products")
button_2 = KeyboardButton('Пока! 👋')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
main_kb.add(button_1)
# main_kb.add(button_2)

product_kb = InlineKeyboardMarkup(row_width = 1)
product_btn_1 = InlineKeyboardButton(text = "Купить номер", callback_data = "buy_token")
product_btn_2 = InlineKeyboardButton(text = "Мой номер", callback_data = "my_number")
product_kb.insert(product_btn_1)
product_kb.insert(product_btn_2)