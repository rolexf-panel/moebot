from telegram.ext import CommandHandler

plugin = {
    "name": "broadcast",
    "version": "1.0.0",
    "description": "Broadcast pesan ke semua user/grup",
    "commands": ["/broadcast"]
}

from moebot.config import OWNER_ID
from moebot.database import db

async def broadcast_command(update, context):
    """Command /broadcast - broadcast pesan"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Command ini hanya untuk owner!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /broadcast <pesan>")
        return
    
    pesan = " ".join(context.args)
    
    user_ids = await db.get_all_user_ids()
    group_ids = await db.get_all_group_ids()
    
    success = 0
    failed = 0
    
    await update.message.reply_text(f"📢 Memulai broadcast ke {len(user_ids)} user dan {len(group_ids)} grup...")
    
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=pesan)
            success += 1
        except:
            failed += 1
    
    for gid in group_ids:
        try:
            await context.bot.send_message(chat_id=gid, text=pesan)
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(
        f"✅ Broadcast selesai!\n\nBerhasil: {success}\nGagal: {failed}"
    )

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("broadcast", broadcast_command))
