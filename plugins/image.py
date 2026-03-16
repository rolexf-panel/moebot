from telegram.ext import CommandHandler

plugin = {
    "name": "image",
    "version": "1.0.0",
    "description": "Cari gambar",
    "commands": ["/image", "/wallpaper"]
}

import httpx

async def image_command(update, context):
    """Command /image - cari gambar"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /image <query>")
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text("🔍 Mencari gambar...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://source.unsplash.com/random",
                params={"query": query},
                follow_redirects=True
            )
            
            if response.status_code == 200:
                await update.message.reply_photo(
                    photo=response.url,
                    caption=f"📷 Gambar: {query}"
                )
            else:
                await update.message.reply_text("Tidak ada hasil!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def wallpaper_command(update, context):
    """Command /wallpaper - cari wallpaper"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /wallpaper <query>")
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text("🔍 Mencari wallpaper...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://source.unsplash.com/1920x1080",
                params={"query": query},
                follow_redirects=True
            )
            
            if response.status_code == 200:
                await update.message.reply_photo(
                    photo=response.url,
                    caption=f"🖼️ Wallpaper: {query}"
                )
            else:
                await update.message.reply_text("Tidak ada hasil!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("image", image_command))
    application.add_handler(CommandHandler("wallpaper", wallpaper_command))
