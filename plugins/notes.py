from telegram.ext import CommandHandler

plugin = {
    "name": "notes",
    "version": "1.0.0",
    "description": "Simpan dan ambil catatan",
    "commands": ["/save", "/get", "/notes", "/delnote"]
}

from moebot.database import db

async def save_note_command(update, context):
    """Command /save - simpan note"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /save <nama> <isi>")
        return
    
    name = context.args[0].lower()
    content = " ".join(context.args[1:])
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    await db.save_note(chat_id, name, content, user_id)
    await update.message.reply_text(f"✅ Note '{name}' disimpan!")

async def get_note_command(update, context):
    """Command /get - ambil note"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /get <nama>")
        return
    
    name = context.args[0].lower()
    chat_id = update.effective_chat.id
    
    note = await db.get_note(chat_id, name)
    
    if note:
        await update.message.reply_text(f"📝 **{name}**\n\n{note['content']}", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Note '{name}' tidak ditemukan!")

async def notes_command(update, context):
    """Command /notes - lihat semua note"""
    chat_id = update.effective_chat.id
    
    notes = await db.get_notes(chat_id)
    
    if notes:
        text = "📝 **Notes**\n\n"
        for note in notes:
            text += f"• {note}\n"
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Tidak ada note di grup ini!")

async def delnote_command(update, context):
    """Command /delnote - hapus note"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /delnote <nama>")
        return
    
    name = context.args[0].lower()
    chat_id = update.effective_chat.id
    
    if await db.delete_note(chat_id, name):
        await update.message.reply_text(f"✅ Note '{name}' dihapus!")
    else:
        await update.message.reply_text(f"❌ Note '{name}' tidak ditemukan!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("save", save_note_command))
    application.add_handler(CommandHandler("get", get_note_command))
    application.add_handler(CommandHandler("notes", notes_command))
    application.add_handler(CommandHandler("delnote", delnote_command))
