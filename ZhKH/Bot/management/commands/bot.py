from django.core.management.base import BaseCommand
from Bot.models import News, Proposal
import telebot;
from telebot import types
from Bot import views
bot = telebot.TeleBot('5277263469:AAF5QhoRLb2mATz92atasY-KkHv7U-FfdOU')

class Command(BaseCommand):
    help = 'help'
    def handle(self, *args, **options):
        @bot.message_handler(commands=['menu'])
        def start(message, res=False):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            news_button = types.KeyboardButton("Новости")
            proposal_button = types.KeyboardButton("Подать жалобу/предложение")
            admission_button = types.KeyboardButton("Пропуск на машину/курьера")
            workers_button = types.KeyboardButton("Вызов рабочих")
            markup.add(news_button, proposal_button, admission_button, workers_button)
            bot.send_message(message.chat.id, text='Меню', reply_markup=markup)
        @bot.message_handler(content_types=['text'])
        def callback_worker(message):
            if message.text == "Новости":
                news=views.get_last_news()
                bot.send_message(message.from_user.id, news)
            elif message.text == "Подать жалобу/предложение":
                bot.send_message(message.from_user.id, "Опишите жалобу")
                bot.register_next_step_handler(message, save_prop)
            else:
                bot.send_message(message.from_user.id, "Я Вас не понимаю. Введите '/menu' и выберите пункт меню")

        def save_prop(mes):
            proposal=views.create_proposal(mes.text)
            bot.send_message(mes.from_user.id, proposal)
            bot.send_message(mes.chat.id, text='Меню', reply_markup=markup)
        bot.polling(none_stop=True, interval=0)
