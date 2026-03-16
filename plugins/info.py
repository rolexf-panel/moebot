from telegram.ext import CommandHandler

plugin = {
    "name": "info",
    "version": "1.0.0",
    "description": "Info user, grup, dan ID",
    "commands": ["/userinfo", "/groupinfo", "/id"]
}

from moebot.database import db

async def userinfo_command(update, context):
    """Command /userinfo"""
    user = None
    
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args:
        try:
            user_id = int(context.args[0])
            chat = await context.bot.get_chat(user_id)
            user = type('User', (), {
                'id': chat.id,
                'username': chat.username,
                'first_name': chat.first_name,
                'last_name': chat.last_name,
                'is_bot': chat.is_bot
            })()
        except:
            pass
    else:
        user = update.effective_user
    
    if not user:
        await update.message.reply_text("❌ User tidak ditemukan!")
        return
    
    db_user = await db.get_user(user.id)
    
    text = f"ℹ️ **User Info**\n\n"
    text += f"ID: `{user.id}`\n"
    text += f"Name: {user.first_name}"
    if user.last_name:
        text += f" {user.last_name}"
    text += "\n"
    if user.username:
        text += f"Username: @{user.username}\n"
    text += f"Bot: {'Ya' if hasattr(user, 'is_bot') and user.is_bot else 'Tidak'}\n"
    
    if db_user:
        text += f"Banned: {'Ya' if db_user.get('is_banned') else 'Tidak'}\n"
        text += f"Admin: {'Ya' if db_user.get('is_admin') else 'Tidak'}\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def groupinfo_command(update, context):
    """Command /groupinfo"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ Command ini hanya untuk grup!")
        return
    
    chat = update.effective_chat
    db_group = await db.get_group(chat.id)
    
    text = f"ℹ️ **Group Info**\n\n"
    text += f"ID: `{chat.id}`\n"
    text += f"Title: {chat.title}\n"
    if chat.username:
        text += f"Username: @{chat.username}\n"
    text += f"Type: {chat.type}\n"
    
    if db_group:
        text += f"Welcome: {'Aktif' if db_group.get('welcome_enabled') else 'Nonaktif'}\n"
        text += f"Anti-flood: {'Aktif' if db_group.get('antiflood_enabled') else 'Nonaktif'}\n"
    
    member_count = 0
    try:
        member_count = await context.bot.get_chat_member_count(chat.id)
    except:
        pass
    text += f"Members: {member_count}"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def id_command(update, context):
    """Command /id"""
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == "private":
        text = f"🆔 **ID Kamu**\n\n`{user.id}`"
    else:
        text = f"🆔 **ID Info**\n\n"
        text += f"Chat ID: `{chat.id}`\n"
        text += f"User ID: `{user.id}`"
    
    await update.message.reply_text(text, parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("userinfo", userinfo_command))
    application.add_handler(CommandHandler("groupinfo", groupinfo_command))
    application.add_handler(CommandHandler("id", id_command))
