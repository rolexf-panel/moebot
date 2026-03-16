from telegram.ext import CommandHandler

plugin = {
    "name": "encode",
    "version": "1.0.0",
    "description": "Encode/Decode teks",
    "commands": ["/base64", "/binary", "/reverse"]
}

import base64
import binascii

async def base64_command(update, context):
    """Command /base64 - encode/decode base64"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /base64 <encode|decode> <teks>")
        return
    
    mode = context.args[0].lower()
    text = " ".join(context.args[1:])
    
    if mode in ["e", "encode", "-e"]:
        try:
            encoded = base64.b64encode(text.encode()).decode()
            await update.message.reply_text(f"**Base64 Encode:**\n\n`{encoded}`", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    elif mode in ["d", "decode", "-d"]:
        try:
            decoded = base64.b64decode(text.encode()).decode()
            await update.message.reply_text(f"**Base64 Decode:**\n\n`{decoded}`", parse_mode="Markdown")
        except binascii.Error:
            await update.message.reply_text("Invalid Base64!")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("Usage: /base64 <encode|decode> <teks>")

async def binary_command(update, context):
    """Command /binary - encode/decode binary"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /binary <encode|decode> <teks>")
        return
    
    mode = context.args[0].lower()
    text = " ".join(context.args[1:])
    
    if mode in ["e", "encode", "-e"]:
        try:
            binary = ' '.join(format(ord(c), '08b') for c in text)
            await update.message.reply_text(f"**Binary Encode:**\n\n`{binary}`", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    elif mode in ["d", "decode", "-d"]:
        try:
            binary_list = text.split()
            decoded = ''.join(chr(int(b, 2)) for b in binary_list)
            await update.message.reply_text(f"**Binary Decode:**\n\n`{decoded}`", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("Usage: /binary <encode|decode> <teks>")

async def reverse_command(update, context):
    """Command /reverse - balik teks"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /reverse <teks>")
        return
    
    text = " ".join(context.args)
    reversed_text = text[::-1]
    
    await update.message.reply_text(f"**Reverse:**\n\n`{reversed_text}`", parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("base64", base64_command))
    application.add_handler(CommandHandler("binary", binary_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
