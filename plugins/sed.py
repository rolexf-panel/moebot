from telegram.ext import MessageHandler, filters

plugin = {
    "name": "sed",
    "version": "1.0.0",
    "description": "Edit pesan dengan syntax s/old/new/",
    "commands": []
}

import re

async def sed_message(update, context):
    """Handle pesan sed"""
    if not update.message or not update.message.text:
        return
    
    text = update.message.text
    
    if text.startswith("s/") and len(text) > 2:
        parts = text[2:].split("/", 1)
        if len(parts) == 2:
            old_text = parts[0]
            new_text = parts[1]
            
            if update.message.reply_to_message and update.message.reply_to_message.text:
                original = update.message.reply_to_message.text
                
                if old_text in original:
                    new_text_final = original.replace(old_text, new_text, 1)
                    
                    try:
                        await update.message.reply_to_message.edit_text(new_text_final)
                        await update.message.delete()
                    except:
                        pass
            elif text.startswith("s/") and "/" in text[2:]:
                pass

def register(application):
    """Register handler"""
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, sed_message))
