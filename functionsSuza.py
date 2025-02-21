import os.path
import sqlite3
from importlib.resources import contents
from time import sleep
import json
import telebot
from telebot import TeleBot, types, util
import datetime
import speech_recognition
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import pytz
from datetime import datetime
from Suza_game import *


# SV -1001721689921 train -1001874349025


def GetOwner(message, bot):
    admins = bot.get_chat_administrators(message.chat.id)
    for admin in admins:
        if admin.status == 'creator':
            owner_id = admin.user.id
            owner_username = admin.user.username
            owner_lastname = admin.user.last_name
            owner_firstname = admin.user.first_name
            owner = [owner_id, owner_username, owner_lastname, owner_firstname]
            bot.reply_to(message, f"Идентификатор владельца чата: {owner}")
            break

def Help(message, bot):
    if "/start" in message.text or message.text == "суза":
        bot.reply_to(message, "Привет! Нужна моя помощь?/help")
    elif "/help" in message.text:
        bot.reply_to(message,"Я - бот. Меня зовут Суза.\nТы в любой момент "
                             "можешь меня позвать отправив /start или Суза "
                             "в своем сообщении.\n\n"
                             "Также есть небольшая игра и я могу рассказать "
                             "ее правила. /game\n\n"
                             "Еще могу показать меню разных полезностей "
                             "для мотоциклов Suzuki SV. /menu\n\n"
                             "Каждый день я закрепляю в группе сообщение "
                             "с названием тупого праздника. /holiday\n\n"
                             "В любой группе есть свои болтуны "
                             "и я веду их учет. /windbag\n\n"
                             "Ну и попутно я вывожу текст голосовых "
                             "и видеокружочков.\n"
                             "Помощь тут - /help")
    elif "/game" in message.text:
        bot.reply_to(message, "Я веду техническую часть небольшой "
                              "текстовой игры. Правила таковы:\n"
                              "Если ты отвечаешь на чужое сообщение с помощью "
                              "функции 'ответить' и используешь одно из "
                              "игровых слов, то будет выполнено одно из "
                              "действий:\n\n"
                              "украсть, спиздить, скрасть, обокрасть, "
                              "воровать, обчистить - любое из этих слов "
                              "приведет к тому, что ты попытаешься украсть "
                              "запчасти у того на чьё сообщение ты отвечал\n\n"
                              "пнуть,опустить, отпиздить, зачмырить, унизить -"
                              " любое из этих слов приведет к тому, что ты "
                              "попытаешься ударить того на чье сообщение "
                              "ты отвечал\n\n"
                              "поцеловать, поцелуй, чмок, целовашки - любое из"
                              " этих слов приведет к тому, что ты поцелуешь "
                              "того на чье сообщение ты отвечал\n\n"
                              "обнять, обнимашки, затискать - любое из этих "
                              "слов приведет к тому, что ты обнимешь того на "
                              "чье сообщение ты отвечал\n\n"
                              "пожертвовать, подарить - любое из этих слов "
                              "приведет к тому, что ты подаришь запчасти тому "
                              "на чье сообщение ты отвечал, а ты при этом "
                              "получишь небольшой подъем авторитета\n\n"
                              "чпок - думаю, тут не надо объяснять , да?!\n\n"
                              "+, +++, спасибо, пасяб,спс, сяб, пасибо - "
                              "любое из этих слов приведет к тому, что ты "
                              "поднимешь на  единичку авторитет того на чье "
                              "сообщение ты отвечал\n\n"
                              "отправленный '-' понизит авторитет на единичку "
                              "того на чье сообщение ты отвечал\n\n"
                              "удастся ли пнуть или украсть - рассчитывается "
                              "случайно, как и то сколько ты украдешь или "
                              "насколько понизишь авторитет.\n\n"
                              "В начале игры твой авторитет равен 100, а "
                              "запчастей у тебя 10\n\n"
                              "Помощь тут - /help")
    elif "/holiday" in message.text:
        bot.reply_to(
            message,
            "Каждый день в 00ч 00мин по московскому времени, я отправляю "
            "сообщение с названием сегодняшнего праздника. И закрепляю это "
            "сообщение в группе. Не знаю существуют ли такие праздники, но "
            "не стоит к этому относиться слишком серьезно, это всего лишь "
            "ради забавы. Помощь тут - /help")
    elif "/windbag" in message.text:
        bot.reply_to(
            message,
            "Я записываю кто сколько сообщений написал в группе за день, "
            "за неделю, за месяц, за год. И на основании этих данных "
            "присваиваю шутейные 'звания'. Вызвать статистику за день можно "
            "написав /stat или !stat. Помощь тут - /help")

def writing_statistics(message: Message):
    """
    Функция для записи количества сообщений отправленных пользователем
    в группу или бота.

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`

    :return: None
    """
    content_type = message.content_type
    chat_id = str(message.chat.id)
    chat_title = message.chat.title
    user_id = str(message.from_user.id)
    if content_type in ['text', 'animation', 'audio',
                        'document', 'photo', 'sticker',
                        'video', 'video_note', 'voice']:
        with sqlite3.connect('users.db') as con:
            cursor = con.cursor()
            cursor.execute(f'''CREATE TABLE 
                            IF NOT EXISTS "{chat_id}" 
                            ("chat_title"	TEXT,
                            "user_id"	TEXT NOT NULL UNIQUE,
                            "text"	INTEGER NOT NULL DEFAULT 0,
                            "animation"	INTEGER NOT NULL DEFAULT 0,
                            "audio"	INTEGER NOT NULL DEFAULT 0,
                            "document"	INTEGER NOT NULL DEFAULT 0,
                            "photo"	INTEGER NOT NULL DEFAULT 0,
                            "sticker"	INTEGER NOT NULL DEFAULT 0,
                            "video"	INTEGER NOT NULL DEFAULT 0,
                            "video_note"	INTEGER NOT NULL DEFAULT 0,
                            "voice"	INTEGER NOT NULL DEFAULT 0,
                            "reputation"	INTEGER NOT NULL DEFAULT 0)''')
            con.commit()
            cursor.execute(f'''SELECT user_id FROM "{chat_id}" 
                                WHERE user_id=?''',(user_id,))
            if cursor.fetchone() is None:
                cursor.execute(f'''INSERT INTO "{chat_id}" 
                                    (chat_title, user_id, text, animation, 
                                    audio, document, photo, sticker, video, 
                                    video_note, voice, reputation) VALUES 
                                    (?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)''',
                        (chat_title, user_id, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0))
            con.commit()
            cursor.execute(f'''SELECT {content_type} FROM "{chat_id}" 
                                    WHERE user_id=?''', (user_id,))
            result = list(cursor.fetchone())
            result[0] += 1
            cursor.execute(f'''UPDATE "{chat_id}" SET {content_type} = ?
                             WHERE user_id = ?''', (result[0], user_id))
            con.commit()

def check_command(message: Message, bot: TeleBot):
    if message.text.lower() == "/start":
        pass
    elif message.text.lower() == "/help":
        pass
    elif message.text.lower() == "/stat":
        check_statistic(message, bot)

def check_statistic(message: Message, bot: TeleBot):
    '''
    Обрабатывает запрос на показ статистики пользователя в данном чате

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`

    :return: None
    '''

    user_id = None
    user_lastname = None
    username = None
    user_firstname = None
    chat_id = str(message.chat.id)
    if message.reply_to_message is None:
        user_id = str(message.from_user.id)
        user_lastname = message.from_user.last_name
        username = message.from_user.username
        user_firstname = message.from_user.first_name
    else:
        user_id = str(message.reply_to_message.from_user.id)
        user_lastname = message.reply_to_message.from_user.last_name
        username = message.reply_to_message.from_user.username
        user_firstname = message.reply_to_message.from_user.first_name
    with sqlite3.connect('users.db') as con:
        cursor = con.cursor()
        cursor.execute(f'''SELECT * FROM "{chat_id}" WHERE user_id = ? ''',
                       (user_id,))
        result = cursor.fetchall()
        text = f'''Фамилия: {user_lastname}\n
                   Имя: {user_firstname}\n
                   Юзернейм: {username}\n
                   отправил:\n
                   текстовых - {result[0][2]}\n,
                   анимаций - {result[0][3]}\n,
                   аудио - {result[0][4]}\n,
                   документов - {result[0][5]}\n,
                   фото - {result[0][6]}\n,
                   стикеров - {result[0][7]}\n,
                   видео - {result[0][8]}\n,
                   видеокружков - {result[0][9]}\n,
                   голосовых - {result[0][10]}\n,
                   репутация - {result[0][11]}\n
                   '''
        pic = None
        member = bot.get_user_profile_photos(int(user_id),1,1)
        print() # получить фото пользователя

def VoiceMsg(message:Message, bot:TeleBot):
    whosaid = ""
    # Получаем информацию о голосовом сообщении
    file_info = bot.get_file(message.voice.file_id)
    file_path = file_info.file_path

    # Скачиваем аудиофайл
    downloaded_file = bot.download_file(file_path)

    # Сохраняем аудиофайл на диск
    with open('voice_message.ogg', 'wb') as f:
        f.write(downloaded_file)

    # Загружаем аудиофайл и конвертируем его в WAV
    audio = AudioSegment.from_file('voice_message.ogg', format='ogg')
    audio.export('voice_message.wav', format='wav')
    RecognAudio("voice_message.wav", bot,message)

def VideoMsg(message, bot):
    if message.content_type == "video":
        file_id = message.video.file_id
    else:
        file_id = message.video_note.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("video.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)
    video = VideoFileClip("video.mp4")
    audio = video.audio
    audio.write_audiofile("audio.wav")
    RecognAudio("audio.wav", bot, message)

def RecognAudio(audio,bot:TeleBot, message:Message):
    # Распознаем речь в аудиофайле
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language='ru')  # выдает не весь текст, проверить
            lines = telebot.util.smart_split(text, chars_per_string= 3000)
            for line in lines:
                bot.reply_to(message, line)
                sleep(20)
        except speech_recognition.exceptions.UnknownValueError:
            bot.reply_to(message, "Бурчит себе чего-то под нос, "
                                  "ни фига непонятно. Говори четче")

keybMain = types.InlineKeyboardMarkup(row_width=3)
btnManual = types.InlineKeyboardButton(text="Мануал",
                                       callback_data="manuals")
btnParts = types.InlineKeyboardButton(text="Расходники",
                                      callback_data="expendables")
btnTraders = types.InlineKeyboardButton(text="Продавцы",
                                        callback_data="traders")
btnMasters = types.InlineKeyboardButton(text="Мастера",
                                        callback_data="masters")
btnEvents = types.InlineKeyboardButton(text="События",
                                       callback_data="events")
btnGoodness = types.InlineKeyboardButton(text="Полезности",
                                         callback_data="goodness")
keybMain.add(btnManual, btnParts, btnTraders, btnMasters,
             btnEvents, btnGoodness)
def Menu(message, bot):
    bot.reply_to(message, "Выбирайте, что хотите. Помощь тут - /help",
                 reply_markup=keybMain)
def suza_menu(callback, bot):
    if 1 <= len(callback.data.split(" ")) < 2:
        conn = sqlite3.connect('SV.db')
        cursor = conn.cursor()

        # Выполнение запроса для выборки строки по полю "name"
        cursor.execute(f"SELECT title,name FROM {callback.data}")
        rows = cursor.fetchall()
        keyb = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        for row in rows:
            title = row[0]
            name = row[1]
            button = types.InlineKeyboardButton(name,
                                                callback_data=f"{title} {callback.data}")
            buttons.append(button)
        keyb.add(*buttons)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text="Вот что есть:", reply_markup=keyb)

    elif 2 <= len(callback.data.split(" ")) < 3:
        if callback.data.split(" ")[0] == "main":
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.id,
                                  text="Привет,  я - Суза.", reply_markup=keybMain)
        else:
            name_table = callback.data.split(" ")[1]
            first_field = callback.data.split(" ")[0]
            conn = sqlite3.connect('SV.db')
            cursor = conn.cursor()

            # Выполнение запроса для выборки строки по полю "name"
            cursor.execute(f"SELECT title,name,description,link,picture "
                           f"FROM {name_table} WHERE title=?",
                           (first_field,))
            rows = cursor.fetchall()
            for row in rows:
                if row[4] and row[4] != "" and row[4] != " ":
                    photo = open(f"{row[4]}", 'rb')
                    caption = f"{row[2]} \n {row[3]}"
                    bot.send_photo(chat_id=callback.message.chat.id,
                                   photo=photo, caption=caption,
                                   reply_to_message_id=callback.message.message_id)

                else:
                    caption = f"{row[2]} \n {row[3]}"
                    bot.send_message(chat_id=callback.message.chat.id,
                                     text=caption,
                                     reply_to_message_id=callback.message.message_id)

# проверить эту же функцию в Suza_game и убрать отсюда
def Wedding(callback, bot):
    wife = callback.data.split(" ")
    wife = wife[1]
    if callback.from_user.id == int(wife):
        if "notmarried" in callback.data:
            callback.data = callback.data.replace("notmarried ", "")
            callback.data = callback.data.split(" ")
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT user_id,username,lastname,firstname "
                           "FROM users WHERE user_id=?",
                           (callback.data[1],))
            robb_mar = cursor.fetchone()
            bot.send_message(callback.message.chat.id,
                             f"{robb_mar[0]}/{robb_mar[1]}/{robb_mar[2]} "
                             f"{robb_mar[3]}\nСожалею, но тебе отказали.")
        else:
            robb_id = callback.data.split(" ")
            robb_id= robb_id[1]
            vict_id = callback.data.split(" ")
            vict_id = vict_id[2]
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET married=? "
                           "WHERE user_id=?", ("mariied", robb_id))
            conn.commit()
            cursor.execute("UPDATE users SET married=? "
                           "WHERE user_id=?", ("mariied", vict_id))
            conn.commit()
            cursor.execute("SELECT user_id,username,lastname,firstname "
                           "FROM users WHERE user_id=?", (robb_id,))
            robb_mar = cursor.fetchone()
            cursor.execute("SELECT user_id,username,lastname,firstname "
                           "FROM users WHERE user_id=?", (robb_id,))
            vict_mar = cursor.fetchone()
            bot.send_message(callback.message.chat.id,
                             f"Отныне между\n{robb_mar[0]}/{robb_mar[1]}/"
                             f"{robb_mar[2]} {robb_mar[3]}\nи\n{vict_mar[0]}/"
                             f"{vict_mar[1]}/{vict_mar[2]} {vict_mar[3]}\n"
                             f"заключен брак!\nЖивите и процветайте, "
                             f"пока дорожный столб не разъединит вас.")
            conn.close()


def BirthdaySVClub(bot):
    current_date = datetime.now(
        pytz.timezone('Europe/Moscow')).strftime('%m-%d')
    conn = sqlite3.connect('SV.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Name, Date, UserName FROM SVCLUB_Birthday")
    rows = cursor.fetchall()

    # Отправка поздравления в группу для каждого участника с днем рождения
    for row in rows:
        name = row[0]
        username = row[2]
        photo = open('Birthday.jpg', 'rb')
        timezone = pytz.timezone('UTC')
        datetime_object = datetime.strptime(
            row[1],
            '%Y-%m-%d').replace(tzinfo=pytz.utc).astimezone(timezone)
        birthday_date = datetime_object.strftime('%m-%d')
        if birthday_date == current_date:
            birthday_message = (f"С днем рождения,{name}! Пусть твои "
                                f"мотоциклетные приключения будут полны "
                                f"ветра в волосах и свободы на дороге. "
                                f"Желаем тебе невероятных путешествий, "
                                f"безопасных маневров и всегда удачных "
                                f"приземлений. Пусть каждая поездка будет "
                                f"наполнена адреналином и радостью.")
            bot.send_photo(-1001721689921, photo, birthday_message)
            #if (birthday_date.month ==12 and birthday_date.day == 31) or (birthday_date.month ==0o1 and birthday_date.day == 0o1):
                #photony = open('ny.png', 'rb')
                #bot.send_photo(1303933780, photo= photony, caption= "Дорогие SV'шники! Пусть новый год прольется на вас как свежий ветер, наполняя сердца радостью и оптимизмом. Пусть в Новом году дороги будут ровными, а повороты – захватывающими. Пусть каждый километр приносит новые впечатления и незабываемые моменты. Пусть мотоцикл будет вашим верным спутником, а дорога – источником вдохновения. С Новым Годом!")

    conn.close()
