from telegram.ext import CommandHandler

plugin = {
    "name": "lyrics",
    "version": "1.0.0",
    "description": "Cari lirik lagu",
    "commands": ["/lyrics", "/lirik"]
}

import httpx

async def lyrics_command(update, context):
    """Command /lyrics - cari lirik"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /lyrics <artis - judul>")
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text("🔍 Mencari lirik...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.lyrics.ovh/suggest",
                params={"q": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                songs = data.get("data", [])
                
                if not songs:
                    await update.message.reply_text("Tidak ada hasil!")
                    return
                
                song = songs[0]
                title = song.get("title", "N/A")
                artist = song.get("artist", {}).get("name", "N/A")
                
                lyrics_response = await client.get(
                    f"https://api.lyrics.ovh/v1/{artist}/{title}"
                )
                
                if lyrics_response.status_code == 200:
                    lyrics_data = lyrics_response.json()
                    lyrics = lyrics_data.get("lyrics", "Lirik tidak ditemukan.")
                    
                    if len(lyrics) > 1500:
                        lyrics = lyrics[:1500] + "\n\n... (terlalu panjang)"
                    
                    text = f"🎵 **{title}** - {artist}\n\n{lyrics}"
                    await update.message.reply_text(text, parse_mode="Markdown")
                else:
                    await update.message.reply_text(f"Lagu ditemukan tapi lirik tidak tersedia!\n\n{artist} - {title}")
            else:
                await update.message.reply_text("Error API!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def lirik_command(update, context):
    """Command /lirik"""
    await lyrics_command(update, context)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("lyrics", lyrics_command))
    application.add_handler(CommandHandler("lirik", lirik_command))
