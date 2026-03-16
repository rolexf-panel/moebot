from telegram.ext import CommandHandler

plugin = {
    "name": "ping",
    "version": "1.0.0",
    "description": "Cek kecepatan bot",
    "commands": ["/ping"]
}

import time

async def ping_command(update, context):
    """Command /ping"""
    start = time.time()
    msg = await update.message.reply_text("🏓 Pong!")
    end = time.time()
    
    latency = round((end - start) * 1000, 2)
    await msg.edit_text(f"🏓 Pong!\n\nLatensi: {latency}ms")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("ping", ping_command))
