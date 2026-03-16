from telegram.ext import MessageHandler, filters

plugin = {
    "name": "antiflood",
    "version": "1.0.0",
    "description": "Deteksi flood dan auto-mute",
    "commands": ["/antiflood"]
}

from moebot.database import db
from moebot.config import FLOOD_THRESHOLD, FLOOD_COOLDOWN
from telegram import ChatPermissions
import time

flood_last_message = {}

async def antiflood_message(update, context):
    """Cek pesan untuk flood"""
    if not update.message or not update.message.text:
        return
    
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == "private":
        return
    
    chat_id = chat.id
    user_id = user.id
    
    antiflood_enabled = await db.get_group_setting(chat_id, "antiflood_enabled", True)
    if not antiflood_enabled:
        return
    
    key = f"{chat_id}:{user_id}"
    now = time.time()
    
    if key in flood_last_message:
        last_time = flood_last_message[key]
        if now - last_time < 2:
            flood_count = await db.update_flood_count(user_id, chat_id)
            
            if flood_count >= FLOOD_THRESHOLD:
                try:
                    await context.bot.restrict_chat_member(
                        chat_id=chat_id,
                        user_id=user_id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=now + FLOOD_COOLDOWN
                    )
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"⚠️ {user.first_name} telah dimute karena flood! ({FLOOD_COOLDOWN//60} menit)"
                    )
                    await db.reset_flood_count(user_id, chat_id)
                except:
                    pass
        else:
            await db.reset_flood_count(user_id, chat_id)
    
    flood_last_message[key] = now

async def antiflood_command(update, context):
    """Command /antiflood"""
    if len(context.args) < 1:
        enabled = await db.get_group_setting(update.effective_chat.id, "antiflood_enabled", True)
        status = "Aktif" if enabled else "Nonaktif"
        await update.message.reply_text(f"Anti-flood: {status}\n\nGanti: /antiflood on/off")
        return
    
    status = context.args[0].lower()
    enabled = status in ["on", "enable", "aktif", "1", "true"]
    
    await db.set_group_setting(update.effective_chat.id, "antiflood_enabled", enabled)
    await update.message.reply_text(f"✅ Anti-flood {'diaktifkan' if enabled else 'dinonaktifkan'}!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("antiflood", antiflood_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, antiflood_message))

from telegram.ext import CommandHandler
