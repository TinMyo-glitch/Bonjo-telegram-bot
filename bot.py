# အသစ်ပြန်ပတ်မည်
import telebot
from telebot import types
import os
from flask import Flask, send_from_directory
from threading import Thread

# --- Render အတွက် Web Server နှင့် HTML ဖိုင်ချိတ်ဆက်ခြင်း ---
app = Flask(__name__)
@app.route('/ch1')
def channel1():
    # TVM အတွက် link ကို source ထဲမှာ ထည့်ပါ
    link = "http://203.81.84.130/hls/mwd_serie/index.m3u8"
    return render_video_page(link)

@app.route('/Arirang_South_Korea')
def channel2():
    link = "http://amdlive.ctnd.com.edgesuite.net/arirang_1ch/smil:arirang_1ch.smil/playlist.m3u8"
    return render_video_page(link)

@app.route('/CNN INDONESIA HD')
def channel3():
    link = "https://live.cnnindonesia.com/livecnn/smil:cnntv.smil/chunklist_w596222982_b384000_sleng.m3u8"
    return render_video_page(link)

def render_video_page(m3u8_url):
    # HTML ကို code ထဲမှာတင် တိုက်ရိုက် ရေးလိုက်တာ ပိုမြန်ပါတယ်
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
        <style>body {{ margin: 0; background: #000; }} .video-js {{ width: 100vw; height: 100vh; }}</style>
    </head>
    <body>
        <video id="v" class="video-js vjs-default-skin" controls autoplay preload="auto">
            <source src="{m3u8_url}" type="application/x-mpegURL">
        </video>
        <script src="https://vjs.zencdn.net/7.20.3/video.js"></script>
    </body>
    </html>
    '''

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
    
    # Render URL (သင့် URL ကို အမှန်ပြင်ရန်)
    base_url = "https://your-bot-name.onrender.com"
    
    # TVM ခလုတ်
    web_app1 = types.WebAppInfo(url=f"{base_url}/TVM")
    btn1 = types.InlineKeyboardButton(text="📺 TVM ကြည့်ရန်", web_app=web_app1)
    
    # Arirang_South_Korea ခလုတ်
    web_app2 = types.WebAppInfo(url=f"{base_url}/Arirang_South_Korea")
    btn2 = types.InlineKeyboardButton(text="📺 Arirang_South_Korea ကြည့်ရန်", web_app=web_app2)
    
    # CNN INDONESIA HD ခလုတ်
    web_app3 = types.WebAppInfo(url=f"{base_url}/CNN INDONESIA HD")
    btn3 = types.InlineKeyboardButton(text="📺 CNN INDONESIA HD ကြည့်ရန်", web_app=web_app3)
    
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, "ကြည့်ရှုလိုသည့် Channel ကို ရွေးချယ်ပါ-", reply_markup=markup)

# အခြား Message တွေကို လက်ခံတဲ့အပိုင်း (Optional)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Live ကြည့်ချင်ရင် /start ကို နှိပ်ပါခင်ဗျာ။")

if __name__ == "__main__":
    keep_alive() # Web Server နှိုးခြင်း
    print("Bot is starting...")
    bot.infinity_polling() # Bot စတင် Run ခြင်း
