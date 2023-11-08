import telebot
from telebot import types
import sqlite3
with open('setup.SQL', 'r') as sql_file:
    sql_script = sql_file.read()


bot = telebot.TeleBot()

file_id = None
NameID = None

#приветственная кнопка
#альбом
#кнопки
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("<", callback_data="<")
    btn3 = types.InlineKeyboardButton(">", callback_data=">")
    markup.row(btn1, btn3)
    btn4 = types.InlineKeyboardButton('Приложить фото', callback_data='Приложить фото')
    markup.row(btn4)
    photo = open('фото1.png', 'rb')
    bot.send_photo(message.chat.id, photo,'<b>"Eto pizdec"</b>', parse_mode='html', reply_markup=markup)

    def now(call):
        db = sqlite3.connect('obdrocheno.db')
        cursor = db.cursor()

        cursor.execute('SELECT url, comment FROM images')
        cursor.execute('SELECT tg_id FROM users')
        noww = cursor.fetchmany()

        info = ''
        for el in images:
            info += f'Спот №1: {comment} {tg_id} {url}'

        db.close()
        cursor.close()
        bot.send_message(call.message.chat.id, info)

    global NameID
    NameID = message.from_user.id

#кнопки реплай
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn6 = types.KeyboardButton('Кто мы такие')
    btn7 = types.KeyboardButton('Мои споты')
    markup1.row(btn6, btn7)
    btn8 = types.KeyboardButton('Сделать свой спот')
    markup1.row(btn8)
    bot.send_message(message.chat.id, '<b>Добро пожаловать на обдрочено</b>',parse_mode='html',reply_markup=markup1)

    db = sqlite3.connect('obdrocheno.db')
    cursor = db.cursor()

# айдиюзера для юзер
    cursor.execute(
        f'INSERT INTO users (tg_id) VALUES ({NameID})'
    )

# поинт айди дл поинтимедж
    cursor.execute(
        f'INSERT INTO pointsimages (point_id) SELECT id FROM points'
    )
    db.commit()
    db.close()


#хендлер для реплай кнопок
@bot.message_handler()
def click(message):
    if message.text == 'Кто мы такие':
        bot.send_message(message.chat.id, 'Мы очень классная тема мы делаем стики лялял')
    elif message.text == 'Мои споты':
        markup3 = types.InlineKeyboardMarkup()
        markup3.add(types.InlineKeyboardButton("Ваши споты: 0", callback_data="0"))
        bot.reply_to(message, "Извините, у вас нет спотов", reply_markup=markup3)
    elif message.text == 'Сделать свой спот':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Приобрести стикеры", callback_data="Приобрести стикеры"))
        bot.reply_to(message, "Мы продаем стикеры. Купите", reply_markup=markup2)

#хендлер фото
def recieve_photo(message):
    if len(message.photo) == 0:
        return
    global file_id
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    markup = types.InlineKeyboardMarkup()
    btn5 = types.InlineKeyboardButton("Не прикреплять комментарий", callback_data="Skiptext")
    markup.row(btn5)
    bot.register_next_step_handler(message, callback=recieve_message)
    bot.send_message(message.chat.id, 'Ты можешь написать комментарий к фотографии', reply_markup=markup)
    if message != 0:
        @bot.message_handler()
        def comment(message):
            if message.text != 0:
                db = sqlite3.connect('obdrocheno.db')
                cursor = db.cursor()

                cursor.execute(
                f'INSERT INTO images (comment) VALUES ({message})'
                    )

                urlK = 'https://vk.com/kiradiev'

                # айдиюзер и юрл для имаджес
                cursor.execute(
                    f'INSERT INTO images (url) VALUES ({urlK})'
                )

                # юзерайди для имеджис из юзеров
                cursor.execute(
                     f'INSERT INTO images (user_id) SELECT id FROM users'
                )

                # имаджайди для поинтсимаджес
                cursor.execute(
                    f'INSERT INTO pointsimages (image_id) SELECT id FROM images'
                )
                db.commit()
                db.close()
                cursor.close()


#сообщение после регистрации фото
def recieve_message(message):
    bot.send_message(message.chat.id, 'Вы зарегестрированы на спот')

#Хендлер для альбома
@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'Приложить фото':
        bot.send_message(callback.message.chat.id, 'Скинь свое фото, <b>учти, что твой тг айди будет прикреплен к фотографии</b>', parse_mode='html',)
        bot.register_next_step_handler(callback.message, callback=recieve_photo)
    elif callback.data == '<':
        def stepback(call):
            db = sqlite3.connect('obdrocheno.db')
            cursor = db.cursor()

            cursor.execute('SELECT url, comment FROM images')
            cursor.execute('SELECT tg_id FROM users')
            stepbackk = cursor.fetchmany()

            info = ''
            for el in images:
                info += f'Спот №1: {comment -1} {tg_id -1} {url - 1}'

            bot.send_message(call.message.chat.id, info)

    elif callback.data == ">":
        def stepforward(call):
            db = sqlite3.connect('obdrocheno.db')
            cursor = db.cursor()

            cursor.execute('SELECT url, comment FROM images')
            cursor.execute('SELECT tg_id FROM users')
            stepforwardd = cursor.fetchmany()

            info = ''
            for el in images:
                info += f'Спот №1: {comment +1} {tg_id +1} {url +1}'

            bot.send_message(call.message.chat.id, info)

    elif callback.data == "Skiptext":
        bot.send_message(callback.message.chat.id,"Вы зарегестрированы на спот")
    elif callback.data == "Приобрести стикеры":
        bot.send_message(callback.message.chat.id, "Для покупки перейдите по ссылке и нажмите кнопку после покупки")
        markup3 = types.InlineKeyboardMarkup()
        btn10 = types.InlineKeyboardButton("Я оплатил", callback_data="Я оплатил")
        markup3.row(btn10)


bot.polling(non_stop=True)