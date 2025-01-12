import sqlite3, pytz,datetime,os, random
import time





def hollidays(message, bot):
    if message.chat. id is None:
        message.chat.id = message.reply_to_message.chat. id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получаем текущую дату
    current_date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m-%d')

    # Проверяем, есть ли праздник на сегодняшнюю дату в таблице
    cursor.execute('SELECT holiday FROM holidays WHERE date = ?', (current_date,))
    holiday = cursor.fetchone()

    # Если праздник найден, отправляем его название
    if holiday:
        bot.send_message(message.chat.id, f"Сегодня отмечаем: {holiday[0]}", disable_notification=True)
    else:
        bot.send_message(message.chat.id, "Сегодня каких-либо особых праздников не нашлось. Но ничто ж не мешает выпить за здоровье для здоровья!ПС: неумеренное употребление алкоголя вредит вашему здоровью. ;)")
    conn.close()


def UpActivity(message, bot):
    if message.chat.id is None:
        chat_id = message.reply_to_message.chat.id
    else:
        chat_id = message.chat.id
    if "вечер в хату" in message.text or "доброго вечера" in message.text or "добрый вечер" in message.text:
        evening_words = ["Так.Вышел за дверь, и зашел нормально!",
                         "Вечерело, собирались алкаши...",
                         "Наше вам с кисточкой.",
                         "Наше почтение.",
                         "Действительно добрый!",
                         "Вы уверены?",
                         "И вам не чахнуть",
                         "Сейчас еще день, у вас какие-то намерения на вечер?",
                         "Справедливое высказывание!",
                         "Наливай."]
        bot.reply_to(message, f"{evening_words[random.randint(0,len(evening_words) - 1)]}")
    elif "утра" in message.text or "утро" in message.text:
        morning_words = ["Хуютра!",
                         "И тебе боброго!",
                         "Денег нет",
                         "Какие еще новости?",
                         "С моим совпало только на пятьдесят процентов",
                         "Нет, в жизни либо добро, либо утро, и они несовместимы, как показывает практика",
                         "Ты уже 'Добрый день' пиши, так надежнее:)",
                         "Утро добрым не бывает!",
                         "Какие утра?",
                         "После такого вечера утро добрым не бывает.",
                         "Надеюсь, твои слова окажутся реальностью."]
        bot.reply_to(message, f"{morning_words[random.randint(0,len(morning_words) - 1)]}")
    elif "сиськи" in message.text:
        bot.reply_to(message, "Сам напросился")
        photo = open('Siski.jpg', 'rb')
        bot.send_photo(chat_id, photo)
    elif "ямаха" in message.text:
        bot.reply_to(message, "Ямаха, ямаха, да иди ты на ... в магазин.\n Бан за использование неканоничной марки в SV-чате!")
    elif "хонда" in message.text:
        bot.reply_to(message, "Хонда.... Пять букв, последние две 'да'. Кажется я припоминаю еще одно слово заканчивающиеся на '...да'. \n Бан за скрытый мат! ")
    elif "оксана" in message.text:
        oksana_words = ["Уносите детей. Воспитательница рядом )))",
                        "Чую пахнет интригой...",
                        "Снова стою одна, снова курю мама, снова... Так, о чем это я ?!",
                        "Оксана, Оксана... Что-то меня на тревогу пробило...",
                        "Оксана, Ксеня, Ксюша.... Ксюш, Ксюш, Ксюша, девочка из плюша ..."]
        bot.reply_to(message, f"{oksana_words[random.randint(0,len(oksana_words) - 1)]}")
    elif "гараж" in message.text:
        garage_words = ["Гараж для мотоциклиста - второй дом!",
                        "Гараж? Какой гараж? Кафе 'Два Коляна???'",
                        "Гараж!!! Это удивительное место! Где выучивалась мастера! И спивались гении..."]
        bot.reply_to(message, f"{garage_words[random.randint(0,len(garage_words) - 1)]}")
    elif "литр" in message.text:
        litr_words = ["Литр... Возьми ты уже лучше 'Альфу'. Она хоть прёт.",
                      "Литр, литр... Да возьми ты уже полтарашку и не парься!",
                      "Клитр. Шума много, а толку нет."]
        bot.reply_to(message, f"{litr_words[random.randint(0,len(litr_words) - 1)]}")
    elif "селфитайм" in message.text or "селфи тайм" in message.text or "сэлфи тайм" in message.text or "сэлфитайм" in message.text:
        # Выбираем случайную фотографию из списка
        random_photo = random.choice(os.listdir("selfi_pics"))
        # Отправляем фотографию
        bot.send_photo(chat_id=chat_id, photo=open(os.path.join("selfi_pics", random_photo), 'rb'), caption="селфитайм")



def check_word(message): #сделать триггер на селфитайм и фоток сузы селфи
    word_list = ["вечер в хату", "утра", "доброе утро", "сиськи", "ямаха", "хонда",
                 "гараж", "оксана", "литр", "добрый вечер", "доброго вечера",
                 "селфитайм", "селфи тайм", "сэлфи тайм", "сэлфитайм"]
    for word in word_list:
        if word in message.text:
            return True
    return False



def forward_message_to_group(message, bot):
    if message.text is not None:
        text = ' '.join(message.text.split()[1:])
        bot.send_message(-1001721689921,text)
    elif message.caption is not None and message.photo is not None:
        text = ' '.join(message.caption.split()[1:])
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        downloaded_photo = bot.download_file(photo_info.file_path)
        photo = downloaded_photo
        bot.send_photo(-1001721689921,photo= photo, caption= text)
    elif message.caption is not None and message.video is not None:
        text = ' '.join(message.caption.split()[1:])
        video_id = message.video.file_id
        video_info = bot.get_file(video_id)
        downloaded_video = bot.download_file(video_info.file_path)
        video = downloaded_video
        bot.send_video(-1001721689921,video= video, caption= text)


# Переделать по-людски
def set_reminder(message):
    droped_text = message.text.split(" ")
    message_date = datetime.utcfromtimestamp(message.date)
    # Определение часового пояса
    tz_moscow = pytz.timezone('Europe/Moscow')
    date_moscow = message_date.replace(tzinfo=pytz.utc).astimezone(tz_moscow)
    date = (((str(date_moscow)).split())[0]).split("-")
    if len(droped_text) > 1:
        desc = message.reply_to_message.text
        date[2] = str(int(date[2]) + int(droped_text[1]))
    else:
        desc = message.reply_to_message.text
        date[2] = str(int(date[2]) + 5)
    date_to_string = f"{date[0]}" + "-" + f"{date[1]}" + "-" f"{date[2]}"
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS reminds (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, day INTEGER)")
        cursor.execute(f"INSERT INTO reminds (description, day) VALUES ('{desc}', '{date_to_string}')")
        con.commit()


# переделать по-людски
def checking_reminds(message):
    message_date = datetime.utcfromtimestamp(message.date)
    # Определение часового пояса
    tz_moscow = pytz.timezone('Europe/Moscow')
    message_date_moscow = message_date.replace(tzinfo=pytz.utc).astimezone(tz_moscow)
    # Извлечение дня отправленного сообщения в часовом поясе Москвы
    message_day_moscow = message_date_moscow.day
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT description FROM reminds WHERE day = {message_day_moscow}")
