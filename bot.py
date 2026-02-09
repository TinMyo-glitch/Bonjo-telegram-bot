# အပေါ်ဆုံးမှာ ဒါလေး ထည့်ထားပါ
# Update Version: 1.1

# ... import အပိုင်းများ ...

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

# --- Video Player စနစ် ---
def render_video_page(m3u8_url):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <style>body {{ margin: 0; background: #000; }} video {{ width: 100vw; height: 100vh; }}</style>
    </head>
    <body>
        <video id="video" controls autoplay></video>
        <script>
          var video = document.getElementById('video');
          var videoSrc = "{m3u8_url}";
          if (Hls.isSupported()) {{
            var hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
          }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
            video.src = videoSrc;
          }}
        </script>
    </body>
    </html>
    '''

# --- Web App လမ်းကြောင်းများ (ခလုတ်ထဲက နာမည်တွေနဲ့ ကိုက်ညီအောင် ပြင်ထားသည်) ---
@app.route('/ch1')
def mwd_channel():
    return render_video_page("http://203.81.84.130/hls/mwd_serie/index.m3u8")

@app.route('/ch2')
def arirang_channel():
    return render_video_page("http://amdlive.ctnd.com.edgesuite.net/arirang_1ch/smil:arirang_1ch.smil/playlist.m3u8")

@app.route('/ch3')
def cnn_channel():
    return render_video_page("https://live.cnnindonesia.com/livecnn/smil:cnntv.smil/playlist.m3u8")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Bot အပိုင်း ---
TOKEN = '8298038885:AAFibdgnkESK4UVuEmYWUj-Hjo7Mm5B_rbc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    base_url = "https://bonjo1-telegram-bot.onrender.com"
    
    # URL လမ်းကြောင်းများကို အပေါ်က app.route အတိုင်း /ch1, /ch2, /ch3 ပေးထားသည်
    btn1 = types.InlineKeyboardButton(text="📺 TVM (MWD)", web_app=types.WebAppInfo(url=f"{base_url}/ch1"))
    btn2 = types.InlineKeyboardButton(text="📺 Arirang Korea", web_app=types.WebAppInfo(url=f"{base_url}/ch2"))
    btn3 = types.InlineKeyboardButton(text="📺 CNN Indonesia", web_app=types.WebAppInfo(url=f"{base_url}/ch3"))
    
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, "ကြည့်ရှုလိုသည့် Channel ကို ရွေးပါ-", reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
