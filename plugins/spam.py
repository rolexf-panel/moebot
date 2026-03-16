from telegram.ext import CommandHandler

plugin = {
    "name": "spam",
    "version": "1.0.0",
    "description": "Spam pesan (owner only)",
    "commands": ["/spam"]
}

from moebot.config import OWNER_ID
import asyncio

async def spam_command(update, context):
    """Command /spam - spam pesan"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Command ini hanya untuk owner!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spam <jumlah> <pesan>")
        return
    
    try:
        count = int(context.args[0])
        if count > 10:
            count = 10
    except ValueError:
        await update.message.reply_text("Jumlah harus angka!")
        return
    
    text = " ".join(context.args[1:])
    
    chat_id = update.effective_chat.id
    
    for i in range(count):
        await context.bot.send_message(chat_id=chat_id, text=text)
        await asyncio.sleep(0.5)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("spam", spam_command))
