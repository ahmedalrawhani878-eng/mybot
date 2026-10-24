import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8840987474:AAFE2fEXwrh_7eFT6JXZw_Q9C3v1uNtuHaQ"

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

# لوحة الأقسام العادية (4 مواد الأولى + 2 شبكات وقواعد بيانات وويب ومخاطر وتشفير)
# لوحة الأقسام العادية (مضاف إليها التلخيص والتسجيلات)
def sections_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📖 نظري"), KeyboardButton("💻 عملي")],
        [KeyboardButton("📝 تكاليف"), KeyboardButton("📸 صور المحاضرة")],
        [KeyboardButton("📝 تلخيص المادة"), KeyboardButton("🎙️ 🎥 تسجيلات المحاضرات")],
        [KeyboardButton("🔙 رجوع للمواد")]
    ], resize_keyboard=True)

# لوحة أقسام مادة ثقافة (2) - (بدون عملي)
def culture_sections_menu_kb():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📖 نظري"), KeyboardButton("📝 تكاليف")],
        [KeyboardButton("📸 صور المحاضرة"), KeyboardButton("🎙️ 🎥 تسجيلات المحاضرات")],
        [KeyboardButton("📝 تلخيص المادة"), KeyboardButton("🔙 رجوع للمواد")]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    admin_id = 8860646306  # الآي دي الخاص بك
    
    # إرسال إشعار لك في خاصك عندما يدخل أي طالب جديد
    if user.id != admin_id:
        notification_text = (
            f"🚨 طالب جديد دخل البوت!\n\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🔗 المعرّف: @{user.username if user.username else 'لا يوجد'}\n"
            f"🆔 الآي دي: `{user.id}`"
        )
        try:
            await context.bot.send_message(chat_id=admin_id, text=notification_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending notification: {e}")

    user_states[update.effective_user.id] = "main"
    await update.message.reply_text(
        "طلاب الأمن السيبراني - جامعة العلوم والتكنولوجيا (صنعاء)",
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
                context.user_data['current_sub_name'] = text
                user_states[user_id] = "sections"
                
                # إذا كانت المادة ثقافة 2 نعرض لها القائمة المخصصة بدون عملي
                if text == "ثقافة (2)":
                    await update.message.reply_text(f"مادة: {text}\nاختر القسم المطلوب:", reply_markup=culture_sections_menu_kb())
                else:
                    await update.message.reply_text(f"مادة: {text}\nاختر القسم المطلوب:", reply_markup=sections_menu_kb())

    elif state == "sections":
        if text == "🔙 رجوع للمواد":
            user_states[user_id] = "subjects"
            await update.message.reply_text("اختر المادة:", reply_markup=subjects_menu_kb())
        else:
            sub_name = context.user_data.get('current_sub_name', '')
                        sec_map = {
                "📖 نظري": "_theory", 
                "💻 عملي": "_practical", 
                "📝 تكاليف": "_tasks", 
                "📸 صور المحاضرة": "_board",
                "📝 تلخيص المادة": "_summary",
                "🎙️ 🎥 تسجيلات المحاضرات": "_recordings"
            }

            
            if text in sec_map:
                sub_code = context.user_data.get('current_sub', 'sub_risk')
                section_key = f"{sub_code}{sec_map[text]}"
                files = stored_files.get(section_key, [])
                
                current_kb = culture_sections_menu_kb() if sub_name == "ثقافة (2)" else sections_menu_kb()

                if not files:
                    await update.message.reply_text(f"📁 لا توجد ملفات مرفوعة حتى الآن في هذا القسم.\n(قم برفعها في القناة السرية بالهاشتاج: #{section_key})", reply_markup=current_kb)
                else:
                    await update.message.reply_text(f"📁 إليك الملفات والصور الموجودة في هذا القسم ({len(files)} ملف):", reply_markup=current_kb)
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
                            for section in ["_theory", "_practical", "_tasks", "_board", "_summary", "_recordings"]:
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
