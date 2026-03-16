from telegram.ext import CommandHandler

plugin = {
    "name": "pastebin",
    "version": "1.0.0",
    "description": "Paste ke pastebin",
    "commands": ["/paste", "/haste"]
}

import httpx

async def paste_command(update, context):
    """Command /paste - paste ke ix.io"""
    if not update.message.reply_to_message or not update.message.reply_to_message.text:
        await update.message.reply_text("Reply teks untuk di-paste!")
        return
    
    text = update.message.reply_to_message.text
    
    if len(text) > 10000:
        await update.message.reply_text("Teks terlalu panjang!")
        return
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://ix.io",
                data={"c": text}
            )
            
            if response.status_code == 200:
                await update.message.reply_text(f"📎 **Paste:**\n\n{response.text.strip()}", parse_mode="Markdown")
            else:
                await update.message.reply_text("Gagal paste!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def haste_command(update, context):
    """Command /haste - paste ke hastebin"""
    if not update.message.reply_to_message or not update.message.reply_to_message.text:
        await update.message.reply_text("Reply teks untuk di-paste!")
        return
    
    text = update.message.reply_to_message.text
    
    if len(text) > 10000:
        await update.message.reply_text("Teks terlalu panjang!")
        return
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://hastebin.com/documents",
                data=text
            )
            
            if response.status_code == 200:
                result = response.json()
                key = result.get("key")
                await update.message.reply_text(f"📎 **Hastebin:**\n\nhttps://hastebin.com/raw/{key}", parse_mode="Markdown")
            else:
                await update.message.reply_text("Gagal paste!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("paste", paste_command))
    application.add_handler(CommandHandler("haste", haste_command))
