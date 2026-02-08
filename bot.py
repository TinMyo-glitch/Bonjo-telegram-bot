import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- Render အတွက် မအိပ်အောင် လုပ်တဲ့အပိုင်း ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

TOKEN = '8298038885:AAFibdgnkESK4UVuEmYWUj-Hjo7Mm5B_rbc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('/LIVE_1')
    btn2 = types.KeyboardButton('/m3u')
    btn3 = types.KeyboardButton('/LIVE_2')
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, "မင်္ဂလာပါ! Render မှ ကြိုဆိုပါတယ်၊", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == '/LIVE_1':
        bot.send_message(message.chat.id, "Link 1: https://t.me/example")
    elif message.text == '/m3u':
        bot.send_message(message.chat.id, "M3U Link: https://t.me/example")

if __name__ == "__main__":
    keep_alive() # Web Server ကို အရင်နှိုးမယ်
    bot.infinity_polling() # ပြီးမှ Bot ကို Run မယ်
