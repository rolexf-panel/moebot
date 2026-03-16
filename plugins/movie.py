from telegram.ext import CommandHandler

plugin = {
    "name": "movie",
    "version": "1.0.0",
    "description": "Cari info film",
    "commands": ["/movie", "/imdb"]
}

import httpx

async def movie_command(update, context):
    """Command /movie - cari info film"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /movie <judul>")
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text("🔍 Mencari...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://www.omdbapi.com/",
                params={
                    "apikey": "4a3b711b",
                    "t": query,
                    "type": "movie"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("Response") == "False":
                    await update.message.reply_text("Film tidak ditemukan!")
                    return
                
                title = data.get("Title", "N/A")
                year = data.get("Year", "N/A")
                rated = data.get("Rated", "N/A")
                plot = data.get("Plot", "N/A")[:300]
                genre = data.get("Genre", "N/A")
                imdb = data.get("imdbRating", "N/A")
                
                text = f"🎬 **{title}** ({year})\n\n"
                text += f"📊 Rating: {rated}\n"
                text += f"⭐ IMDB: {imdb}/10\n"
                text += f"🎭 Genre: {genre}\n\n"
                text += f"📖 {plot}"
                
                await update.message.reply_text(text, parse_mode="Markdown")
            else:
                await update.message.reply_text("Error API!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def imdb_command(update, context):
    """Command /imdb"""
    await movie_command(update, context)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("movie", movie_command))
    application.add_handler(CommandHandler("imdb", imdb_command))
