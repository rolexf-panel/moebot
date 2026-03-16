from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

plugin = {
    "name": "plugin_manager",
    "version": "1.0.0",
    "description": "Kelola plugin: list, enable, disable",
    "commands": ["/plugins", "/enable", "/disable"]
}

from moebot.main import get_all_plugins, get_plugin
from moebot.database import db

async def plugins_command(update, context):
    """Command /plugins - lihat semua plugin"""
    plugins = get_all_plugins()
    
    text = "📦 **Plugin List**\n\n"
    
    enabled = 0
    disabled = 0
    
    for name, meta in plugins.items():
        status = "✅" if await db.get_plugin_state(name) else "❌"
        if await db.get_plugin_state(name):
            enabled += 1
        else:
            disabled += 1
        text += f"{status} {name} - v{meta.get('version', '1.0.0')}\n"
    
    text += f"\nTotal: {enabled} aktif, {disabled} nonaktif"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def enable_command(update, context):
    """Command /enable - aktifkan plugin"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /enable <nama_plugin>")
        return
    
    plugin_name = context.args[0].lower()
    plugins = get_all_plugins()
    
    if plugin_name not in plugins:
        await update.message.reply_text(f"❌ Plugin '{plugin_name}' tidak ditemukan!")
        return
    
    await db.set_plugin_state(plugin_name, True)
    await update.message.reply_text(f"✅ Plugin '{plugin_name}' telah diaktifkan!")

async def disable_command(update, context):
    """Command /disable - nonaktifkan plugin"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /disable <nama_plugin>")
        return
    
    plugin_name = context.args[0].lower()
    plugins = get_all_plugins()
    
    if plugin_name not in plugins:
        await update.message.reply_text(f"❌ Plugin '{plugin_name}' tidak ditemukan!")
        return
    
    await db.set_plugin_state(plugin_name, False)
    await update.message.reply_text(f"✅ Plugin '{plugin_name}' telah dinonaktifkan!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("plugins", plugins_command))
    application.add_handler(CommandHandler("enable", enable_command))
    application.add_handler(CommandHandler("disable", disable_command))
