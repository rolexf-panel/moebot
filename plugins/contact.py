from telegram.ext import CommandHandler

plugin = {
    "name": "contact",
    "version": "1.0.0",
    "description": "Kirim contact/location",
    "commands": ["/contact", "/location"]
}

async def contact_command(update, context):
    """Command /contact"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /contact <nama> <nomor>")
        return
    
    name = context.args[0]
    phone = context.args[1]
    
    await update.message.reply_contact(phone_number=phone, first_name=name)

async def location_command(update, context):
    """Command /location"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /location <latitude> <longitude>")
        return
    
    try:
        lat = float(context.args[0])
        lon = float(context.args[1])
        
        await update.message.reply_location(latitude=lat, longitude=lon)
    except ValueError:
        await update.message.reply_text("Koordinat tidak valid!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("location", location_command))
