import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["قائمة الخيارات 1", "قائمة الخيارات 2"],
        ["المساعدة", "تواصل معنا"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك يا بطل! تم تشغيل البوت بنجاح 🚀\nاختر من الأزرار المربعة أدناه:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "قائمة الخيارات 1":
        await update.message.reply_text("لقد اخترت القائمة الأولى بنجاح! 📋")
    elif text == "قائمة الخيارات 2":
        await update.message.reply_text("لقد اخترت القائمة الثانية بنجاح! 📂")
    elif text == "المساعدة":
        await update.message.reply_text("هذا بوت تجريبي تم برمجته لأجلك لتسهيل الاستخدام.")
    elif text == "تواصل معنا":
        await update.message.reply_text("يمكنك التواصل معنا عبر التيليجرام في أي وقت.")
    else:
        await update.message.reply_text(f"أنت كتبت: {text}")

def main():
    TOKEN = "8980115075:AAEzEh6DcrI8nr6RgL3dtstj21pXOjGeVxc"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت يعمل الآن وجاهز لاستقبال الرسائل...")
    app.run_polling()

if __name__ == "__main__":
    main()
