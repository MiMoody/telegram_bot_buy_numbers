import datetime
import logging
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
import keyboards as kb
from models.main import User
from json_db.utils import JsonStruct

YOO_TOKEN = "381764678:TEST:41571" 
BOT_TOKEN = "2131731114:AAFZIzni5g3zWJsiiOCv7PcuLLjHDqqjVgI"

# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Часовой пояс
TZINFO_MOSCOW = datetime.timezone(datetime.timedelta(hours=3), 'МСК')

MAX_NUMBERS = 1500

@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    await message.answer("Стартуем...", reply_markup = kb.main_kb)

# Хэндлер на команду Купить номер
@dp.message_handler(Text(equals = "Номер"))
async def numbers(message: types.Message):
    await message.answer(text="Номерки", reply_markup=kb.product_kb)
    
@dp.callback_query_handler(text="my_number")
async def get_number(call:types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    user = User.get_by_id(str(call.from_user.id))
    if user:
        await bot.send_message(call.message.chat.id, text = f"Ваш номер: {user['individual_number']}", reply_markup = kb.main_kb)
        return 
    await bot.send_message(call.message.chat.id, text = f"Для начала нужно купить номер!", reply_markup = kb.main_kb)
    
@dp.callback_query_handler(text="buy_token")
async def get_products(call:types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    individual_numbers:list = JsonStruct.get("individual_numbers")
    if User.get_by_id(str(call.from_user.id)):
        await bot.send_message(call.message.chat.id, text = f"Вы уже получили номерок!", reply_markup = kb.main_kb)
        return
    elif MAX_NUMBERS in individual_numbers: 
        await bot.send_message(call.message.chat.id, text = f"Номерки закончились!", reply_markup = kb.main_kb)
        return
    else:
        await bot.send_invoice(chat_id= call.from_user.id,
                               title="Покупка номера",
                               description="Покупка индивидуального номера для участия в конкурсе",
                               payload="individual_number",
                               provider_token=YOO_TOKEN,
                               currency="RUB",
                               start_parameter="in_number",
                               prices=[{"label":"Руб", "amount":15000}])

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "individual_number":
        payment = {
            "currency": message.successful_payment.currency,
            "total_amount": message.successful_payment.total_amount,
            "invoice_payload": message.successful_payment.invoice_payload,
            "datetime_payment":f'{datetime.datetime.now(TZINFO_MOSCOW):%Y-%m-%d %H:%M:%S}',
            "shipping_option_id": message.successful_payment.shipping_option_id,
            "order_info": message.successful_payment.order_info,
            "telegram_payment_charge_id": message.successful_payment.telegram_payment_charge_id,
            "provider_payment_charge_id": message.successful_payment.provider_payment_charge_id
        }
        individual_numbers:list = JsonStruct.get("individual_numbers")
        number =  individual_numbers[-1] + 1 if individual_numbers  else 1
        individual_numbers.append(number)
        JsonStruct.save("individual_numbers", individual_numbers)
        User.create(user_id = message.from_user.id,
                    username = message.from_user.username,
                    first_name = message.from_user.first_name,
                    last_name = message.from_user.last_name,
                    payment = payment,
                    individual_number = number
                    )
        await bot.send_message(message.chat.id, text = f"Ваш индивидуальный номер: {number}", reply_markup = kb.main_kb)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)