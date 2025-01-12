import sqlite3
import random



def play_process(message, bot):
    game_words = ["спасибо","погладить", "почесать спинку", "спс","мой авторитет", "сяб", "пасибо", "пасяб", "спс", "поженимся", "чпок", "-", "+", "+++", "благодарю", "спиздить",
                     "обчистить", "украсть", "обокрасть", "пнуть", "обнять", "обнимашки", "скрасть", "отпиздить",
                     "опустить", "пнуть", "поцеловать", "поцелуй", "чмок", "целовашки", "подарить", "пожертвовать", "унизить", "зачмырить", "своровать","затискать", "потискать"]
    phrase = ""
    photo = None
    robber, victim = checking_users(message, bot)
    if message.text == "+" or message.text == "+++" or message.text == "спасибо" or message.text == "спс" or message.text == "сяб" or message.text == "пасибо" or message.text == "пасяб" or message.text == "спс" or message.text == "благодарю":
        robber, victim, phrase = thanks_giving(robber,victim, phrase)
    elif message.text == "-":
        robber, victim, phrase = negative_giving(robber, victim, phrase)
    elif message.text == "украсть" or message.text == "скрасть" or message.text == "спиздить" or message.text == "обокрасть" or message.text == "обчистить" or message.text == "своровать":
        robber, victim, phrase = attempted_theft(robber, victim, phrase)
    elif message.text == "пнуть" or message.text == "опустить" or message.text == "отпиздить" or message.text == "унизить" or message.text == "зачмырить":
        robber, victim, phrase = kicking(robber, victim, phrase)
    elif message.text == "обнять" or message.text == "обнимашки" or message.text == "затискать" or message.text == "потискать":
        robber, victim, phrase, photo = hugging(robber, victim, phrase, photo)
    elif message.text == "поцеловать" or message.text == "поцелуй" or message.text == "чмок" or message.text == "целовашки":
        robber, victim, phrase, photo = kissing(robber, victim, phrase, photo)
    elif message.text == "пожертвовать" or message.text == "подарить":
        robber, victim, phrase = gifting(robber, victim, phrase)
    elif message.text == "погладить" or message.text == "почесать спинку":
        robber, victim, phrase = catting(robber, victim, phrase, message.text)
    elif message.text == "мой авторитет":
        robber, phrase = asking_status(robber, phrase, message)
    elif message.text == "чпок":
        robber, victim, phrase = try_fuck(robber, victim, phrase)
    saving_res(robber, victim, phrase, message)
    return message, phrase, photo





def checking_users(message, bot):
    robber = [message.from_user.id, message.from_user.username, message.from_user.last_name, message.from_user.first_name]
    victim = []
    if message.reply_to_message is not None:
        victim = [message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,message.reply_to_message.from_user.last_name, message.reply_to_message.from_user.first_name]
    else:
        admins = bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            if admin.status == 'creator':
                victim = [admin.user.id, admin.user.username, admin.user.last_name, admin.user.first_name]
    with sqlite3.connect("game.db") as con:
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS '{message.chat.id}' (user_id INTEGER NOT NULL, username TEXT, lastname TEXT, firstname TEXT, stolen INTEGER NOT NULL DEFAULT 100, credibility INTEGER NOT NULL DEFAULT 10, status TEXT, married TEXT NOT NULL DEFAULT 'не в браке')")
        cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE user_id == {robber[0]}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO '{message.chat.id}' (user_id, username, lastname, firstname, stolen, credibility, status, married) VALUES ({robber[0]}, '{robber[1]}', '{robber[2]}', '{robber[3]}', 100, 10, 'первосезонник', 'не в браке')")
            con.commit()
        else:
            cursor.execute(f"UPDATE '{message.chat.id}' SET username = '{robber[1]}', lastname = '{robber[2]}', firstname = '{robber[3]}' WHERE user_id = {robber[0]}")
            con.commit()
        cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE user_id = {victim[0]}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO '{message.chat.id}' (user_id, username, lastname, firstname, stolen, credibility, status, married) VALUES ({victim[0]}, '{victim[1]}', '{victim[2]}','{victim[3]}', 100, 10, 'первосезонник', 'не в браке')")
            con.commit()
        else:
            cursor.execute(f"UPDATE '{message.chat.id}' SET username = '{victim[1]}', lastname = '{victim[2]}', firstname = '{victim[3]}' WHERE user_id = {victim[0]}")
            con.commit()
        robber = list(cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE user_id == {robber[0]}").fetchone())
        victim = list(cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE user_id == {victim[0]}").fetchone())
    return robber, victim

def set_status(score):
        if -60 < score <= -39:
            status = "нубасик"
        elif -40 <= score <= 19:
            status = "Новичок на двух колесах"
        elif -20 <= score <= 0:
            status = "Постепенно осваивающийся"
        elif 0 < score <= 20:
            status = "Первосезонник"
        elif 20 < score <= 59:
            status = "Уверенный на дороге"
        elif 60 <= score < 100:
            status = "Опытный гонщик"
        elif 100 <= score < 150:
            status = "Мастер мотоциклизма"
        elif 150 <= score < 200:
            status = "Ветеран двухколесного мира"
        elif score >= 200:
            status = "Легенда мотоциклизма"
        return status

def thanks_giving(robber, victim, phrase):
    if robber[0] == victim[0]:
        phrase = " Хватит мастурбировать при всех!!!!"
    elif victim[0] == 6026030050:
        phrase = "Спасибо. Я это ценю."
    else:
        victim[5] += 1
        victim[6] = set_status(victim[5])
        phrase = f"Авторитет {victim[3]} повышен.\n{victim[3]} \U0001F3C5 : {victim[5]}"
    return robber, victim , phrase

def negative_giving(robber, victim, phrase):
    if robber[0] == victim[0]:
        phrase = "Смотрите-ка сам себе пинка отвесить умудрился! Мазохист какой-то"
    elif victim[0] == 6026030050:
        phrase = "Это несправедливо. За что?!"
    else:
        victim[5] -= 1
        victim[6] = set_status(victim[5])
        phrase = f"Авторитет {victim[3]} понижен.\n{victim[3]} \U0001F3C5 : {victim[5]}"
    return robber, victim, phrase

def attempted_theft(robber, victim, phrase): # проверить на сам себя
    trying = random.randint(1, 11)
    modificator = random.randint(1, 15)
    if trying > 5:
        if victim[4] > modificator:
            victim[4] -= modificator
            robber[4] += modificator
            phrase = f"{robber[3]} украл у {victim[3]} \u2699{modificator}  \n{robber[3]} +\u2699{modificator}\n{victim[3]} -\u2699{modificator}\n{robber[3]} {robber[4]} : \u2699\n{victim[3]}  {victim[4]} : \u2699"
        elif victim[4] == modificator or 0 < victim[4] < modificator:
            modificator = victim[4]
            robber[4] += modificator
            victim[4] = 0
            phrase = f"{robber[3]} обнес дочиста {victim[3]}\n{robber[3]} +\u2699{modificator}\n{victim[3]} -\u2699{modificator}\n{robber[3]}  {robber[4]} : \u2699\n{victim[3]}  {victim[4]} : \u2699"
        else:
            phrase = f"{robber[3]} пытался обокрасть {victim[3]}.Да только красть у него нечего.\n{robber[3]}  {robber[4]} : \u2699\n{victim[3]}  {victim[4]} : \u2699"
    else:
        phrase = "Даже воровать ты не умеешь. Кража не удалась"
    return robber, victim, phrase

#для каждого действия создаем отдельную функцию, и надо разобраться с генератором фраз
def kicking(robber, victim, phrase):
    trying = random.randint(1, 11)
    modificator = random.randint(1, 15)
    if robber[0] == victim[0]:
        phrase = "Ну, как бы если тебе хочется пинать самого себя - никто не против. Забавное надо сказать зрелище."
    elif victim[0] == 6026030050:
        robber[5] -= 50
        robber[6] = set_status(robber[5])
        phrase = f"Ты на кого клешню пытаешься поднять, мешок кожанный?!\n{robber[3]}  \U0001F3C5{robber[5]} \n{robber[3]} \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}"
    else:
        if trying > 8:
            victim[5] -= modificator
            victim[6] = set_status(victim[5])
            robber[5] += modificator
            robber[6] = set_status(robber[5])
            phrase = f"{robber[3]} пнул {victim[3]}.\n{robber[3]} +{modificator}\U0001F3C5 / {victim[3]} -{modificator}\U0001F3C5. \n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}\n{victim[3]}  \U0001F3CD : {victim[6]} \U0001F3C5 : {victim[5]}"
        elif 3 < trying <= 8:
            phrase = f"{robber[3]} пытался пнуть {victim[3]}. Но из этого ничего не вышло.\n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}\n{victim[3]} \U0001F3CD : {victim[6]} \U0001F3C5 : {victim[5]}"
        else:
            robber[5] -= modificator / 2
            robber[6] = set_status(robber[5])
            victim[5] += modificator / 2
            victim[6] = set_status(victim[5])
            phrase = f"{robber[3]} пытался пнуть {victim[3]}. Но поскользнулся и только задницу себе отбил\n {robber[3]} \U0001F3CD{robber[6]} \U0001F3C5{robber[5]} / {victim[3]} \U0001F3CD{victim[6]} {victim[5]}"
    return robber, victim, phrase

def kissing(robber, victim, phrase, photo):
    if victim[0] == 6026030050:
        photo = open("hug.jpg", 'rb')
        phrase = f"{robber[3]} поцеловал {victim[3]}. Ммммм, целовашчки!\n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}\n{victim[3]}  \U0001F3CD : {victim[6]} \U0001F3C5 : {victim[5]}"
    elif victim[0] == robber[0]:
        robber[5] += 5
        robber[6] = set_status(robber[5])
        phrase = f"Лови воздушный поцелуйчик.\n{robber[3]}  \U0001F3C5 : +5\n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}"
    else:
        victim[5] += 7
        victim[6] = set_status(victim[5])
        phrase = f"{robber[3]} поцеловал {victim[3]}. Целовашечки это здорово.\n{victim[3]}  \U0001F3C5 : +7\n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}\n{victim[3]} \U0001F3CD : {victim[6]} \U0001F3C5 : {victim[5]}"
    return robber, victim, phrase, photo

def hugging(robber, victim, phrase, photo):
    if victim[0] == 6026030050:
        photo = open("hug.jpg", 'rb')
        phrase = f"{robber[3]} обнял {victim[3]}. Обнимашки это так мило.\n{robber[3]}  \U0001F3CD : {robber[6]} \U0001F3C5 : {robber[5]}\n{victim[3]}  \U0001F3CD : {victim[6]} \U0001F3C5 : {victim[5]}"
    elif victim[0] == robber[0]:
        robber[5] += 3
        robber[6] = set_status(robber[5])
        phrase = f"Бедняжка.Иди ко мне я тебя обниму.\nСуза обняла {robber[3]}\n{robber[3]} : \U0001F3C5 : +3\n{robber[3]} \U0001F3CD{robber[6]} \U0001F3C5{robber[5]}"
    else:
        victim[5] += 5
        victim[6] = set_status(victim[5])
        phrase = f"{robber[3]} обнял {victim[3]}. Обнимашки это так мило.\n{robber[3]} \U0001F3CD{robber[6]} \U0001F3C5{robber[5]} / {victim[3]} \U0001F3CD{victim[6]} \U0001F3C5{victim[5]}"
    return robber, victim, phrase, photo

def gifting(robber, victim, phrase):
    if victim[0] == 6026030050:
        victim[4] += 7
        robber[5] += 3
        robber[6] = set_status(robber[5])
        phrase = f"{robber[3]} подарил Сузе 7 \u2699.Спасибо за подарочек). Очень приятно.\nАвторитет {robber[3]} повышен, а {victim[3]} получил немножко запчастей для мототайки.\n{robber[3]} \U0001F3C5 : {robber[5]}\n{victim[3]} \u2699 : {victim[4]}"
    elif robber[0] == victim[0]:
        phrase = "Радовать подарками самого себя обязательно надо!"
    else:
        victim[4] += 7
        robber[5] += 3
        robber[6] = set_status(robber[5])
        phrase = f"{robber[3]} подарил {victim[3]} 7 \u2699.\nАвторитет {robber[3]} повышен, а {victim[3]} получил немножко запчастей для мототайки.\n{robber[3]} \U0001F3C5 : {robber[5]}\n{victim[3]} \u2699 : {victim[4]}"
    return robber, victim, phrase

def catting(robber, victim, phrase, text):
    cat_names = ["кот", "котик", "котейка", "котэ", "котя", "котофей", "котяра", "cat", "kot", "koteika", "kitty", "cote"]
    if text == "погладить":
        action_text = "погладил котика"
    else:
        action_text = "почесал котику спинку"
    if str(victim[2]).lower() in cat_names or str(victim[3]).lower() in cat_names:
        if robber[0] == victim[0]:
            victim[5] -= 2
            victim[6] = set_status(victim[5])
            phrase = f"Кот хватит вылизывать яйца при всех! \n{victim[3]} \U0001F3CD{victim[6]} \U0001F3C5{victim[5]}"
        else:
            victim[5] += 5
            victim[6] = set_status(victim[5])
            robber[5] += 5
            robber[6] = set_status(robber[5])
            phrase = f"{robber[3]} {action_text} ({victim[3]}). Оба получили удовольствие ).\n{robber[3]} \U0001F3CD{robber[6]} \U0001F3C5{robber[5]} / {victim[3]} \U0001F3CD{victim[6]} \U0001F3C5{victim[5]}"
    return robber, victim, phrase

def try_fuck(robber,victim, phrase):
    phrase = "Прям здесь что ли? При всех?? Совсем сдурел что ли??? 0_0"
    return robber, victim, phrase

def wedding(robber, victim):
    # keybMarry = types.InlineKeyboardMarkup(row_width=3)
    # btnMarried = types.InlineKeyboardButton(text="Да", callback_data=f"married {victim[0]} {robber[0]}")
    # btnNotMarried = types.InlineKeyboardButton(text="Нет", callback_data=f"notmarried {victim[0]} {robber[0]}")
    # keybMarry.add(btnMarried, btnNotMarried)
    # if robber[7] != "":
    #     bot.reply_to(message, "Куда это ты???! Ты уже в браке! Ишь че тут удумали!")
    # elif victim[7] != "":
    #     bot.reply_to(message, "Твой объект воздыхания уже в браке. Прими мои соболезнования.")
    # else:
    #     msg = bot.reply_to(message, f"{robber[0]}/{robber[1]}/{robber[2]} {robber[3]}\nПредлагает тебе создать ячейку общества. Согласишься?", reply_markup=keybMarry)
    #     time.sleep(120)
    #     bot.delete_message(msg.chat.id,msg.id)
    pass

def asking_status(robber, phrase, message):
    with sqlite3.connect("game.db") as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM '{message.chat.id}' WHERE user_id = {robber[0]}")
        robber = cursor.fetchone()
        phrase = f"{robber[0]}/{robber[1]}/{robber[2]} {robber[3]}\nТвой статус:\nЗапчасти: \U0001F3CD{robber[4]}\nАвторитет: \U0001F3C5 : {robber[5]}  \U00002699 : {robber[6]}\n{robber[7]}"
    return robber, phrase


def saving_res(robber, victim, phrase, message):
    with sqlite3.connect("game.db") as con:
        cursor = con.cursor()
        cursor.execute(f"UPDATE '{message.chat.id}' SET username = '{robber[1]}', lastname = '{robber[2]}', firstname = '{robber[3]}', stolen = {robber[4]}, credibility = {robber[5]}, status = '{robber[6]}', married = '{robber[7]}' WHERE user_id = {robber[0]}")
        con.commit()
        if robber[0] != victim[0]:
            cursor.execute(f"UPDATE '{message.chat.id}' SET username = '{victim[1]}', lastname = '{victim[2]}', firstname = '{victim[3]}', stolen = {victim[4]}, credibility = {victim[5]}, status = '{victim[6]}', married = '{victim[7]}' WHERE user_id = {victim[0]}")
            con.commit()
