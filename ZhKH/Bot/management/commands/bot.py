from django.core.management.base import BaseCommand
from Bot.models import News, Proposal
import telebot;
bot = telebot.TeleBot('5277263469:AAF5QhoRLb2mATz92atasY-KkHv7U-FfdOU')

class Command(BaseCommand):
    help = 'help'
    def handle(self, *args, **options):
        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.text == "Новости":
                news = News.objects.all()
                bot.send_message(message.from_user.id, news)
            elif message.text == "Жалоба":
                bot.send_message(message.from_user.id, "Опишите жалобу")
                bot.register_next_step_handler(message, get_zhaloba)
            else:
                bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши11 /help.")
        def get_zhaloba(message):
            Proposal.objects.create(title='zhaloba',text=message)
        bot.polling(none_stop=True, interval=0)
