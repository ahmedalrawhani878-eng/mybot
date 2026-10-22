import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# توكن البوت الصحيح والكامل
TOKEN = "8826493490:AAENCMKbIwDs2i4sj2cWDLvhGn5GbB_7oj4"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- القائمة الرئيسية ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 المستوى الأول", callback_data="lvl_1")],
        [InlineKeyboardButton("📚 المستوى الثاني", callback_data="lvl_2")],
        [InlineKeyboardButton("📚 المستوى الثالث", callback_data="lvl_3")],
        [InlineKeyboardButton("📚 المستوى الرابع", callback_data="lvl_4")],
        [InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text("مرحباً بك يا مهندس في بوت اتحاد طلاب الأمن السيبراني - جامعة الاتحاد (إب).\nاختر المستوى الدراسي:", reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("اختر المستوى الدراسي:", reply_markup=reply_markup)

# --- مستويات الدراسة ---
async def levels_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "lvl_2":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="lvl2_sem1"),
             InlineKeyboardButton("الفصل الثاني (الجديد)", callback_data="lvl2_sem2")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اختر الفصل الدراسي للمستوى الثاني:", reply_markup=reply_markup)
        
    elif data == "lvl_3":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="lvl3_sem1"),
             InlineKeyboardButton("الفصل الثاني", callback_data="lvl3_sem2")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("مستويات السنة الثالثة - اختر الفصل:", reply_markup=reply_markup)

    elif data == "lvl_4":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="lvl4_sem1"),
             InlineKeyboardButton("الفصل الثاني", callback_data="lvl4_sem2")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("مستويات السنة الرابعة - اختر الفصل:", reply_markup=reply_markup)

    elif data == "main_menu":
        await start(update, context)

# --- مواد السنة الثانية - الفصل الثاني ---
async def lvl2_semester2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("إدارة مخاطر الأمن السيبراني", callback_data="sub_risk")],
        [InlineKeyboardButton("أساسيات التشفير", callback_data="sub_crypto")],
        [InlineKeyboardButton("تقنيات الويب", callback_data="sub_web")],
        [InlineKeyboardButton("نظم التشغيل", callback_data="sub_os")],
        [InlineKeyboardButton("إدارة وأمن قواعد البيانات", callback_data="sub_db")],
        [InlineKeyboardButton("التوجيه والتبديل في الشبكات", callback_data="sub_net")],
        [InlineKeyboardButton("ثقافة (2)", callback_data="sub_culture")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="lvl_2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("📚 مواد السنة الثانية - الفصل الثاني:\nاختر المادة لعرض (نظري، عملي، تكاليف):", reply_markup=reply_markup)

# --- قائمة أقسام المادة ---
async def subject_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sub_code = query.data  
    
    keyboard = [
        [InlineKeyboardButton("📖 نظري", callback_data=f"{sub_code}_theory"),
         InlineKeyboardButton("💻 عملي", callback_data=f"{sub_code}_practical"),
         InlineKeyboardButton("📝 تكاليف", callback_data=f"{sub_code}_tasks")],
        [InlineKeyboardButton("🔙 رجوع للمواد", callback_data="lvl2_sem2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("اختر القسم المطلوب للمادة:", reply_markup=reply_markup)

# تخزين الملفات مؤقتاً
stored_files = {}

async def content_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    section_key = query.data 
    
    files = stored_files.get(section_key, [])
    if not files:
        text = "📁 لا توجد ملفات مرفوعة حتى الآن في هذا القسم.\n\n(ارسلها في القناة السرية مع الهاشتاج وسيحفظها البوت تلقائياً!)"
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="lvl2_sem2")]]
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
    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(levels_handler, pattern="^lvl_[1-4]$"))
    application.add_handler(CallbackQueryHandler(lvl2_semester2_handler, pattern="^lvl2_sem2$"))
    application.add_handler(CallbackQueryHandler(subject_menu_handler, pattern="^sub_"))
    application.add_handler(CallbackQueryHandler(content_view_handler, pattern="(_theory|_practical|_tasks)$"))

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & (filters.Document.ALL | filters.PHOTO | filters.TEXT), handle_channel_post))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
