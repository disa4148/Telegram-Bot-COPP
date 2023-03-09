import telebot
import re
import xlsxwriter
import EmailSender
import json


from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект
from telebot import types

KeyboardRemove = telebot.types.ReplyKeyboardRemove()
bot = telebot.TeleBot('5826445945:AAGwHbEk5eklQu7BIOwszG84EALhWrzmCJw')

user_status = 'unauthorized'
name = ''
surname = ''
email = ''
age = 0 
number = 0
int(number)
int(age)


addr_from = "koly.bessonov.2004@mail.ru"
addr_to = "Koskova@mail.ru"

msg = MIMEMultipart()
msg['From'] = addr_from
msg['To'] = addr_to
msg['Subject'] = "Тестовая отправка Exel"

body = "А вот тебе и Exel:)"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Добро пожаловать в телеграмм бот ЦОПП Кузбасса!\n\n" +
    "Мы занимаемся:\n\n" +
    "✅ Выявлением наиболее востребованных в регионе профессий;\n\n" +
    "✅ Разработкой единых подходов к образовательным программам для всех категорий граждан;\n\n" +
    "✅ Содействием центрам занятости в поиске соискателей для актуальных вакансий; \n\n" +
    "✅ Информированием работодателей и работников о проектах рынка труда;\n\n"+
    "✅ Защитой интеллектуальной собственности;\n\n"+
    "✅ Организацией и проведением профориентационных работ в регионе;\n\n"+
    "✅ Вопросами международного сотрудничества;\n\n"+
    "✅ Организацией и проведением деловых встреч и мероприятий", parse_mode='html')
    get_menu(message)

def get_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Записаться на курс 👨‍💻", callback_data='course'))
    keyboard.add(types.InlineKeyboardButton(text="Наши контакты 🌍", callback_data='contacts'))

    bot.send_message(message.from_user.id, "Выберите категорию:", parse_mode='html', reply_markup=keyboard )

@bot.message_handler(commands=['course']) #Список доступных курсов
def list_courses(message):
    if user_status == 'authorized':
        #bot.send_message(message.from_user.id, "Список доступных курсов:  ", parse_mode='html')
        count = 10
        page = 1
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                   types.InlineKeyboardButton(text=f'Вперёд --->',
                                              callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                  page + 1) + ",\"CountPage\":" + str(count) + "}"))

        bot.send_message(message.from_user.id, "Привет!!!", reply_markup=markup)

    else:
        bot.send_message(message.from_user.id, "Смотреть список курсов могут только <b>авторизованные</b> пользователи.\n\n " +
                                               "Воспользуйтесь командой /reg для прохождения регистрации", parse_mode='html')

@bot.message_handler(commands=['reg']) #Начало процедуры регистрации
def start_reg(message):
    if user_status == 'unauthorized':
        bot.send_message(message.from_user.id, "Введите ваше имя", parse_mode='html', reply_markup=KeyboardRemove)
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Вы уже авторизованы", parse_mode='html', reply_markup=KeyboardRemove)


def get_name(message): #Получение имени пользователя
    global name
    name = message.text

    if (len(name)) >= 2:
        if (len(name)) < 20:
            if any(char.isdigit() for char in name): #Проверка на цифры в имени
                bot.send_message(message.from_user.id, 'Имя не должно содержат цифр\n\n Попробуйте ввести ещё раз', parse_mode='html')
                bot.register_next_step_handler(message, get_name)
            else:
                bot.send_message(message.from_user.id, 'Введите вашу фамилию', parse_mode='html')
                bot.register_next_step_handler(message, get_surname)
        else:
            bot.send_message(message.from_user.id, 'Имя слишком длинное\n\n Попробуйте ввести ещё раз', parse_mode='html')
            bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Имя слишком короткое\n\n Попробуйте ввести ещё раз', parse_mode='html')
        bot.register_next_step_handler(message, get_name)

def get_surname(message): #Получение фамилии пользователя
    global surname
    surname = message.text

    if (len(surname)) >= 2:
        if (len(surname)) < 60:
            if any(char.isdigit() for char in surname):
                bot.send_message(message.from_user.id,
                                 'Фамилия не должна содержать цифр, попробуйте ввести ещё раз', parse_mode='html')
                bot.register_next_step_handler(message, get_surname)
            else:
                bot.send_message(message.from_user.id, 'Введите номер телефона', parse_mode='html')
                bot.register_next_step_handler(message, get_number)
        else:
            bot.send_message(message.from_user.id, 'Фамилия слишком длинная, попробуйте ввести ещё раз',
                             parse_mode='html')
            bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(message.from_user.id, 'Фамилия слишком короткая, попробуйте ввести ещё раз',
                         parse_mode='html')
        bot.register_next_step_handler(message, get_surname)

def get_number(message): #Получение номера телефона пользователя
    global number
    number = message.text
    pattern = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', number)

    if (bool(pattern)) == True:
        bot.send_message(message.from_user.id, 'Введите адрес электронной почты', parse_mode='html')
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.from_user.id, 'Введите коррекнтые данные', parse_mode='html')
        bot.register_next_step_handler(message, get_number)

def get_email(message): #Получение эл.почты пользователя
    global email
    email = message.text
    email_validate_pattern = r"^\S+@\S+\.\S+$"

    if bool(re.match(email_validate_pattern, email)) == True:  # Ищет по шаблону (regex) значение строки (email)
        bot.send_message(message.from_user.id, 'Введите ваш возраст?', parse_mode='html')
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, 'Введите корректные данные', parse_mode='html')
        bot.register_next_step_handler(message, get_email)

def get_age(message): #Получение возраста пользователя, проверка на правильность заполнения полей
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Да ✅', callback_data='True'))
    keyboard.add(types.InlineKeyboardButton(text='Нет ❌', callback_data='False'))
    
    global age
    age = message.text
    question = 'Верно ли заполнены поля?\n\nВаше имя: ' + name + '\nВаша фамилия: ' + surname + '\nНомер телефона: ' + "+ " + str(number) + '\nАдрес эл. почты: ' + email + '\nВаш возраст: ' + str(age)
    bot.send_message(message.from_user.id, question, parse_mode='html', reply_markup=keyboard)






@bot.callback_query_handler(func=lambda call: True)
def callback_reply(call):
    global user_status
    if call.data:
        if call.data == 'course':
            if user_status == 'unauthorized':
                bot.send_message(call.from_user.id, 'Для записи на курс необходимо пройти регистрацию \n\nЗарегистрироваться можно здесь: <b>https://platform.copp42.ru/registration</b>\n\n Для регистрации в <b>Telegram</b> напишите <b>/reg</>',parse_mode='html')
            elif user_status == 'authorized':
                 list_courses(call)
        elif call.data == 'contacts':
            bot.send_message(call.from_user.id, 'Контакты: \n\n' +
                             "📍 650021, г.Кемерово, ул.Павленко, 1а\n\n" +
                             "📞 +7 (3842) 57-11-20 \n📞 +7 (3842) 57-11-14\n\n" +
                             "✉  copp42@yandex.ru\n\n" +
                             "Режим работы:\n\n" +
                             "Пн-Пт 8:30-17:00\nСб 8:30-14:00\nВс-выходной\n" +
                             "Социальные сети: \n\n" +
                             "Вконтакте: \nhttps://vk.com/copp42kuzbass \n\n" +
                             "Одноклассники: \nhttps://ok.ru/copp42kuzbass \n\n" +
                             "Telegram канал: \nhttps://t.me/copp42 \n\n" +
                             "Youtube канал: \n\nhttps://www.youtube.com/channel/UCn2HyuY_HBUy9L75sqx0qcw",
                             parse_mode='html', reply_markup=KeyboardRemove)

        elif call.data == 'True':

            bot.send_message(call.from_user.id, 'Все успешно заполнено 👏 \n\nВы можете ознакомиться с курсами с помощью команды <b> /course </b>', parse_mode='html')
            user_status = 'authorized'

            Collected_Data = (['Имя', name], ['Фамилия', surname], ['Номер телефона', number], ['Адрес эл. почты', email], ['Возраст', age])
            workbook = xlsxwriter.Workbook('C:/Users/2/Desktop/Collected_info_user.xlsx')
            worksheet = workbook.add_worksheet("Лист 1")

            for i, (item, information) in enumerate(Collected_Data, start=1):
                worksheet.write(f'A{i}', item)
                worksheet.write(f'B{i}', information)
            workbook.close()

#            files = ["C:/Users/2/Desktop/Collected_info_user.xlsx"]

#           EmailSender.send_email(addr_to, "Test Exel", "А вот и текст:)", files)  # Почта находится в файле ForEmail.py

        elif call.data == 'False':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn_return_to_start = types.KeyboardButton("/reg")
            markup.add(btn_return_to_start)
            bot.send_message(call.from_user.id, 'Нажми кнопку <b>"/reg"</b> для возврата назад', parse_mode='html', reply_markup=markup)




    #Для пагнинации

        req = call.data.split('_')
        # Обработка кнопки - скрыть
        if req[0] == 'unseen':
            bot.delete_message(call.message.chat.id, call.message.message_id)
        # Обработка кнопок - вперед и назад
        elif 'pagination' in req[0]:
            # Расспарсим полученный JSON
            json_string = json.loads(req[0])
            count = json_string['CountPage']
            page = json_string['NumberPage']
            # Пересоздаем markup
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            # markup для первой страницы
            if page == 1:
                markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           types.InlineKeyboardButton(text=f'Вперёд --->',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page + 1) + ",\"CountPage\":" + str(count) + "}"))
            # markup для второй страницы
            elif page == count:
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page - 1) + ",\"CountPage\":" + str(count) + "}"),
                           types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
            # markup для остальных страниц
            else:
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page - 1) + ",\"CountPage\":" + str(count) + "}"),
                           types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           types.InlineKeyboardButton(text=f'Вперёд --->',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page + 1) + ",\"CountPage\":" + str(count) + "}"))
#           bot.edit_message_text(f'Страница {page} из {count}', reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.edit_message_text("Наши мероприятия:\n" +
                                  " ", reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

"""""
def get_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Записаться на курс 👨‍💻", callback_data='course'))
    keyboard.add(types.InlineKeyboardButton(text="Наши контакты 🌍", callback_data='contacts'))

    bot.send_message(message.from_user.id, "Выберите категорию:", parse_mode='html', reply_markup=keyboard )

@bot.callback_query_handler(func=lambda call: True)
def callback_reply(call):
    if call.data:
        if call.data == 'course':
            bot.send_message(call.from_user.id, 'Для записи на курс необходимо пройти регистрацию \n\nЗарегистрироваться можно здесь: <b>https://platform.copp42.ru/registration</b>\n\n Для регистрации в <b>Telegram</b> напишите <b>/reg</>', parse_mode='html')
        elif call.data == 'contacts':
            bot.send_message(call.from_user.id, 'Контакты)', parse_mode='html')
"""""
bot.polling(none_stop=True)