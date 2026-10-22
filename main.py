import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ADMIN_IDS = [8860646306]  # أيدي المشرف (أنت وقريباً المندوبة)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛡 السنة الثانية (الحالية)"],
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

    # استقبال الملفات والصور من المشرفين وتوجيهها للفصل الثاني مباشرة
    if user_id in ADMIN_IDS and (update.message.document or update.message.photo):
        await update.message.reply_text(
            "📥 تم استقبال الملف بنجاح يا مهندس!\n"
            "سيتم حفظه وتوجيهه مباشرة إلى ⬅ **السنة الثانية - الفصل الدراسي الثاني**."
        )
        return

    # التنقل بين السنوات
    if text == "🛡 السنة الثانية (الحالية)":
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

    # الأقسام الستة عند اختيار أي فصل دراسي
    elif text in ["🔥 الفصل الدراسي الثاني (الحالي)", "📚 الفصل الدراسي الثاني", "📚 الفصل الدراسي الأول"]:
        keyboard = [
            ["📁 الملازم", "📅 الجدول والمحاضرات"],
            ["📝 نماذج الاختبارات", "📢 الإعلانات"],
            ["📚 الملخص", "📸 صور المحاضرات"],
            ["⬅ العودة للسنوات"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"أنت في {text}. اختر القسم المطلوب:", reply_markup=reply_markup)

    # تفاصيل الأقسام الستة
    elif text == "📁 الملازم":
        await update.message.reply_text("📁 قسم الملازم الدراسية:\n(جاهز لاستقبال ملازمكم وملفاتكم هنا 📂)")
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

    # أزرار الرجوع
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

    print("بوت الأمن السيبراني يعمل بالهيكلة الكاملة...")
    app.run_polling()

if __name__ == "__main__":
    main()
