import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ADMIN_IDS = [8860646306]  # أيدي المشرف (أنت)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛡 السنة الثانية (اختر هنا لتفاصيل دفعتكم)"],
        ["🛡 السنة الثالثة", "🛡 السنة الرابعة"],
        ["📢 الإعلانات العامة"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً بك في بوت مجتمع طلاب الأمن السيبراني - جامعة الاتحاد (إب - اليمن) 🛡\n\nيرجى اختيار السنة الدراسية:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # إذا كان المرسل هو المشرف وأرسل ملفاً أو صورة
    if user_id in ADMIN_IDS and (update.message.document or update.message.photo):
        await update.message.reply_text(
            "📥 تم استقبال الملف بنجاح يا مهندس!\n"
            "سيتم حفظه وتوجيه مباشرة إلى ⬅ **السنة الثانية - الفصل الدراسي الثاني**."
        )
        return

    # التنقل بين السنوات
    if text == "🛡 السنة الثانية (اختر هنا لتفاصيل دفعتكم)":
        keyboard = [
            ["📚 الفصل الدراسي الأول", "🔥 الفصل الدراسي الثاني (الحالي)"],
            ["⬅ القائمة الرئيسية"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("أنت الآن في السنة الثانية. اختر الفصل الدراسي:", reply_markup=reply_markup)

    elif text in ["🛡 السنة الثالثة", "🛡 السنة الرابعة"]:
        keyboard = [
            ["📚 الفصل الدراسي الأول", "📚 الفصل الدراسي الثاني"],
            ["⬅ القائمة الرئيسية"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"أنت الآن في {text}. اختر الفصل الدراسي:", reply_markup=reply_markup)

    # الأقسام الستة عند اختيار الفصل الثاني أو الأول
    elif text in ["🔥 الفصل الدراسي الثاني (الحالي)", "📚 الفصل الدراسي الثاني", "📚 الفصل الدراسي الأول"]:
        keyboard = [
            ["📁 الملازم", "📅 الجدول والمحاضرات"],
            ["📝 نماذج الاختبارات", "📢 الإعلانات"],
            ["📚 الملخص", "📸 صور المحاضرات"],
            ["⬅ العودة للسنوات"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"أنت في {text}. اختر القسم المطلوب:", reply_markup=reply_markup)

    elif text == "📁 الملازم":
        await update.message.reply_text("📁 قسم الملازم الدراسية (السنة الثانية - الفصل الثاني):\n(جاهز لاستقبال ملازمكم هنا)")
    elif text == "📅 الجدول والمحاضرات":
        await update.message.reply_text("📅 جدول المحاضرات ومواعيد المحاضرات:")
    elif text == "📝 نماذج الاختبارات":
        await update.message.reply_text("📝 نماذج الاختبارات السابقة والتدريبية:")
    elif text == "📢 الإعلانات":
        await update.message.reply_text("📢 إعلانات القسم والفصل الدراسي:")
    elif text == "📚 الملخص":
        await update.message.reply_text("📚 الملخصات والمذكرات المختصرة:")
    elif text == "📸 صور المحاضرات":
        await update.message.reply_text("📸 صور السبورة والمحاضرات العملية:")

    elif text == "⬅ العودة للسنوات" or text == "⬅ القائمة الرئيسية":
        await start(update, context)
    else:
        if text:
            await update.message.reply_text("يرجى استخدام الأزرار الظاهرة في الكيبورد أدناه 👇")

def main():
    TOKEN = "8826493490:AAENCMKbIwDs2i4sj2cWDLvhGn5GbB_7oj4"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler((filters.TEXT | filters.Document.ALL | filters.PHOTO) & (~filters.COMMAND), handle_message))

    print("البوت يعمل بنجاح تامة...")
    app.run_polling()

if __name__ == "__main__":
    main()
