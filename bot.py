  import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

# --- خادم HTTP الوهمي لإبقاء الخدمة نشطة على Render ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# ----------------------------------------------------

# ضع التوكن الصحيح الخاص بك هنا
TOKEN = '8798616483:AAEFanIBQDxbxlO9TZ5rpOByLumX8HInL1o'
CHANNEL_USERNAME = '@PK1TASKEARNHUB'
ADMIN_ID = 8804323255

bot = telebot.TeleBot(TOKEN)

users = {}
referrals = {}

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if not check_subscription(user_id):
        bot.reply_to(
            message,
            f"❌ لا يمكنك استخدام البوت إلا بعد الاشتراك في قناتنا أولاً:\n"
            f"🔗 {CHANNEL_USERNAME}\n\n"
            f"بعد الاشتراك، قم بإرسال الأمر /start مجدداً."
        )
        return

    if user_id not in users:
        users[user_id] = {'count': 0}

    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        
        if referrer_id != user_id and user_id not in referrals:
            referrals[user_id] = referrer_id
            
            if referrer_id in users:
                users[referrer_id]['count'] += 1
            else:
                users[referrer_id] = {'count': 1}

            try:
                bot.send_message(
                    referrer_id,
                    f"🎉 مبروك! انضم مستخدم جديد عبر رابطك 👤\n"
                    f"👤 اسم المدعو: {user_name}\n"
                    f"📊 إجمالي إحالاتك الناجحة: {users[referrer_id]['count']}"
                )
            except:
                pass

            try:
                bot.send_message(
                    ADMIN_ID,
                    f"🚨 [إحالة جديدة ناجحة]\n"
                    f"👤 الداعي (ID): `{referrer_id}`\n"
                    f"👥 المدعو: {user_name} (`{user_id}`)\n"
                    f"📈 إجمالي إحالات الداعي: {users[referrer_id]['count']}"
                )
            except Exception as e:
                print(f"Failed to send admin notification: {e}")

    ref_link = f"https://t.me/PK_Task_New_bot?start={user_id}"
    
    welcome_text = (
        f"Welcome to the Referral Bot! 🇵🇰💰\n\n"
        f"Your Referral Link:\n{ref_link}\n\n"
        f"Share this link with your friends to earn referrals!"
    )

    if len(args) > 1 and args[1].isdigit():
        welcome_text += f"\n\n✅ تم تسجيل إحالتك بنجاح!"

    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    count = users.get(user_id, {}).get('count', 0)
    bot.reply_to(message, f"📊 Your Referral Count: {count}")

@bot.message_handler(commands=['menu', 'help'])
def send_menu(message):
    menu_text = (
        f"🤖 **قائمة البوت الرئيسية**\n\n"
        f"• /start - بدء استخدام البوت والتسجيل\n"
        f"• /menu - عرض قائمة الأوامر المتاحة\n"
        f"• /stats - معرفة عدد إحالاتك"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")

print("Bot is running stably...")
# استخدام الطريقة التقليدية الآمنة بعد إيقاف أي تكرار سابق
bot.infinity_polling(skip_pending=True)
