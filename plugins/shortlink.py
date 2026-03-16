from telegram.ext import CommandHandler

plugin = {
    "name": "shortlink",
    "version": "1.0.0",
    "description": "Perpendek URL",
    "commands": ["/short", "/tiny"]
}

import httpx

async def short_command(update, context):
    """Command /short - perpendek URL"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /short <url>")
        return
    
    url = context.args[0]
    
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://cleanuri.com/api/v1/shorten",
                data={"url": url}
            )
            
            if response.status_code == 200:
                data = response.json()
                short_url = data.get("result_url", "Gagal!")
                await update.message.reply_text(f"🔗 **URL Pendek:**\n\n{short_url}", parse_mode="Markdown")
            else:
                await update.message.reply_text("Gagal memperpendek URL!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def tiny_command(update, context):
    """Command /tiny"""
    await short_command(update, context)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("short", short_command))
    application.add_handler(CommandHandler("tiny", tiny_command))
