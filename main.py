import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8826493490:AAENCMKbIwDs2i4sj2cWDLvhGn5GbB_7oj4"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

user_states = {}
stored_files = {}

def main_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📚 السنة الدراسية الأولى"), KeyboardButton("📚 السنة الدراسية الثانية (الحالية)")],
        [KeyboardButton("📚 السنة الدراسية الثالثة"), KeyboardButton("📚 السنة الدراسية الرابعة")],
        [KeyboardButton("📢 الإعلانات العامة"), KeyboardButton("ℹ️ عن البوت")]
    ], resize_keyboard=True)

def sem_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("الفصل الأول"), KeyboardButton("الفصل الثاني (الحالي)")],
        [KeyboardButton("🔙 رجوع للقائمة الرئيسية")]
    ], resize_keyboard=True)

def subjects_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("إدارة مخاطر الأمن السيبراني"), KeyboardButton("أساسيات التشفير")],
        [KeyboardButton("تقنيات الويب"), KeyboardButton("نظم التشغيل")],
        [KeyboardButton("إدارة وأمن قواعد البيانات"), KeyboardButton("التوجيه والتبديل في الشبكات")],
        [KeyboardButton("ثقافة (2)"), KeyboardButton("🔙 رجوع للفصول")]
    ], resize_keyboard=True)

def sections_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📖 نظري"), KeyboardButton("💻 عملي")],
        [KeyboardButton("📝 تكاليف"), KeyboardButton("🔙 رجوع للمواد")]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_states[update.effective_user.id] = "main"
    await update.message.reply_text(
        "مرحباً بك يا مهندس في بوت اتحاد طلاب الأمن السيبراني - جامعة العلوم والتكنولوجيا (صنعاء).\nاختر من لوحة المفاتيح بالأسفل:",
        reply_markup=main_menu_kb()
    )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    state = user_states.get(user_id, "main")

    if text == "🔙 رجوع للقائمة الرئيسية" or text == "/start":
        user_states[user_id] = "main"
        await update.message.reply_text("القائمة الرئيسية:", reply_markup=main_menu_kb())
        return

    if state == "main":
        if text == "📚 السنة الدراسية الثانية (الحالية)":
            user_states[user_id] = "sems"
            await update.message.reply_text("اختر الفصل الدراسي:", reply_markup=sem_menu_kb())
        elif text in ["📚 السنة الدراسية الأولى", "📚 السنة الدراسية الثالثة", "📚 السنة الدراسية الرابعة"]:
            await update.message.reply_text(f"🛡 عذراً يا مهندس، محتوى **{text}** غير متوفر حالياً.", reply_markup=main_menu_kb(), parse_mode="Markdown")
        elif text == "📢 الإعلانات العامة":
            await update.message.reply_text("📢 لا توجد إعلانات هامة في الوقت الحالي.", reply_markup=main_menu_kb())
        elif text == "ℹ️ عن البوت":
            await update.message.reply_text("🛡 بوت اتحاد طلاب الأمن السيبراني - جامعة العلوم والتكنولوجيا (صنعاء).", reply_markup=main_menu_kb())

    elif state == "sems":
        if text == "الفصل الثاني (الحالي)":
            user_states[user_id] = "subjects"
            await update.message.reply_text("📚 مواد السنة الثانية - الفصل الثاني:\nاختر المادة:", reply_markup=subjects_menu_kb())
        elif text == "الفصل الأول":
            await update.message.reply_text("📚 محتوى الفصل الأول قيد التحديث.", reply_markup=sem_menu_kb())
        elif text == "🔙 رجوع للقائمة الرئيسية":
            user_states[user_id] = "main"
            await update.message.reply_text("القائمة الرئيسية:", reply_markup=main_menu_kb())

    elif state == "subjects":
        if text == "🔙 رجوع للفصول":
            user_states[user_id] = "sems"
            await update.message.reply_text("اختر الفصل الدراسي:", reply_markup=sem_menu_kb())
        else:
            sub_map = {
                "إدارة مخاطر الأمن السيبراني": "sub_risk",
                "أساسيات التشفير": "sub_crypto",
                "تقنيات الويب": "sub_web",
                "نظم التشغيل": "sub_os",
                "إدارة وأمن قواعد البيانات": "sub_db",
                "التوجيه والتبديل في الشبكات": "sub_net",
                "ثقافة (2)": "sub_culture"
            }
            if text in sub_map:
                context.user_data['current_sub'] = sub_map[text]
                user_states[user_id] = "sections"
                await update.message.reply_text(f"مادة: {text}\nاختر القسم المطلوب (نظري، عملي، تكاليف):", reply_markup=sections_menu_kb())

    elif state == "sections":
        if text == "🔙 رجوع للمواد":
            user_states[user_id] = "subjects"
            await update.message.reply_text("اختر المادة:", reply_markup=subjects_menu_kb())
        else:
            sec_map = {"📖 نظري": "_theory", "💻 عملي": "_practical", "📝 تكاليف": "_tasks"}
            if text in sec_map:
                sub_code = context.user_data.get('current_sub', 'sub_risk')
                section_key = f"{sub_code}{sec_map[text]}"
                files = stored_files.get(section_key, [])
                
                if not files:
                    await update.message.reply_text(f"📁 لا توجد ملفات مرفوعة حتى الآن في هذا القسم.\n(قم برفعها في القناة السرية بالهاشتاج: #{section_key})", reply_markup=sections_menu_kb())
                else:
                    await update.message.reply_text(f"📁 إليك الملفات الموجودة في هذا القسم ({len(files)} ملف):", reply_markup=sections_menu_kb())
                    for message in files:
                        await context.bot.copy_message(
                            chat_id=user_id,
                            from_chat_id=message.chat_id,
                            message_id=message.message_id
                        )

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & (filters.Document.ALL | filters.PHOTO | filters.TEXT), handle_channel_post))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
