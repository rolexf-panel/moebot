from telegram.ext import CommandHandler, ChatMemberHandler

plugin = {
    "name": "welcome",
    "version": "1.0.0",
    "description": "Sambut member baru dan goodbye",
    "commands": ["/welcome", "/goodbye"]
}

from moebot.database import db

async def welcome_command(update, context):
    """Command /welcome"""
    if len(context.args) < 1:
        enabled = await db.get_group_setting(update.effective_chat.id, "welcome_enabled", True)
        status = "Aktif" if enabled else "Nonaktif"
        text = await db.get_group_setting(update.effective_chat.id, "welcome_text", "Welcome {name}!")
        await update.message.reply_text(f"Welcome: {status}\nText: {text}\n\nGanti: /welcome on/off <text>")
        return
    
    status = context.args[0].lower()
    enabled = status in ["on", "enable", "aktif", "1", "true"]
    
    await db.set_group_setting(update.effective_chat.id, "welcome_enabled", enabled)
    
    if len(context.args) > 1:
        text = " ".join(context.args[1:])
        await db.set_group_setting(update.effective_chat.id, "welcome_text", text)
    
    await update.message.reply_text(f"✅ Welcome {'diaktifkan' if enabled else 'dinonaktifkan'}!")

async def goodbye_command(update, context):
    """Command /goodbye"""
    if len(context.args) < 1:
        enabled = await db.get_group_setting(update.effective_chat.id, "goodbye_enabled", False)
        status = "Aktif" if enabled else "Nonaktif"
        text = await db.get_group_setting(update.effective_chat.id, "goodbye_text", "Selamat tinggal {name}")
        await update.message.reply_text(f"Goodbye: {status}\nText: {text}\n\nGanti: /goodbye on/off <text>")
        return
    
    status = context.args[0].lower()
    enabled = status in ["on", "enable", "aktif", "1", "true"]
    
    await db.set_group_setting(update.effective_chat.id, "goodbye_enabled", enabled)
    
    if len(context.args) > 1:
        text = " ".join(context.args[1:])
        await db.set_group_setting(update.effective_chat.id, "goodbye_text", text)
    
    await update.message.reply_text(f"✅ Goodbye {'diaktifkan' if enabled else 'dinonaktifkan'}!")

async def chat_member_update(update, context):
    """Handle member join/leave"""
    chat = update.effective_chat
    new_member = update.my_chat_member.new_chat_member
    
    if chat.type == "private":
        return
    
    if new_member.status == "member":
        welcome_enabled = await db.get_group_setting(chat.id, "welcome_enabled", True)
        if welcome_enabled:
            welcome_text = await db.get_group_setting(chat.id, "welcome_text", "Welcome {name}!")
            user_name = new_member.user.first_name
            text = welcome_text.replace("{name}", user_name)
            await context.bot.send_message(chat_id=chat.id, text=text)
    
    elif new_member.status == "left":
        goodbye_enabled = await db.get_group_setting(chat.id, "goodbye_enabled", False)
        if goodbye_enabled:
            goodbye_text = await db.get_group_setting(chat.id, "goodbye_text", "Selamat tinggal {name}")
            user_name = new_member.user.first_name
            text = goodbye_text.replace("{name}", user_name)
            await context.bot.send_message(chat_id=chat.id, text=text)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("welcome", welcome_command))
    application.add_handler(CommandHandler("goodbye", goodbye_command))
    application.add_handler(ChatMemberHandler(chat_member_update, chat_member_types=["my_chat_member"]))
