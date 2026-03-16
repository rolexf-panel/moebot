from telegram.ext import CommandHandler

plugin = {
    "name": "help",
    "version": "1.0.0",
    "description": "Help dinamis berdasarkan plugin aktif",
    "commands": ["/help"]
}

async def help_command(update, context):
    """Command /help - help dinamis"""
    from moebot.main import get_all_plugins
    
    plugins = get_all_plugins()
    
    text = "📖 **Daftar Command**\n\n"
    
    cmd_list = {}
    for name, meta in plugins.items():
        for cmd in meta.get("commands", []):
            desc = meta.get("description", "")
            if cmd not in cmd_list:
                cmd_list[cmd] = desc
    
    for cmd, desc in sorted(cmd_list.items()):
        text += f"{cmd} - {desc}\n"
    
    text += f"\nTotal: {len(cmd_list)} command"
    
    await update.message.reply_text(text, parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("help", help_command))
