import os
from flask import Flask
from threading import Thread

# Flask App ဆောက်ခြင်း
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot logic ရဲ့ အရှေ့မှာ ထည့်ပါ
keep_alive()

# ဒီအောက်မှာ bot.infinity_polling() ကို ဆက်ထားပါ
