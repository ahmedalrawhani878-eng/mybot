import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# التوكن الصحيح والجاهز تماماً
TOKEN = "8826493490:AAENCMKbIwDs2i4sj2cWDLvhGn5GbB_7oj4"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- القائمة الرئيسية (تظهر في لوحة المفاتيح أسفل الكتابة) ---
def get_main_reply_keyboard():
    keyboard = [
        [KeyboardButton("📚 السنة الدراسية الأولى"), KeyboardButton("📚 السنة الدراسية الثانية (الحالية)")],
        [KeyboardButton("📚 السنة الدراسية الثالثة"), KeyboardButton("📚 السنة الدراسية الرابعة")],
        [KeyboardButton("📢 الإعلانات العامة"), KeyboardButton("ℹ️ عن البوت")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_main_reply_keyboard()
    await update.message.reply_text(
        "مرحباً بك يا مهندس في بوت اتحاد طلاب الأمن السيبراني - جامعة الاتحاد (إب).\nانقر على زر القائمة أسفل الشاشة لاختيار السنة الدراسية:",
        reply_markup=reply_markup
    )

# --- استقبال الضغط من لوحة المفاتيح أسفل الشاشة ---
async def handle_reply_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 السنة الدراسية الثانية (الحالية)":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="lvl2_sem1"),
             InlineKeyboardButton("الفصل الثاني (الحالي)", callback_data="lvl2_sem2")],
            [InlineKeyboardButton("🔙 إخفاء القائمة", callback_data="hide_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("اختر الفصل الدراسي للسنة الدراسية الثانية:", reply_markup=reply_markup)

    elif text in ["📚 السنة الدراسية الأولى", "📚 السنة الدراسية الثالثة", "📚 السنة الدراسية الرابعة"]:
        year_name = text
        keyboard = [[InlineKeyboardButton("🔙 إخفاء القائمة", callback_data="hide_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🛡 عذراً يا مهندس، محتوى **{year_name}** غير متوفر حالياً أو لم يتم رفع مواده بعد.\n\nترقبونا سيتم إضافته قريباً من قبل إدارة الاتحاد! تمنياتنا لكم بالتوفيق.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif text == "📢 الإعلانات العامة":
        await update.message.reply_text("📢 لا توجد إعلانات هامة في الوقت الحالي. تابعنا دائماً لمعرفة كل جديد!", reply_markup=ReplyKeyboardRemove())
    elif text == "ℹ️ عن البوت":
        await update.message.reply_text("🛡 بوت اتحاد طلاب الأمن السيبراني - جامعة الاتحاد (إب)\nمصمم لمساعدة طلاب الدفعات الدراسية في الوصول للملفات والمواد بكل سهولة.", reply_markup=ReplyKeyboardRemove())

# --- فصول السنة الثانية ---
async def levels_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "lvl2_sem2":
        keyboard = [
            [InlineKeyboardButton("إدارة مخاطر الأمن السيبراني", callback_data="sub_risk")],
            [InlineKeyboardButton("أساسيات التشفير", callback_data="sub_crypto")],
            [InlineKeyboardButton("تقنيات الويب", callback_data="sub_web")],
            [InlineKeyboardButton("نظم التشغيل", callback_data="sub_os")],
            [InlineKeyboardButton("إدارة وأمن قواعد البيانات", callback_data="sub_db")],
            [InlineKeyboardButton("التوجيه والتبديل في الشبكات", callback_data="sub_net")],
            [InlineKeyboardButton("ثقافة (2)", callback_data="sub_culture")],
            [InlineKeyboardButton("🔙 إخفاء القائمة", callback_data="hide_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 مواد السنة الثانية - الفصل الثاني:\nاختر المادة لعرض (نظري، عملي، تكاليف):", reply_markup=reply_markup)
    elif data == "lvl2_sem1":
        keyboard = [[InlineKeyboardButton("🔙 إخفاء القائمة", callback_data="hide_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 محتوى الفصل الأول للسنة الثانية قيد التحديث.", reply_markup=reply_markup)
    elif data == "hide_menu":
        await query.message.reply_text("تم إخفاء القائمة. لإظهارها مرة أخرى أرسل /start", reply_markup=ReplyKeyboardRemove())

# --- قائمة أقسام المادة ---
async def subject_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sub_code = query.data  
    
    keyboard = [
        [InlineKeyboardButton("📖 نظري", callback_data=f"{sub_code}_theory"),
         InlineKeyboardButton("💻 عملي", callback_data=f"{sub_code}_practical")],
        [InlineKeyboardButton("📝 تكاليف", callback_data=f"{sub_code}_tasks")],
        [InlineKeyboardButton("🔙 رجوع للفصول", callback_data="lvl2_sem2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("اختر القسم المطلوب للمادة (نظري / عملي / تكاليف):", reply_markup=reply_markup)

# تخزين الملفات مؤقتاً
stored_files = {}

async def content_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    section_key = query.data 
    
    files = stored_files.get(section_key, [])
    if not files:
        text = "📁 لا توجد ملفات مرفوعة حتى الآن في هذا القسم.\n\n(قم برفعها في القناة السرية مع الهاشتاج المناسب وسيرسلها البوت هنا تلقائياً للطلاب!)"
        keyboard = [[InlineKeyboardButton("🔙 رجوع للمواد", callback_data="lvl2_sem2")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text(text=f"تم العثور على {len(files)} ملف في هذا القسم.")

# --- استقبال المنشورات من القناة السرية تلقائياً ---
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if message and message.caption:
        caption = message.caption.strip()
        for key in ["sub_risk", "sub_crypto", "sub_web", "sub_os", "sub_db", "sub_net", "sub_culture"]:
            for section in ["_theory", "_practical", "_tasks"]:
                full_tag = f"#{key}{section}"
                if full_tag in caption:
                    target_key = f"{key}{section}"
                    if target_key not in stored_files:
                        stored_files[target_key] = []
                    stored_files[target_key].append(message)
                    await message.reply_text(f"✅ تم حفظ الملف بنجاح في قسم: {target_key}")
                    return

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_buttons))
    application.add_handler(CallbackQueryHandler(levels_handler, pattern="^(lvl2_sem|hide_menu)$"))
    application.add_handler(CallbackQueryHandler(subject_menu_handler, pattern="^sub_"))
    application.add_handler(CallbackQueryHandler(content_view_handler, pattern="(_theory|_practical|_tasks)$"))

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & (filters.Document.ALL | filters.PHOTO | filters.TEXT), handle_channel_post))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
