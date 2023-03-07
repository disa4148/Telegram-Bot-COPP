import telebot
import re


from telebot import types


bot = telebot.TeleBot('5826445945:AAGwHbEk5eklQu7BIOwszG84EALhWrzmCJw')

#global name, surname, email, age, number
name = ''
surname = ''
email = ''
age = 0
number = 0
int(number)
int(age)

def get_name(message):  # Получение имени пользователя
    global name
    name = message.text

    if (len(name)) >= 2:
        if (len(name)) < 20:
            if any(char.isdigit() for char in name):  # Проверка на цифры в имени
                bot.send_message(message.from_user.id, 'Имя не должно содержат цифр, попробуйте ввести ещё раз',
                                 parse_mode='html')
                bot.register_next_step_handler(message, get_name)
            else:
                bot.send_message(message.from_user.id, 'Введите вашу фамилию', parse_mode='html')
                bot.register_next_step_handler(message, get_surname)
        else:
            bot.send_message(message.from_user.id, 'Имя слишком длинное, попробуйте ввести ещё раз',
                             parse_mode='html')
            bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Имя слишком короткое, попробуйте ввести ещё раз', parse_mode='html')
        bot.register_next_step_handler(message, get_name)

def get_surname(message):  # Получение фамилии пользователя
    global surname
    surname = message.text

    if (len(surname)) >= 2:
        if (len(surname)) < 60:
            if any(char.isdigit() for char in surname):
                bot.send_message(message.from_user.id,
                                 'Фамилия не должна содержать цифр, попробуйте ввести ещё раз',
                                 parse_mode='html')
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

def get_number(self, message):  # Получение номера телефона пользователя
    global number
    number = message.text
    pattern = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                       number)

    if (bool(pattern)) == True:
        bot.send_message(message.from_user.id, 'Введите адрес электронной почты', parse_mode='html')
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.from_user.id, 'Введите данные корректно', parse_mode='html')
        bot.register_next_step_handler(message, get_number)

def get_email(self, message):  # Получение эл.почты пользователя
    global email
    email = message.text
    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"

    if bool(re.match(pattern, email)) == True:  # Ищет по шаблону (Pattern) значение строки (email)
        bot.send_message(message.from_user.id, 'Введите ваш возраст?', parse_mode='html')
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, 'Введите данные корректно',
                         parse_mode='html')
        bot.register_next_step_handler(message, get_email)

def get_age(self, message):  # Получение возраста пользователя, проверка на правильность заполнения полей
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Да ✅', callback_data='True'))
    keyboard.add(types.InlineKeyboardButton(text='Нет ❌', callback_data='False'))

    global age
    age = int(message.text)

    question = 'Верно ли заполнены поля?\n\nВаше имя: ' + name + '\nВаша фамилия: ' + surname + '\nНомер телефона: ' + "+ " + str(
          number) + '\nАдрес эл. почты: ' + email + '\nВаш возраст: ' + str(age)
    bot.send_message(message.from_user.id, question, parse_mode='html', reply_markup=keyboard)
