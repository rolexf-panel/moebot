from telegram.ext import CommandHandler

plugin = {
    "name": "pin",
    "version": "1.0.0",
    "description": "Pin/unpin pesan",
    "commands": ["/pin", "/unpin"]
}

from moebot.utils.decorators import admin_only, group_only

async def pin_command(update, context):
    """Command /pin"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply pesan yang ingin di-pin!")
        return
    
    try:
        await update.message.reply_to_message.pin()
        await update.message.reply_text("✅ Pesan di-pin!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def unpin_command(update, context):
    """Command /unpin"""
    try:
        await context.bot.unpin_chat_message(chat_id=update.effective_chat.id)
        await update.message.reply_text("✅ Pesan di-unpin!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("pin", pin_command))
    application.add_handler(CommandHandler("unpin", unpin_command))
