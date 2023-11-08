BOT_TOKEN = 
PAYMENT_TOKEN =

from aiogram import Bot, Dispatcher, executor, types
        import payment

        BOT_TOKEN = 
        PAYMENT_TOKEN = 

        bot = Bot(payment.BOT_TOKEN)
        dp = Dispatcher(bot)

        async def pay(message: types.message):
            await bot.send_invoice(message.chat.id, 'Купить стикеры',
                                   'Для покупки перейдите по ссылке и нажмите кнопку после покупки', 'invoice',
                                   payment.PAYMENT_TOKEN, 'RUB', [types.labeled_price('Купить стикеры', 3.5 * 100)])

        @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
        async def success(message: types.message):
            await message.answer(f'Оплата заказа {message.successful_payment.order_info} произошла!')