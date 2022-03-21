import keyboard as keyboard
from django.core.management.base import BaseCommand
import telebot;
from telebot import types
from Bot import views
bot = telebot.TeleBot('5277263469:AAF5QhoRLb2mATz92atasY-KkHv7U-FfdOU')


class Command(BaseCommand):
    help = 'help'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    news_button = types.KeyboardButton("Новости")
    proposal_button = types.KeyboardButton("Жалобы/предложения")
    admission_button = types.KeyboardButton("Заказать пропуск")
    workers_button = types.KeyboardButton("Вызов сотрудника ЖКХ")
    counters_button = types.KeyboardButton("Счетчики")
    contacts_button = types.KeyboardButton("Контакты ☎")
    keyboard=["Новости", "Жалобы/предложения", "Заказать пропуск", "Вызов сотрудника ЖКХ", "Счетчики", "Контакты ☎"]
    def __init__(self):
        self.markup.add(self.news_button, self.proposal_button, self.admission_button,
                        self.workers_button, self.counters_button, self.contacts_button)

    def handle(self, *args, **options):
        @bot.message_handler(commands=['start'])
        def start(message, res=False):
            if not views.auth(message.from_user.username):
                bot.send_message(message.from_user.id, "Вы не зарегестрированы!")
            bot.send_message(message.chat.id, text='Меню', reply_markup=self.markup)
        @bot.message_handler(content_types=['text'])
        def callback_worker(message):
            print(message.from_user.username, views.auth(message.from_user.username))
            if not views.auth(message.from_user.username):
                bot.send_message(message.from_user.id, "Вы не зарегестрированы!")
            else:
                if message.text == "Новости":
                    news = views.get_last_news()
                    bot.send_message(message.from_user.id, news, reply_markup=self.markup)
                elif message.text == "Жалобы/предложения":
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton("Написать новую", callback_data='create_new_proposal')
                    )
                    keyboard.row(
                        telebot.types.InlineKeyboardButton("Просмотреть уже поданные", callback_data='get_proposals')
                    )
                    bot.send_message(message.chat.id, text='Жалобы/предложения', reply_markup=keyboard)

                elif message.text == "Заказать пропуск":
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    carTypes = views.get_car_types()
                    for i in carTypes:
                        keyboard.row(
                            telebot.types.InlineKeyboardButton(i.name, callback_data='get_car_types%s' % i.id)
                        )
                    bot.send_message(message.chat.id, text='Выберите тип машины', reply_markup=keyboard)


                elif message.text == "Вызов сотрудника ЖКХ":
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    spec=views.get_specialities()
                    for i in spec:
                        keyboard.row(
                            telebot.types.InlineKeyboardButton(i.name, callback_data='get_employee%s' % i.id)
                        )
                    bot.send_message(message.chat.id, text='Сотрудники ЖКХ', reply_markup=keyboard)

                elif message.text == "Счетчики":
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton("Подать показания", callback_data='save_counters')
                    )
                    keyboard.row(
                        telebot.types.InlineKeyboardButton("Просмотреть показания", callback_data='get_counters')
                    )
                    bot.send_message(message.chat.id, text='Показания счетчиков', reply_markup=keyboard)


                elif message.text == "Контакты ☎":
                    get_contacts(message)

                else:
                    bot.send_message(message.from_user.id, "Я Вас не понимаю. Выберите пункт меню", reply_markup=self.markup)

        @bot.callback_query_handler(func=lambda call: True)
        def get_callback(query):
            if query.data == 'create_new_proposal':
                keyboard = telebot.types.InlineKeyboardMarkup()
                urgencies = views.get_urgencies()
                for i in urgencies:
                    keyboard.row(
                        telebot.types.InlineKeyboardButton(i.name, callback_data='get_urgency%s' % i.id)
                    )
                bot.send_message(query.message.chat.id, text='Выберите срок действия пропуска', reply_markup=keyboard)

            if 'get_urgency' in query.data:
                set_urgency(query.message, query.data[-1])

            if query.data == 'get_proposals':
                get_proposals(query)

            if 'get_employee' in query.data:
                save_employee_calling(query.message, query.data[-1])

            if query.data == 'get_counters':
                get_counters(query.message)

            if query.data == 'save_counters':
                save_counters(query.message)

            if 'get_car_types' in query.data:
                set_carType_admission(query.message, query.data[-1])

            if 'get_timeLimits' in query.data:
                set_carNumber_admission(query.message,timeLimit=query.data[-2], carType=query.data[-1] )

      # -------------------------------------Proposals
        def set_urgency(message, urgency):
            bot.send_message(message.chat.id, "Опишите жалобу", reply_markup=self.markup)
            bot.register_next_step_handler(message, create_proposal, urgency=urgency)

        def create_proposal(message, **kwargs):
            if not message.text in self.keyboard:
                resp = views.create_proposal(message, kwargs)
                bot.send_message(message.chat.id, resp, reply_markup=self.markup)
            else:
                callback_worker(message)

        def get_proposals(query):
            my_props = views.get_proposals(query.from_user.username)
            for p in my_props:
                bot.send_message(query.message.chat.id, p, reply_markup=self.markup)

        # -----------------------------------Admission

        def set_carType_admission(message, carType):
            if not message.text in self.keyboard:
                if carType == '3':
                    set_fio_admission(message, carType=carType)
                else:
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    timeLimits = views.get_time_limits_types()
                    for i in timeLimits:
                        keyboard.row(
                            telebot.types.InlineKeyboardButton(i.name, callback_data='get_timeLimits%s%s' % (i.id, carType))
                        )
                    bot.send_message(message.chat.id, text='Выберите срок действия пропуска', reply_markup=keyboard)
            else:
                callback_worker(message)



        def set_carNumber_admission(message, **kwargs):
            if not message.text in self.keyboard:
                bot.send_message(message.chat.id, "Напишите номер автомобиля (если есть)", reply_markup=self.markup)
                bot.register_next_step_handler(message, set_fio_admission,
                                               timeLimit=kwargs['timeLimit'],
                                               carType=kwargs['carType']
                                               )
            else:
                callback_worker(message)

        def set_fio_admission(message, **kwargs):
            if kwargs['carType']=='3':
                bot.send_message(message.chat.id, "Напишите ФИО", reply_markup=self.markup)
                bot.register_next_step_handler(message, set_comments_admission, carType=kwargs['carType'])

            else:
                bot.send_message(message.from_user.id, "Напишите ФИО", reply_markup=self.markup)
                bot.register_next_step_handler(message, set_comments_admission,
                                               timeLimit=kwargs['timeLimit'],
                                               carType=kwargs['carType'],
                                               carNumber=message.text
                                               )



        def set_comments_admission(message, **kwargs):
            if not message.text in self.keyboard:
                bot.send_message(message.from_user.id, "Напишите комментарии(если имеются)", reply_markup=self.markup)
                if kwargs['carType']=='3':
                    bot.register_next_step_handler(message, create_admission,
                                                   fio=message.text,
                                                   carType=kwargs['carType']
                                                   )
                else:
                    bot.register_next_step_handler(message, create_admission,
                                                   timeLimit=kwargs['timeLimit'],
                                                   carType=kwargs['carType'],
                                                   carNumber=kwargs['carNumber'],
                                                   fio=message.text
                                                   )

            else:
                callback_worker(message)

        def create_admission(message, **kwargs):
            if not message.text in self.keyboard:
                kwargs['comment'] = message.text
                resp = views.create_admission(kwargs, message.from_user.username)
                bot.send_message(message.from_user.id, resp, reply_markup=self.markup)
            else:
                callback_worker(message)


        # -----------------------------------Employee_call
        def save_employee_calling(message, employeeId):
            if not message.text in self.keyboard:
                resp = views.save_employee_calling(message, employeeId)
                bot.send_message(message.chat.id, resp, reply_markup=self.markup)
            else:
                callback_worker(message)

        # -----------------------------------Counters
        def get_counters(message):
            resp=views.get_counters(message.chat.username)
            bot.send_message(message.chat.id, resp, reply_markup=self.markup)

        def save_counters(message):
            bot.send_message(message.chat.id, "Напишите показания счетчика горячей воды", reply_markup=self.markup)
            bot.register_next_step_handler(message, save_hotWater_counter)

        def save_hotWater_counter(message):
            if not message.text in self.keyboard:
                try:
                    int(message.text)
                    views.save_HotWater_counters(message.text, message.from_user.username)
                    bot.send_message(message.from_user.id, "Напишите показания счетчика холодной воды", reply_markup=self.markup)
                    bot.register_next_step_handler(message, save_coldWater_counter)
                except:
                    bot.send_message(message.from_user.id, "Ошибка! Введите число!", reply_markup=self.markup)
                    save_counters(message)
            else:
                callback_worker(message)


        def save_coldWater_counter(message):
            if not message.text in self.keyboard:
                try:
                    int(message.text)
                    resp = views.save_ColdWater_counters(message.text, message.from_user.username)
                    bot.send_message(message.from_user.id, resp, reply_markup=self.markup)

                except:
                    bot.send_message(message.from_user.id, "Ошибка! Введите число!", reply_markup=self.markup)
                    message.text=1
                    save_counters(message)
            else:
                callback_worker(message)



        # -----------------------------------Contacts
        def get_contacts(message):
            resp=views.get_contacts()
            bot.send_message(message.from_user.id, resp, reply_markup=self.markup)

        bot.polling(none_stop=True, interval=0)
