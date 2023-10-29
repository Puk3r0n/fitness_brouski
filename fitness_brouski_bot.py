import requests
import telebot
from telebot import types

bot = telebot.TeleBot("6330441813:AAFfQk2EGb10grHrm63BaEIcScYNxC7j7IA")
user_data = "PLACEHOLDER"
TexT = ''
a = ''

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести физические данные")

    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        text="Доброго времени суток {0.username}! Я помогу тебе)".format(message.from_user),
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def func(message):
    global user_info
    global user_data

    if message.text == "Ввести физические данные":
        phys_data(message)

    elif message.text == "Мои параметры":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text=str(user_data), reply_markup=markup)

    elif message.text == "Я ввел данные":
        menu_2(message)

    elif message.text == "Индекс массы тела":
        indeks_massi(message)

    elif message.text == "Персональные данные":
        menu_2(message)

    elif message.text == "Назад":
        menu_3(message)

    elif message.text == "Калории":
        calories(message, user_info)

    elif message.text == "Диеты":
        dieti(message)


    else:
        bot.send_message(message.chat.id, text="БРО ты ошибся че то не то ввел")
        bot.register_next_step_handler(message, menu_2)


def phys_data(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, text="Мне нужна информация о тебе:", reply_markup=markup)
    btn1 = types.KeyboardButton("мужской")
    btn2 = types.KeyboardButton("женский")
    markup.add(btn1, btn2)
    sex_answer = bot.send_message(message.chat.id, text="Твой пол", reply_markup=markup)
    bot.register_next_step_handler(sex_answer, sex_otvetka)


def sex_otvetka(message):
    global user_info
    if message.text != "мужской" and message.text != "женский":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id,
                         text="Ты ввел некоректный пол, воспользуйся кнопками,"
                                               " я же не просто так их добавил",
                         reply_markup=markup)
        bot.register_next_step_handler(message, sex_otvetka)
    else:
        a = telebot.types.ReplyKeyboardRemove()
        age_answer = bot.send_message(message.chat.id,
                                      text="Какой у тебя возраст?",
                                      reply_markup=a)
        user_info = {"sex": message.text,
                     "id": message.chat.id}
        bot.register_next_step_handler(age_answer,
                                       age_otvetka,
                                       user_info)


def age_otvetka(message, user_info):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_info["age"] = message.text
    try:
        if int(user_info["age"]) > 70:
            bot.send_message(
                message.chat.id,
                text="Бро твои ровесники не знают что такое телега, кого ты обманываешь ?",
                reply_markup=markup,
            )
        height_answer = bot.send_message(
            message.chat.id, text="Какой у тебя рост?", reply_markup=markup
        )
        bot.register_next_step_handler(height_answer, height_otvetka, user_info)
    except ValueError:
        bot.send_message(
            message.chat.id, text="Пиши нормально черт(ток числовые значения)", reply_markup=markup
        )
        bot.register_next_step_handler(message, age_otvetka, user_info)


def height_otvetka(message, user_info):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_info["height"] = message.text
    try:
        if int(user_info["height"]) > 185:
            bot.send_message(message.chat.id, text="Самолеты не задевают ?\nЛадно шучу)")
        weight_answer = bot.send_message(message.chat.id, text="Твой вес?", reply_markup=markup)
        bot.register_next_step_handler(weight_answer, weight_otvetka, user_info)
    except ValueError:
        bot.send_message(
            message.chat.id, text="Пиши нормально черт(ток числовые значения)", reply_markup=markup
        )
        bot.register_next_step_handler(message, height_otvetka, user_info)


def proverka_vozrasta(user_info):
    if (
        (int(user_info["age"]) % 10 == 1)
        and (int(user_info["age"]) != 11)
        and (int(user_info["age"]) != 111)
    ):
        year = "год"
    elif (
        (int(user_info["age"]) % 10 > 1)
        and (int(user_info["age"]) % 10 < 5)
        and (int(user_info["age"]) != 12)
        and (int(user_info["age"]) != 13)
        and (int(user_info["age"]) != 14)
    ):
        year = "года"
    else:
        year = "лет"

    return year


def menu_2(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    item1 = types.KeyboardButton("Индекс массы тела")
    item2 = types.KeyboardButton("Мои параметры")
    item3 = types.KeyboardButton("Калории")
    back = types.KeyboardButton("Назад")
    markup.add(item1, item2, item3, back)

    bot.send_message(message.chat.id, "меню", reply_markup=markup)
    bot.register_next_step_handler(message, func)


def menu_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Персональные данные")
    btn2 = types.KeyboardButton("Диеты")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "главное меню", reply_markup=markup)


def indeks_massi(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        url = "https://fitness-calculator.p.rapidapi.com/bmi"

        querystring = user_info

        headers = {
            "X-RapidAPI-Key": "371c151a12msh30153b530a57321p176ffajsn8849dbe89160",
            "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)

        a = f'Индекс массы тела -> {response.json()["data"]["bmi"]} \nСостояние -> {response.json()["data"]["health"]}'

        bot.send_message(message.chat.id, text=a, reply_markup=markup)
        bot.send_photo(
            message.chat.id,
            "https://shilovo-med.medgis.ru/uploads/3c/bf/d1/dd"
            "/3cbfd1dd909dae37fa3d1b6248c2b520de7a46e9.jpg",
        )
    except KeyError:
        bot.register_next_step_handler(message, indeks_massi)


def chortik(message):
    global user_info
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(
        message.chat.id, text="Пиши нормально черт(ток числовые значения)", reply_markup=markup
    )
    bot.register_next_step_handler(message, weight_otvetka, user_info)


def vivod_calori(message):

    global user_info
    global dd

    if message.text == "Минимальная активность":
        cal = avg * 1.2
    elif message.text == "Слабый уровень активности":
        cal = avg * 1.375
    elif message.text == "Умеренный уровень активности":
        cal = avg * 1.55
    elif message.text == "Тяжелая активность":
        cal = avg * 1.7
    elif message.text == "Экстремальный уровень":
        cal = avg * 1.9
    elif message.text == "Легендарный уровень активности(для Юсуфа)":
        cal = avg * 1.62


    user_info['Kcal'] = cal
    bot.send_message(message.chat.id, text=f"Твоя суточноя норма каллорий:\n{cal}")


def weight_otvetka(message, user_info):
    global user_data
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    user_info["weight"] = message.text
    try:
        if int(user_info["weight"]) > 90:
            bot.send_message(
                message.chat.id, text="Нам предстоит очень много работы)", reply_markup=markup
            )
    except ValueError:
        chortik(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn3 = types.KeyboardButton("Я ввел данные")

    markup.add(btn3)

    user_data = (
        f'Данные сохранены: \n\n\nПол-> {user_info["sex"]} \nВозраст-> {user_info["age"]}'
        f' {proverka_vozrasta(user_info)} \nРост-> {user_info["height"]} см\n'
        f'Вес-> {user_info["weight"]} кг'
    )

    bot.send_message(message.chat.id, text=user_data, reply_markup=markup)

    bot.register_next_step_handler(message, func)


def calories(message, user_info):
    #Суточную норму каллорий буду считать по формуле Миффлина-Сан Жеора
    global user_data
    global avg
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("Минимальная активность")
    button2 = types.KeyboardButton("Слабый уровень активности")
    button3 = types.KeyboardButton("Умеренный уровень активности")
    button4 = types.KeyboardButton("Тяжелая активность")
    button5 = types.KeyboardButton("Экстремальный уровень")
    button6 = types.KeyboardButton("Легендарный уровень активности(для Юсуфа)")

    markup.add(button1, button2, button3, button4, button5, button6)

    bot.send_message(
        message.chat.id,
        "<b>Выбирете уровень активности</b>\n\n<b>Минимальная активность</b>:\n"
        "Cидячая работа, не требующая значительных "
        "физических нагрузок\n\n<b>Слабый уровень активности</b>:\n"
        "Интенсивные упражнения не менее 20 минут один-три раза в неделю. "
        "Это может быть езда на велосипеде, бег трусцой, баскетбол, плавание, "
        "катание на коньках и т. д. Если вы не тренируетесь регулярно, но сохраняете "
        "занятый стиль жизни, который требует частой ходьбы в течение длительного "
        "времени, то выберите этот коэффициент\n\n<b>Умеренный уровень активности</b>:"
        "\nИнтенсивная тренировка не менее 30-60 мин три-четыре раза в неделю "
        "(любой из перечисленных выше видов спорта)\n\n<b>Тяжелая активность</b>:"
        "\nИнтенсивные упражнения и занятия спортом 5-7 дней в неделю. Трудоемкие "
        "занятия также подходят для этого уровня, они включают строительные работы "
        "(кирпичная кладка, столярное дело и т. д.), занятость в сельском хозяйстве "
        "и т. п.\n\n"
        f"<b>Экстремальный уровень</b>:\nВключает чрезвычайно активные "
        f"и/или очень энергозатратные виды деятельности: занятия спортом с почти "
        f"ежедневным графиком и несколькими тренировками в течение дня; очень "
        f"трудоемкая работа, например, сгребание угля или длительный рабочий "
        f"день на сборочной линии. Зачастую этого уровня активности очень трудно "
        f"достичь.\n\n<b>Легендарный уровень активности(для Юсуфа):</b>\n"
        f"4 дня(вторник, среда, пятница, воскресенье,) по час 20"
        f"(после тренировки обязательно гейнер и "
        f"креатин!)",
        reply_markup=markup,
        parse_mode="html",
    )


    if user_info["sex"] == "мужской":
        avg = (
            10 * int(user_info["weight"])
            + 6.25 * int(user_info["height"])
            - 5 * int(user_info["age"])
            + 5
        )

    elif user_info["sex"] == "женский":
        avg = (
            10 * int(user_info["weight"])
            + 6.25 * int(user_info["height"])
            - 5 * int(user_info["age"])
            - 161
        )

    user_info['Kcal'] = 0


    user_data = (
        f'Данные сохранены: \n\n\nПол-> {user_info["sex"]} \nВозраст-> {user_info["age"]}'
        f' {proverka_vozrasta(user_info)} \nРост-> {user_info["height"]} см\n'
        f'Вес-> {user_info["weight"]} кг\nKcal-> {user_info["Kcal"]}'
    )

    bot.register_next_step_handler(message, vivod_calori)

    bot.register_next_step_handler(message, sohraneniye_cal)


def sohraneniye_cal(message):
    global user_data
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text="Coхраняем результат...", reply_markup=a)
    user_data = (
        f'Данные сохранены: \n\n\nПол-> {user_info["sex"]} \nВозраст-> {user_info["age"]}'
        f' {proverka_vozrasta(user_info)} \nРост-> {user_info["height"]} см\n'
        f'Вес-> {user_info["weight"]} кг\nСуточная норма-> {int(user_info["Kcal"])} калорий'
    )
    menu_2(message)


def dieti(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    btn1 = types.KeyboardButton("Сбалансированная")
    btn2 = types.KeyboardButton("Экспресс-диета")
    btn3 = types.KeyboardButton("Селективная")
    btn4 = types.KeyboardButton("Контрастная")
    btn5 = types.KeyboardButton("Натуропатическая")
    btn6 = types.KeyboardButton("Искусственная")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(
        message.chat.id,
        "<b>Выбирете диету</b>",
        reply_markup=markup,
        parse_mode="html"
    )

    bot.register_next_step_handler(message, vibor_dieti)


def vibor_dieti(message):
    global TexT
    global a

    if message.text == "Сбалансированная":
        TexT = '<a href="https://food.ru/articles/3270-chto-takoe-sbalansirovannoe-pitanie">' \
               'Сбалансированная Диета</a>'
    elif message.text == "Экспресс-диета":
        TexT = '<a href="https://www.thevoicemag.ru/health/diets/ekspress-dieta-na-3-5-7-dney-bystro-hudeem-posle-prazdnikov/">' \
               'Экспресс-диета</a>'
    elif message.text == "Селективная":
        TexT = '<a href="https://www.tiensmed.ru/fat12_3.html">' \
               'Селективная диета</a>'
    elif message.text == "Контрастная":
        TexT = '<a href="https://www.abcslim.ru/articles/1095/kontrastnye-diety-v-lechebnom-pitanii/">' \
               'Контрастная диета</a>'
    elif message.text == "Натуропатическая":
        TexT = '<a href="https://www.thesymbol.ru/lifestyle/travel/chto-nuzhno-znat-o-naturopaticheskoy-diete/">' \
               'Натуропатическая диета</a>'
    elif message.text == "Искусственная":
        TexT = '<a href="https://ru.wikipedia.org/wiki/%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5">' \
               'Искусственная диета</a>'

    bot.send_message(message.chat.id, TexT, parse_mode='HTML')
    menu_3(message)


bot.polling(none_stop=True)

bot.infinity_polling()