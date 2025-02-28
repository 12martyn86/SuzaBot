from telebot import TeleBot
import telebot
import sqlite3
import datetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


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


def check_statistic(message: Message, bot: TeleBot):
    '''
    Обрабатывает запрос на показ статистики пользователя в данном чате

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`
    :param bot: Telebot
    :return: None
    '''

    user_id = None
    user_lastname = None
    username = None
    user_firstname = None
    chat_id = str(message.chat.id)
    thread_id = None
    text = ""
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
        if result is not None and result != []:
            text +=  (f"Фамилия: {user_lastname}\n"
                     f"Имя: {user_firstname}\n"
                     f"Юзернейм: {username}\n"
                     f"отправил:\n"
                     f"текстовых - {result[0][2]},\n"
                     f"анимаций - {result[0][3]},\n"
                     f"аудио - {result[0][4]},\n"
                     f"документов - {result[0][5]},\n"
                     f"фото - {result[0][6]},\n"
                     f"стикеров - {result[0][7]},\n"
                     f"видео - {result[0][8]},\n"
                     f"видеокружков - {result[0][9]},\n"
                     f"голосовых - {result[0][10]},\n"
                     f"репутация - {result[0][11]}\n")
        user_photos = bot.get_user_profile_photos(int(user_id),1,1).photos
        if message.chat.is_forum:
            thread_id=message.message_thread_id
        if user_photos != [] and not message.from_user.is_bot:
            profile_pic_id = user_photos[0][0].file_id
            bot.send_photo(int(chat_id),
                           photo=profile_pic_id,
                           caption=text,
                           reply_to_message_id=message.message_id,
                           message_thread_id=thread_id)
        elif message.reply_to_message.from_user.is_bot:
            bot.send_message(int(chat_id),
                             "Похоже это бот. Но это неточно.",
                             reply_to_message_id=message.message_id,
                             message_thread_id=thread_id)
        else:
            bot.send_message(int(chat_id),
                             text=text, reply_to_message_id=message.id,
                             message_thread_id=message.message_thread_id)


def join_request(message: Message, bot: TeleBot):
    '''
    Обрабатывает вступление нового пользователя в группу и ограничивает права нового участника.

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`
    :param bot: Telebot
    :return: None
    '''

    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    lastname = message.from_user.last_name
    firstname = message.from_user.first_name
    with sqlite3.connect('users.db') as con:
        cursor = con.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{str(chat_id)}"("chat_title"	TEXT,
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
        cursor.execute(f'''SELECT user_id FROM "{str(chat_id)}"''')
        result = cursor.fetchall()
        if result != []:
            if str(user_id) in result:
                bot.reply_to(message, "Рада вас снова приветствовать в чате! С возвращением!")
            else:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=None,
                         can_send_media_messages=None,
                         can_send_polls=None,
                         can_send_other_messages=None,
                         can_change_info=None,
                         can_invite_users=None,
                         can_pin_messages=None)
                keyb = InlineKeyboardMarkup()
                btn = InlineKeyboardButton('Нажми', callback_data=f'new_join_request {str(user_id)}')
                keyb.add(btn)
                for name in [firstname, username, lastname]:
                    if name is not None and name.strip() != "":
                        bot.reply_to(message,
                                     f"Привет {name}.\nЕсли ты не бот нажми на кнопку ниже в течение 3 минут.",
                                     reply_markup=keyb)
                        break
                    else:
                        bot.reply_to(message,
                                     "Привет.\nЕсли ты не бот нажми на кнопку ниже в течение 3 минут.",
                                     reply_markup=keyb)
    unverifed_user  = [f'{user_id}',f'{datetime.datetime.now()}',f'{chat_id}']
    with open('unverifed_users.txt', 'a', encoding='utf-8', ) as file:
        file.write('#'.join(unverifed_user) + '\n')


def kick_unverifed_user(bot: TeleBot):
    '''
    Проверяет есть ли в файле запись с пользователем, если запись есть - снимает ограничения
    спользователя и удаляет его из группы.

    :param bot: Telebot
    :return: None
    '''
    now = datetime.datetime.now()
    new_data = []
    with open("unverifed_users.txt", 'r', encoding='utf-8') as file:
        data = file.readlines()
        for line in data:
            if line != '\n':
                    info = line.split('#')
                    user_id = int(info[0])
                    user_time = datetime.datetime.strptime(info[1], '%Y-%m-%d %H:%M:%S.%f')
                    chat_id = int(info[2])
                    if user_time + datetime.timedelta(seconds=180) <= now:
                        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True,
                                                 can_send_media_messages=True,
                                                 can_send_polls=True,
                                                 can_send_other_messages=True,
                                                 can_change_info=True,
                                                 can_invite_users=True,
                                                 can_pin_messages=True)
                        bot.unban_chat_member(chat_id, user_id)
                    else:
                        new_data.append(line)
    with open('unverifed_users.txt', 'w', encoding='utf-8', ) as file:
        for line in new_data:
            file.write(line + '\n')


def allow_request_new_member(user_id: int, chat_id: int, bot: TeleBot, ):
    '''
    Обрабатывает нажатие пользователем кнопки подтверждающей, что пользователь не бот.

    :param user_id: int
    :param chat_id: int
    :param bot: TeleBot

    :return: None
    '''
    with open("unverifed_users.txt", 'r', encoding='utf-8') as file:
        data = file.readlines()
        new_data = []
        for line in data:
            if line != '\n' and str(user_id) not in line:
                new_data.append(line)
            else:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=True,
                                         can_send_media_messages=True,
                                         can_send_polls=True,
                                         can_send_other_messages=True,
                                         can_change_info=True,
                                         can_invite_users=True,
                                         can_pin_messages=True)
    with open("unverifed_users.txt", 'w', encoding='utf-8') as file:
        for line in new_data:
            file.write(line + '\n')


def mute_user(bot: TeleBot, message: Message):
    '''
    Блокирует пользователю отправку каких-либо сообщений на указанное время.
    Если время не указанно - блокирует на 5 минут.

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`
    :param bot: Telebot
    :return: None
    '''
    user_id = message.reply_to_message.from_user.id
    id_who_call = message.from_user.id
    admins = bot.get_chat_administrators(message.chat.id)
    time = 300
    admins_ids = []
    for admin in admins:
        admins_ids.append(admin.user.id)
    if id_who_call in admins_ids and user_id not in admins_ids:
        if len(message.text.lower().split()) >= 2:
            time = 60 * int(message.text.lower().split()[1])
        mute_until = datetime.datetime.now() + datetime.timedelta(seconds=time)
        bot.restrict_chat_member(message.chat.id,
                                 user_id,
                                 can_send_messages=None,
                                 can_send_media_messages=None,
                                 can_send_polls=None,
                                 can_send_other_messages=None,
                                 can_change_info=None,
                                 can_invite_users=None,
                                 can_pin_messages=None,
                                 until_date=mute_until
                                 )
        bot.reply_to(message, text=f'Пользователь будет молчать {time/60} минут')

    elif id_who_call in admins_ids and user_id in admins_ids:
        bot.reply_to(message, 'Пользователь которого вы пытаетесь ограничить - является админом чата.\n'
                              'Команда не выполнена.\nРазберитесь между собою в лс.')
    else:
        bot.reply_to(message, 'Вы не являетесь админом чата. Команда не будет выполнена')


def kick_user(bot: TeleBot, message: Message):
    '''
    Удаляет пользователя из группы. Пользователь сможет вернуться в группу.

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`
    :param bot: Telebot
    :return: None
    '''
    user_id = message.reply_to_message.from_user.id
    id_who_call = message.from_user.id
    admins = bot.get_chat_administrators(message.chat.id)
    admins_ids = []
    for admin in admins:
        admins_ids.append(admin.user.id)
    if id_who_call not in admins_ids:
        bot.reply_to(message, 'Вы не админ чата. Команда не будет выполнена')
    elif id_who_call in admins_ids and user_id in admins_ids:
        bot.reply_to(message, 'Это админ группы.\nКоманда не выполнена.\nРазберитесь между собою в лс.')
    elif id_who_call in admins_ids and user_id not in admins_ids:
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, 'Пользователь покинул чат.')


def ban_user(bot: TeleBot, message: Message):
    '''
    Удаляет пользователя из группы и болирует возможность вступить в группу.
    Пользователь не сможет вернуться в группу.

    :param message: Optional. New incoming message of any kind - text, photo, sticker, etc.
    :type message: :class:`telebot.types.Message`
    :param bot: Telebot
    :return: None
    '''
    user_id = message.reply_to_message.from_user.id
    id_who_call = message.from_user.id
    admins = bot.get_chat_administrators(message.chat.id)
    admins_ids = []
    for admin in admins:
        admins_ids.append(admin.user.id)
    if id_who_call not in admins_ids:
        bot.reply_to(message, 'Вы не админ чата. Команда не будет выполнена')
    elif id_who_call in admins_ids and user_id in admins_ids:
        bot.reply_to(message, 'Это админ группы.\nКоманда не выполнена.\nРазберитесь между собою в лс.')
    elif id_who_call in admins_ids and user_id not in admins_ids:
        bot.ban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, 'Пользователь покинул чат.')