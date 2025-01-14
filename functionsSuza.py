# -*- coding: utf-8 -*-
import time
from telebot import types
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
        bot.reply_to(message,"Я - бот. Меня зовут Суза.\nТы в любой момент можешь меня позвать отправив /start или Суза в своем сообщении.\n\n"
                             "Также есть небольшая игра и я могу рассказать ее правила. /game\n\n"
                             "Еще могу показать меню разных полезностей для мотоциклов Suzuki SV. /menu\n\n"
                             "Каждый день я закрепляю в группе сообщение с названием тупого праздника. /holiday\n\n"
                             "В любой группе есть свои болтуны и я веду их учет. /windbag\n\n"
                             "Ну и попутно я вывожу текст голосовых и видеокружочков.\n"
                             "Помощь тут - /help")
    elif "/game" in message.text:
        bot.reply_to(message, "Я веду техническую часть небольшой текстовой игры. Правила таковы:\n"
                              "Если ты отвечаешь на чужое сообщение с помощью функции 'ответить' и используешь одно из игровых слов, то будет выполнено одно из действий:\n\n"
                              "украсть, спиздить, скрасть, обокрасть, воровать, обчистить - любое из этих слов приведет к тому, что ты попытаешься украсть запчасти у того на чьё сообщение ты отвечал\n\n"
                              "пнуть,опустить, отпиздить, зачмырить, унизить - любое из этих слов приведет к тому, что ты попытаешься ударить того на чье сообщение ты отвечал\n\n"
                              "поцеловать, поцелуй, чмок, целовашки - любое из этих слов приведет к тому, что ты поцелуешь того на чье сообщение ты отвечал\n\n"
                              "обнять, обнимашки, затискать - любое из этих слов приведет к тому, что ты обнимешь того на чье сообщение ты отвечал\n\n"
                              "пожертвовать, подарить - любое из этих слов приведет к тому, что ты подаришь запчасти тому на чье сообщение ты отвечал, а ты при этом получишь небольшой подъем авторитета\n\n"
                              "чпок - думаю, тут не надо объяснять , да?!\n\n"
                              "+, +++, спасибо, пасяб,спс, сяб, пасибо - любое из этих слов приведет к тому, что ты поднимешь на  единичку авторитет того на чье сообщение ты отвечал\n\n"
                              "отправленный '-' понизит авторитет на единичку того на чье сообщение ты отвечал\n\n"
                              "удастся ли пнуть или украсть - рассчитывается случайно, как и то сколько ты украдешь или насколько понизишь авторитет.\n\n"
                              "В начале игры твой авторитет равен 100, а запчастей у тебя 10\n\n"
                              "Помощь тут - /help")
    elif "/holiday" in message.text:
        bot.reply_to(message, " Каждый день в 00ч 00мин по московскому времени, я отправляю сообщение с названием сегодняшнего праздника. И закрепляю это сообщение в группе. Не знаю существуют ли такие праздники, но не стоит к этому относиться слишком серьезно, это всего лишь ради забавы. Помощь тут - /help")
    elif "/windbag" in message.text:
        bot.reply_to(message, "Я записываю кто сколько сообщений написал в группе за день, за неделю, за месяц, за год. И на основании этих данных присваиваю шутейные 'звания'. Вызвать статистику за день можно написав /stat или !stat. Помощь тут - /help")

def Statistics(message):
    name_table = "statsmsg" + str(abs(message.chat.id))
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name_table}'")
    existing_table = cursor.fetchone()
    if not existing_table:
        cursor.execute(f"CREATE TABLE {name_table} (user_id INTEGER NOT NULL, username TEXT, lastname TEXT, firstname TEXT, daystats INTEGER, weekstats INTEGER, monthstats INTEGER, yearstats INTEGER, mute TEXT, PRIMARY KEY(user_id))")
        conn.commit()
    cursor.execute(f"SELECT * FROM {name_table} WHERE user_id=?", (message.from_user.id,))
    user_data = cursor.fetchone()
    if user_data is None:
        # Если пользователь не существует, добавляем его в базу данных
        cursor.execute(f"INSERT INTO {name_table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.username, message.from_user.last_name, message.from_user.first_name,1,0,0,0, 'True'))
        conn.commit()
    else:
        user_data = list(user_data)
        user_data[4]+=1
        cursor.execute(f"UPDATE {name_table} SET username=?, lastname=?, firstname=?, daystats=?, weekstats=?, monthstats=?, yearstats=? WHERE user_id=?", (message.from_user.username, message.from_user.last_name, message.from_user.first_name, user_data[4], user_data[5], user_data[6], user_data[7], message.from_user.id))
        conn.commit()

def SaveStats(flag):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получаем список всех таблиц, у которых в названии есть "statsmsg"
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'statsmsg%'")
    table_names = cursor.fetchall()

    for table_name in table_names:
        # Получаем все строки из текущей таблицы
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()

        for row in rows:
            user = list(row)
            if flag == "closeday":
                user[5] += user[4]
                user[4] = 0
            elif flag == "closeweek":
                user[6] = user[6] + user[5] + user[4]
                user[5] = 0
                user[4] = 0
            elif flag == "closemonth":
                user[7] = user[7] + user[6] + user[5] + user[4]
                user[5] = 0
                user[4] = 0
            elif flag == "NewYear":
                user[7] = 0
                user[5] = 0
                user[4] = 0
            cursor.execute(f"UPDATE {table_name[0]} SET username=?, lastname=?, firstname=?, daystats=?, weekstats=?, monthstats=?, yearstats=? WHERE user_id=?", (user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[0]))
            conn.commit()
    # Фиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()

def StatConversations(message, bot):
    name_table = "statsmsg" + str(abs(message.chat.id))
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Выполнение SQL-запроса
    cursor.execute(f"SELECT user_id,daystats FROM {name_table} ORDER BY daystats DESC")
    masive = cursor.fetchall()
    half = len(masive) // 2
    first_half = masive[:half]
    second_half = masive[half:]
    result = [first_half[0][0], first_half[-1][0], second_half[-1][0]]
    cursor.execute(f"SELECT user_id,username,lastname,firstname,daystats FROM {name_table} WHERE user_id IN ({result[0]}, {result[1]}, {result[2]})")
    result = list(cursor.fetchall())
    result.sort(key=lambda x: x[-1], reverse=True)
    pizdabol_text = f"Итак сейчас у нас:\n\nНеостановимый пиздабол:\n@{result[0][1]}/{result[0][0]}/{result[0][2]} {result[0][3]}"
    boltun_text = f"\nПериодический подпездыватель:\n@{result[1][1]}/{result[1][0]}/{result[1][2]} {result[1][3]}"
    tihonya_text = f"\nПодозрительный тихушник:\n@{result[2][1]}/{result[2][0]}/{result[2][2]} {result[2][3]}"
    all_text = f"{pizdabol_text}\n{boltun_text}\n{tihonya_text}"
    conn.close()
    bot.reply_to(message, f"{all_text}")


def VoiceMsg(message, bot):
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

def RecognAudio(audio,bot, message):
    # Распознаем речь в аудиофайле
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language='ru')
            bot.reply_to(message, text)
        except speech_recognition.exceptions.UnknownValueError:
            bot.reply_to(message, "Бурчит себе чего-то под нос, ни фига непонятно. Говори четче")

keybMain = types.InlineKeyboardMarkup(row_width=3)
btnManual = types.InlineKeyboardButton(text="Мануал", callback_data="manuals")
btnParts = types.InlineKeyboardButton(text="Расходники", callback_data="expendables")
btnTraders = types.InlineKeyboardButton(text="Продавцы", callback_data="traders")
btnMasters = types.InlineKeyboardButton(text="Мастера", callback_data="masters")
btnEvents = types.InlineKeyboardButton(text="События", callback_data="events")
btnGoodness = types.InlineKeyboardButton(text="Полезности", callback_data="goodness")
keybMain.add(btnManual, btnParts, btnTraders, btnMasters, btnEvents, btnGoodness)
def Menu(message, bot):
    bot.reply_to(message, "Выбирайте, что хотите. Помощь тут - /help", reply_markup=keybMain)
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
            button = types.InlineKeyboardButton(name, callback_data=f"{title} {callback.data}")
            buttons.append(button)
        keyb.add(*buttons)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text="Вот что есть:", reply_markup=keyb)

    elif 2 <= len(callback.data.split(" ")) < 3:
        if callback.data.split(" ")[0] == "main":
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                    text="Привет,  я - Суза.", reply_markup=keybMain)
        else:
            name_table = callback.data.split(" ")[1]
            first_field = callback.data.split(" ")[0]
            conn = sqlite3.connect('SV.db')
            cursor = conn.cursor()

            # Выполнение запроса для выборки строки по полю "name"
            cursor.execute(f"SELECT title,name,description,link,picture FROM {name_table} WHERE title=?",
                            (first_field,))
            rows = cursor.fetchall()
            for row in rows:
                if row[4] and row[4] != "" and row[4] != " ":
                    photo = open(f"{row[4]}", 'rb')
                    caption = f"{row[2]} \n {row[3]}"
                    bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption=caption,
                                    reply_to_message_id=callback.message.message_id)

                else:
                    caption = f"{row[2]} \n {row[3]}"
                    bot.send_message(chat_id=callback.message.chat.id, text=caption,
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
            cursor.execute("SELECT user_id,username,lastname,firstname FROM users WHERE user_id=?", (callback.data[1],))
            robb_mar = cursor.fetchone()
            bot.send_message(callback.message.chat.id, f"{robb_mar[0]}/{robb_mar[1]}/{robb_mar[2]} {robb_mar[3]}\nСожалею, но тебе отказали.")
        else:
            robb_id = callback.data.split(" ")
            robb_id= robb_id[1]
            vict_id = callback.data.split(" ")
            vict_id = vict_id[2]
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET married=? WHERE user_id=?", ("mariied", robb_id))
            conn.commit()
            cursor.execute("UPDATE users SET married=? WHERE user_id=?", ("mariied", vict_id))
            conn.commit()
            cursor.execute("SELECT user_id,username,lastname,firstname FROM users WHERE user_id=?", (robb_id,))
            robb_mar = cursor.fetchone()
            cursor.execute("SELECT user_id,username,lastname,firstname FROM users WHERE user_id=?", (robb_id,))
            vict_mar = cursor.fetchone()
            bot.send_message(callback.message.chat.id, f"Отныне между\n{robb_mar[0]}/{robb_mar[1]}/{robb_mar[2]} {robb_mar[3]}\nи\n{vict_mar[0]}/{vict_mar[1]}/{vict_mar[2]} {vict_mar[3]}\nзаключен брак!\nЖивите и процветайте, пока дорожный столб не разъединит вас.")
            conn.close()


def BirthdaySVClub(bot):
    current_date = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m-%d')
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
        datetime_object = datetime.strptime(row[1], '%Y-%m-%d').replace(tzinfo=pytz.utc).astimezone(timezone)
        birthday_date = datetime_object.strftime('%m-%d')
        if birthday_date == current_date:
            birthday_message = f"С днем рождения,{name}! Пусть твои мотоциклетные приключения будут полны ветра в волосах и свободы на дороге. Желаем тебе невероятных путешествий, безопасных маневров и всегда удачных приземлений. Пусть каждая поездка будет наполнена адреналином и радостью."
            bot.send_photo(-1001721689921, photo, birthday_message)
            #if (birthday_date.month ==12 and birthday_date.day == 31) or (birthday_date.month ==0o1 and birthday_date.day == 0o1):
                #photony = open('ny.png', 'rb')
                #bot.send_photo(1303933780, photo= photony, caption= "Дорогие SV'шники! Пусть новый год прольется на вас как свежий ветер, наполняя сердца радостью и оптимизмом. Пусть в Новом году дороги будут ровными, а повороты – захватывающими. Пусть каждый километр приносит новые впечатления и незабываемые моменты. Пусть мотоцикл будет вашим верным спутником, а дорога – источником вдохновения. С Новым Годом!")

    conn.close()
