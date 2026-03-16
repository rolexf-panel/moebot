from telegram.ext import CommandHandler

plugin = {
    "name": "wiki",
    "version": "1.0.0",
    "description": "Cari di Wikipedia",
    "commands": ["/wiki"]
}

import httpx

async def wiki_command(update, context):
    """Command /wiki - cari di Wikipedia"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /wiki <query>")
        return
    
    query = " ".join(context.args)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            search_response = await client.get(
                "https://id.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json"
                }
            )
            
            search_data = search_response.json()
            results = search_data.get("query", {}).get("search", [])
            
            if not results:
                await update.message.reply_text("Tidak ada hasil!")
                return
            
            page_title = results[0]["title"]
            page_response = await client.get(
                "https://id.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "titles": page_title,
                    "format": "json"
                }
            )
            
            page_data = page_response.json()
            pages = page_data.get("query", {}).get("pages", {})
            page_id = list(pages.keys())[0]
            extract = pages[page_id].get("extract", "Tidak ada deskripsi.")
            
            if len(extract) > 1000:
                extract = extract[:1000] + "..."
            
            await update.message.reply_text(
                f"📚 **{page_title}**\n\n{extract}",
                parse_mode="Markdown"
            )
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("wiki", wiki_command))
