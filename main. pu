import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📢 الإعـلانـات"],
        ["📚 المحاضرات والملخصات"],
        ["📅 جدول المحاضرات والاختبارات"],
        ["📝 الاختبارات التدريبية"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك في بوت مجتمع طلاب الأمن السيبراني - جامعة الاتحاد 🛡\n\nهنا تجد الإعلانات، المحاضرات والملخصات، جدول المحاضرات والاختبارات، والاختبارات التدريبية.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📢 الإعـلانـات":
        await update.message.reply_text("هنا قسم الإعلانات والتعاميم الخاصة بالجامعة 📢")
    elif text == "📚 المحاضرات والملخصات":
        await update.message.reply_text("هنا تجد كافة المحاضرات والملخصات الدراسية 📚")
    elif text == "📅 جدول المحاضرات والاختبارات":
        await update.message.reply_text("هنا جدول المحاضرات ومواعيد الاختبارات 📅")
    elif text == "📝 الاختبارات التدريبية":
        await update.message.reply_text("هنا تجد الاختبارات التدريبية لاختبار معلوماتك 📝")
    else:
        await update.message.reply_text("يرجى اختيار أحد الأزرار الموجودة في الكيبورد أدناه 👇")

def main():
    TOKEN = "8980115075:AAEzEh6DcrI8nr6RgL3dtstj21pXOjGeVxc"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت يعمل الآن وجاهز لاستقبال الرسائل...")
    app.run_polling()

if __name__ == "__main__":
    main()
