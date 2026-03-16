from telegram.ext import CommandHandler

plugin = {
    "name": "emoji",
    "version": "1.0.0",
    "description": "Generate emoji art",
    "commands": ["/emoji", "/shrug", "/tableflip", "/lenny"]
}

async def emoji_command(update, context):
    """Command /emoji - generate emoji art"""
    if len(context.args) < 1:
        text = """😀 **Daftar Emoji**

• /shrug - ¯\\_(ツ)_/¯
• /tableflip - (╯°□°)╯︵ ┻━┻
• /lenny - ( ͡° ͜ʖ ͡°)
• /disapproval - ಠ_ಠ
• /sunglasses - (•_•) ( •_•)>⌐■-■ (⌐■_■)
• /angry - (ノಠ益ಠ)ノ彡┻━┻
• /crying - ಥ﹏ಥ"""
        await update.message.reply_text(text, parse_mode="Markdown")
        return
    
    emoji_type = context.args[0].lower()
    
    emojis = {
        "shrug": "¯\\_(ツ)_/¯",
        "tableflip": "(╯°□°)╯︵ ┻━┻",
        "lenny": "( ͡° ͜ʖ ͡°)",
        "disapproval": "ಠ_ಠ",
        "sunglasses": "(•_•) ( •_•)>⌐■-■ (⌐■_■)",
        "angry": "(ノಠ益ಠ)ノ彡┻━┻",
        "crying": "ಥ﹏ಥ",
        "happy": "(◕‿◕)",
        "sad": "(╥_╥)",
        "think": "🤔",
        "sparkles": "✨"
    }
    
    if emoji_type in emojis:
        await update.message.reply_text(emojis[emoji_type])
    else:
        await update.message.reply_text("Emoji tidak dikenal!")

async def shrug_command(update, context):
    """Command /shrug"""
    await update.message.reply_text("¯\\_(ツ)_/¯")

async def tableflip_command(update, context):
    """Command /tableflip"""
    await update.message.reply_text("(╯°□°)╯︵ ┻━┻")

async def lenny_command(update, context):
    """Command /lenny"""
    await update.message.reply_text("( ͡° ͜ʖ ͡°)")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("emoji", emoji_command))
    application.add_handler(CommandHandler("shrug", shrug_command))
    application.add_handler(CommandHandler("tableflip", tableflip_command))
    application.add_handler(CommandHandler("lenny", lenny_command))
