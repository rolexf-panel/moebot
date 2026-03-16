from telegram.ext import CommandHandler, MessageHandler, filters

plugin = {
    "name": "filters",
    "version": "1.0.0",
    "description": "Auto-reply berdasarkan keyword",
    "commands": ["/addfilter", "/delfilter", "/filters"]
}

from moebot.database import db

async def addfilter_command(update, context):
    """Command /addfilter - tambah filter"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addfilter <keyword> <response>")
        return
    
    keyword = context.args[0].lower()
    response = " ".join(context.args[1:])
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    await db.add_filter(chat_id, keyword, response, user_id)
    await update.message.reply_text(f"✅ Filter ditambahkan!\n\nKeyword: {keyword}\nResponse: {response}")

async def delfilter_command(update, context):
    """Command /delfilter - hapus filter"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /delfilter <keyword>")
        return
    
    keyword = context.args[0].lower()
    chat_id = update.effective_chat.id
    
    if await db.delete_filter(chat_id, keyword):
        await update.message.reply_text(f"✅ Filter '{keyword}' dihapus!")
    else:
        await update.message.reply_text(f"❌ Filter '{keyword}' tidak ditemukan!")

async def filters_command(update, context):
    """Command /filters - lihat semua filter"""
    chat_id = update.effective_chat.id
    
    filter_list = await db.get_filters(chat_id)
    
    if filter_list:
        text = "🔍 **Filters**\n\n"
        for f in filter_list:
            text += f"• {f['keyword']} → {f['response'][:50]}\n"
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Tidak ada filter di grup ini!")

async def filter_message(update, context):
    """Cek pesan untuk filter"""
    if not update.message or not update.message.text:
        return
    
    chat = update.effective_chat
    if chat.type == "private":
        return
    
    text = update.message.text.lower()
    chat_id = chat.id
    
    filters_list = await db.get_filters(chat_id)
    
    for f in filters_list:
        if f['keyword'].lower() in text:
            await update.message.reply_text(f['response'])
            break

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("addfilter", addfilter_command))
    application.add_handler(CommandHandler("delfilter", delfilter_command))
    application.add_handler(CommandHandler("filters", filters_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_message))
