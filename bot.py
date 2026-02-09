import telebot
from telebot import types
import os
from flask import Flask, send_from_directory
from threading import Thread

# --- Render အတွက် Web Server နှင့် HTML ဖိုင်ချိတ်ဆက်ခြင်း ---
app = Flask(__name__)

@app.route('/')
def home():
    # ဒီစာကြောင်းက index.html ကို Web App အဖြစ် ပြသပေးမှာပါ
    return send_from_directory('.', 'index.html')

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------------

# Bot Token ကို သေချာပြန်ထည့်ပါ (ကော်လံ : ပါရမည်)
TOKEN = '8298038885:AAFibdgnkESK4UVuEmYWUj-Hjo7Mm5B_rbc' 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Render ကပေးထားတဲ့ သင့် Bot ရဲ့ URL ကို ဒီမှာ အမှန်ပြင်ထည့်ပါ
    # ဥပမာ - https://bonjo-telegram-bot.onrender.com
    my_web_url = "https://bonjo-telegram-bot.onrender.com"
    
    # Web App ခလုတ်
    web_app = types.WebAppInfo(url=my_web_url)
    btn_live = types.InlineKeyboardButton(text="⚽ LIVE တိုက်ရိုက်ကြည့်ရန်", web_app=web_app)
    
    # အရင်က ရှိခဲ့တဲ့ သာမန် Reply ခလုတ်တွေအစား Inline ခလုတ်ကို သုံးထားတာပါ
    markup.add(btn_live)
    
    bot.reply_to(message, "မင်္ဂလာပါ! အောက်ကခလုတ်ကိုနှိပ်ပြီး Live Stream ကြည့်နိုင်ပါတယ်-", reply_markup=markup)

# အခြား Message တွေကို လက်ခံတဲ့အပိုင်း (Optional)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Live ကြည့်ချင်ရင် /start ကို နှိပ်ပါခင်ဗျာ။")

if __name__ == "__main__":
    keep_alive() # Web Server နှိုးခြင်း
    print("Bot is starting...")
    bot.infinity_polling() # Bot စတင် Run ခြင်း
