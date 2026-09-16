import telebot

# ضع هنا توكن بوتك الخاص
TOKEN = '8798616483:AAFn-JI8WuVS3yoOhisIeCNvb8GHGWSvDek'

# معرف قناتك (يجب أن يكون البوت مشرفاً فيها)
CHANNEL_USERNAME = '@PK1TASKEARNHUB'

# رقم الآيدي الشخصي الخاص بك لتصلك تقارير الإحالات عليه
ADMIN_ID = 8804323255

bot = telebot.TeleBot(TOKEN)

users = {}
referrals = {}

# دالة للتحقق من الاشتراك في القناة
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # 1. فحص الاشتراك الإجباري
    if not check_subscription(user_id):
        bot.reply_to(
            message,
            f"❌ عذراً، يجب عليك الاشتراك في قناتنا أولاً لتتمكن من استخدام البوت:\n"
            f"🔗 {CHANNEL_USERNAME}\n\n"
            f"بعد الاشتراك، قم بإرسال الأمر /start مجدداً."
        )
        return

    # تسجيل المستخدم الجديد إذا لم يكن مسجلاً
    if user_id not in users:
        users[user_id] = {'count': 0}

    # 2. فحص نظام الإحالة
    args = message.text.split()
    if len(args) > 1:
        referrer_id = args[1]
        if referrer_id.isdigit():
            referrer_id = int(referrer_id)
            # التأكد أن الداعي ليس هو نفس الشخص وأن الداعي مسجل
            if referrer_id != user_id and referrer_id in users:
                if user_id not in referrals:
                    referrals[user_id] = referrer_id
                    users[referrer_id]['count'] += 1
                    
                    # إشعار الداعي (صديقك)
                    try:
                        bot.send_message(
                            referrer_id, 
                            f"🎉 مبروك! انضم شخص جديد وعضو في القناة عبر رابطك.\n"
                            f"👤 اسم المدعو: {user_name}\n"
                            f"📊 إجمالي إحالاتك الناجحة: {users[referrer_id]['count']}"
                        )
                    except:
                        pass

                    # إشعار الأدمن (أنت) بتقرير كامل عن العملية
                    try:
                        bot.send_message(
                            ADMIN_ID,
                            f"🚨 [تقرير إحالة جديد]\n"
                            f"👤 الداعي (ID): {referrer_id}\n"
                            f"👥 المدعو: {user_name} (ID: {user_id})"
                        )
                    except Exception as e:
                        print(f"Failed to send admin notification: {e}")

    # إنشاء رابط الإحالة الخاص بالمستخدم الحالي
    ref_link = f"https://t.me/PK_Task_New_bot?start={user_id}"

    welcome_text = (
        "Welcome to the Referral Bot! 🇵🇰 💰\n\n"
        f"Your Referral Link:\n{ref_link}\n\n"
        "Share this link with your friends to earn referrals!"
    )
    
    if len(args) > 1 and args[1].isdigit() and int(args[1]) in users and int(args[1]) != user_id:
        welcome_text += f"\n\n✅ شكراً لاشتراكك، وتم احتساب إحالتك بنجاح!"

    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    count = users.get(user_id, {}).get('count', 0)
    bot.reply_to(message, f"📊 Your Referral Stats:\n\nTotal successful referrals: {count}")
# تعيين قائمة الأوامر التي تظهر للمستخدمين في زر Menu
@bot.message_handler(commands=['menu', 'help'])
def send_menu(message):
    menu_text = (
        "🤖 **قائمة أওয়াْمِر البوت الرئيسية:**\n\n"
        "▫️ /start - بدء استخدام البوت وتسجيل الدخول\n"
        "▫️ /menu - عرض قائمة الأوامر المتاحة\n"
        "▫️ للحصول على رابط الإحالة الخاص بك، استخدم الأزرار داخل البوت."
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")
    
print("Bot is running with full features...")
bot.infinity_polling()
