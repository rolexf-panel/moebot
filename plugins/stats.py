from telegram.ext import CommandHandler

plugin = {
    "name": "stats",
    "version": "1.0.0",
    "description": "Statistik bot",
    "commands": ["/stats"]
}

from moebot.database import db

async def stats_command(update, context):
    """Command /stats"""
    stats = await db.get_stats()
    user_ids = await db.get_all_user_ids()
    group_ids = await db.get_all_group_ids()
    
    text = f"📊 **Statistik Bot**\n\n"
    text += f"👤 User: {len(user_ids)}\n"
    text += f"👥 Grup: {len(group_ids)}\n"
    text += f"💬 Pesan hari ini: {stats.get('messages_today', 0)}\n"
    text += f"💬 Total pesan: {stats.get('messages_total', 0)}"
    
    await update.message.reply_text(text, parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("stats", stats_command))
