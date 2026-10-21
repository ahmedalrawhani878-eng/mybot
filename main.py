import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# قائمة الأيدي الخاصة بالمشرفين المسموح لهم بإدارة البوت والنشر (رقمك أنت حالياً)
ADMIN_IDS = [8860646306]  # سنضيف أيدي المندوبة غداً هنا

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📢 الإعـلانـات", "📚 المحاضرات والملخصات"],
        ["📅 جدول المحاضرات", "📝 الاختبارات التدريبية"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك في بوت مجتمع طلاب الأمن السيبراني - جامعة الاتحاد (إب - اليمن) 🛡\n\nاختر من الأزرار أدناه للبدء:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # التحقق مما إذا كان المستخدم يضغط على الأزرار العادية
    if text == "📢 الإعـلانـات":
        await update.message.reply_text("هنا قسم الإعلانات والتعاميم الخاصة بالجامعة 📢")
    elif text == "📚 المحاضرات والملخصات":
        await update.message.reply_text("هنا تجد كافة المحاضرات والملخصات الدراسية 📚")
    elif text == "📅 جدول المحاضرات":
        await update.message.reply_text("هنا جدول المحاضرات ومواعيد الاختبارات 📅")
    elif text == "📝 الاختبارات التدريبية":
        await update.message.reply_text("هنا تجد الاختبارات التدريبية لاختبار معلوماتك 📝")
    else:
        # هنا يتم حماية البوت: إذا أرسل أي شخص عادي رسالة أو ملف وليس مشرفاً
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("عذراً، هذا البوت مخصص لعرض محتوى طلاب الأمن السيبراني وللمشرفين فقط 🛡")
        else:
            await update.message.reply_text("أهلاً بك يا مهندس/ة، تم استلام رسالتك بصفتك مشرفاً في البوت ✨")

def main():
    TOKEN = "8826493490:AAENCMKbIwDs2i4sj2cWDLvhGn5GbB_7oj4"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت يعمل الآن بصلاحيات المشرفين وجاهز...")
    app.run_polling()

if __name__ == "__main__":
    main()
