from telegram.ext import CommandHandler, MessageHandler, filters

plugin = {
    "name": "sticker",
    "version": "1.0.0",
    "description": "Kelola sticker",
    "commands": ["/stickerid", "/getsticker"]
}

async def stickerid_command(update, context):
    """Command /stickerid"""
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text("Reply pesan sticker untuk melihat ID!")
        return
    
    sticker = update.message.reply_to_message.sticker
    await update.message.reply_text(
        f"📛 **Sticker Info**\n\n"
        f"ID: `{sticker.file_id}`\n"
        f"Set: {sticker.set_name}\n"
        f"Emoji: {sticker.emoji}",
        parse_mode="Markdown"
    )

async def getsticker_command(update, context):
    """Command /getsticker"""
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text("Reply pesan sticker untuk mengambil!")
        return
    
    sticker = update.message.reply_to_message.sticker
    file = await context.bot.get_file(sticker.file_id)
    await update.message.reply_document(document=file.file_id, caption="Sticker!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("stickerid", stickerid_command))
    application.add_handler(CommandHandler("getsticker", getsticker_command))
