from telegram.ext import Updater, CommandHandler
import os
from telegram import Update
from django.http import HttpResponse
import requests




# khởi tạo đối tượng Updater và Dispatcher
updater = Updater(token='6262155674:AAGHWtp6WL2ZqDYqCeBX8Uvi479OEgorFUk', use_context=True)
dispatcher = updater.dispatcher

# định nghĩa hàm xử lý command /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a bot!")

def today(update, context):
    response = requests.get('http://linhtrangbridal.online/gettodaycart/')
    total_cart = response.json()['total_cart']
    total_paid = response.json()['total_paid']
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Báo cáo hôm nay, tổng doanh thu {total_cart}, tổng tiền thu {total_paid }")

 
# đăng ký command handler cho command /start
start_handler1 = CommandHandler('start', start)
start_handler2 = CommandHandler('today', today)
dispatcher.add_handler(start_handler1)
dispatcher.add_handler(start_handler2)

# start polling để nhận tin nhắn từ người dùng
updater.start_polling()