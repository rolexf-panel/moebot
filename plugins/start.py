from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler

plugin = {
    "name": "start",
    "version": "1.0.0",
    "description": "Menu utama bot",
    "commands": ["/start"]
}

BANNER_URL = "https://files.catbox.moe/j2nm96.png"

async def start_command(update, context):
    """Command /start"""
    user = update.effective_user
    chat = update.effective_chat
    
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data="menu_help")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="menu_info")],
        [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
    ]
    
    if chat.type == "private":
        keyboard.append([InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if chat.type == "private":
        text = f"👋 Halo {user.first_name}!\n\n"
        text += "Selamat datang di MoeBot!\n"
        text += "Saya adalah bot multifungsi yang siap membantu kamu.\n\n"
        text += "Gunakan /help untuk melihat semua command."
    else:
        text = f"👋 Halo semua!\n\n"
        text += "MoeBot aktif di grup ini.\n"
        text += "Ketik /help untuk melihat command."
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        try:
            await update.message.reply_photo(
                photo=BANNER_URL,
                caption=text,
                reply_markup=reply_markup
            )
        except:
            await update.message.reply_text(text, reply_markup=reply_markup)

async def menu_callback(update, context):
    """Handle callback dari inline keyboard"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_help":
        await help_command(update, context)
    elif query.data == "menu_info":
        await query.edit_message_text(
            "ℹ️ Info\n\nMoeBot v1.0.0\n\nBot multifungsi dengan fitur lengkap.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu_main")]])
        )
    elif query.data == "menu_main":
        await start_command(update, context)

async def help_command(update, context):
    """Command /help"""
    text = """📖 **Help**

**Command Dasar:**
• /start - Menu utama
• /help - Lihat help ini

**Admin:**
• /ban - Ban user
• /unban - Unban user
• /mute - Mute user
• /unmute - Unmute user
• /kick - Kick user
• /warn - Warn user
• /setwelcome - Set pesan welcome

**Plugin:**
• /plugins - Lihat plugin
• /enable - Enable plugin
• /disable - Disable plugin

**Lainnya:**
• /userinfo - Info user
• /groupinfo - Info grup
• /id - Ambil ID
• /save - Simpan note
• /get - Ambil note
• /notes - Lihat semua note
• /delnote - Hapus note
• /stats - Statistik bot
• /sysinfo - Info sistem
• /ai - Tanya AI
• /dl - Download video"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))
