from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

plugin = {
    "name": "ytdl",
    "version": "1.0.0",
    "description": "Download video/audio via yt-dlp",
    "commands": ["/dl"]
}

import asyncio
import os

async def download_video(url: str, format_type: str = "video") -> str:
    """Download video/audio dari URL"""
    import yt_dlp
    
    ydl_opts = {
        'format': 'best' if format_type == "video" else 'bestaudio/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

async def dl_command(update, context):
    """Command /dl - download video"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /dl <url>")
        return
    
    url = context.args[0]
    
    keyboard = [
        [InlineKeyboardButton("🎬 Video", callback_data=f"dl_video_{url}")],
        [InlineKeyboardButton("🎵 Audio", callback_data=f"dl_audio_{url}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📥 Download dari: {url}\n\nPilih format:",
        reply_markup=reply_markup
    )

async def dl_callback(update, context):
    """Handle callback download"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("dl_video_"):
        url = data[9:]
        format_type = "video"
    elif data.startswith("dl_audio_"):
        url = data[9:]
        format_type = "audio"
    else:
        return
    
    await query.edit_message_text("⏳ Mendownload...")
    
    try:
        filename = await download_video(url, format_type)
        
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=f,
                    caption=f"📥 Download selesai!"
                )
            os.remove(filename)
        else:
            await query.edit_message_text("❌ Gagal download!")
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("dl", dl_command))
    application.add_handler(CallbackQueryHandler(dl_callback, pattern="^dl_"))

from telegram.ext import CallbackQueryHandler
