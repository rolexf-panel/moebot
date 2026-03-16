from telegram.ext import CommandHandler

plugin = {
    "name": "system",
    "version": "1.0.0",
    "description": "Info sistem: CPU, RAM, disk, uptime",
    "commands": ["/sysinfo"]
}

from moebot.config import OWNER_ID
from moebot.utils.helpers import format_bytes, format_percent
import psutil
import time

async def sysinfo_command(update, context):
    """Command /sysinfo"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Command ini hanya untuk owner!")
        return
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_hours = int(uptime_seconds // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    
    text = "💻 **System Info**\n\n"
    text += f"🖥️ **CPU:** {cpu_percent}%\n\n"
    text += f"💾 **RAM:**\n"
    text += f"   Used: {format_bytes(memory.used)}\n"
    text += f"   Free: {format_bytes(memory.free)}\n"
    text += f"   Total: {format_bytes(memory.total)}\n\n"
    text += f"💿 **Disk:**\n"
    text += f"   Used: {format_bytes(disk.used)}\n"
    text += f"   Free: {format_bytes(disk.free)}\n"
    text += f"   Total: {format_bytes(disk.total)}\n\n"
    text += f"⏰ **Uptime:** {uptime_hours} jam {uptime_minutes} menit"
    
    await update.message.reply_text(text, parse_mode="Markdown")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("sysinfo", sysinfo_command))
