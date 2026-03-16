from telegram.ext import CommandHandler

plugin = {
    "name": "urban",
    "version": "1.0.0",
    "description": "Cari di Urban Dictionary",
    "commands": ["/urban"]
}

import httpx

async def urban_command(update, context):
    """Command /urban - cari di Urban Dictionary"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /urban <query>")
        return
    
    query = " ".join(context.args)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.urbandictionary.com/v0/define",
                params={"term": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("list", [])
                
                if not results:
                    await update.message.reply_text("Tidak ada hasil!")
                    return
                
                result = results[0]
                definition = result.get("definition", "N/A")[:500]
                example = result.get("example", "N/A")[:200]
                
                text = f"📖 **{result['word']}**\n\n"
                text += f"**Definisi:**\n{definition}\n\n"
                text += f"**Contoh:**\n_{example}_"
                
                await update.message.reply_text(text, parse_mode="Markdown")
            else:
                await update.message.reply_text("Error API!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("urban", urban_command))
