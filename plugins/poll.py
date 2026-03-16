from telegram.ext import CommandHandler, ConversationHandler

plugin = {
    "name": "poll",
    "version": "1.0.0",
    "description": "Buat polling",
    "commands": ["/poll", "/spoll"]
}

from telegram import Poll

async def poll_command(update, context):
    """Command /poll - buat polling"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /poll <pertanyaan> | <opsi1> | <opsi2> | ...")
        return
    
    args_text = " ".join(context.args)
    parts = args_text.split("|")
    
    if len(parts) < 3:
        await update.message.reply_text("Minimal 2 opsi!")
        return
    
    question = parts[0].strip()
    options = [opt.strip() for opt in parts[1:]]
    
    if len(options) > 10:
        await update.message.reply_text("Maksimal 10 opsi!")
        return
    
    await update.message.reply_poll(
        question=question,
        options=options,
        is_anonymous=False
    )

async def spoll_command(update, context):
    """Command /spoll - buat polling tanpa hasil"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spoll <pertanyaan> | <opsi1> | <opsi2> | ...")
        return
    
    args_text = " ".join(context.args)
    parts = args_text.split("|")
    
    if len(parts) < 3:
        await update.message.reply_text("Minimal 2 opsi!")
        return
    
    question = parts[0].strip()
    options = [opt.strip() for opt in parts[1:]]
    
    if len(options) > 10:
        await update.message.reply_text("Maksimal 10 opsi!")
        return
    
    await update.message.reply_poll(
        question=question,
        options=options,
        is_anonymous=True,
        allows_multiple_answers=False
    )

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("poll", poll_command))
    application.add_handler(CommandHandler("spoll", spoll_command))
