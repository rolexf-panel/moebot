import logging
import re
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from moebot.config import OWNER_ID

logger = logging.getLogger(__name__)

def escape_html(text: str) -> str:
    """Escape karakter HTML"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_time(seconds: int) -> str:
    """Format detik ke string waktu"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}h")
    if hours > 0:
        parts.append(f"{hours}m")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}d")
    
    return " ".join(parts)

def get_user_name(user) -> str:
    """Dapatkan nama user"""
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        name = user.first_name
        if user.last_name:
            name += f" {user.last_name}"
        return name
    return "User"

def get_chat_name(chat) -> str:
    """Dapatkan nama chat"""
    if chat.title:
        return chat.title
    elif chat.username:
        return f"@{chat.username}"
    return "Chat"

def parse_command_args(text: str, command: str) -> str:
    """Ambil argumen dari command"""
    pattern = f"^{command}(?:\\s+(.*))?$"
    match = re.match(pattern, text)
    return match.group(1).strip() if match and match.group(1) else ""

def create_pagination_buttons(current_page: int, total_pages: int, callback_prefix: str) -> list:
    """Buat tombol pagination"""
    buttons = []
    row = []
    
    if current_page > 1:
        row.append(InlineKeyboardButton("◀️ Prev", callback_data=f"{callback_prefix}_page_{current_page - 1}"))
    
    row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop"))
    
    if current_page < total_pages:
        row.append(InlineKeyboardButton("Next ▶️", callback_data=f"{callback_prefix}_page_{current_page + 1}"))
    
    if row:
        buttons.append(row)
    
    return buttons

def create_back_button(callback_data: str) -> InlineKeyboardButton:
    """Buat tombol back"""
    return InlineKeyboardButton("🔙 Kembali", callback_data=callback_data)

async def send_error_log(context, error: Exception, update: Update = None):
    """Kirim log error ke owner"""
    import traceback
    import sys
    
    error_info = f"❌ Error!\n\n"
    error_info += f"Tipe: {type(error).__name__}\n"
    error_info += f"Pesan: {str(error)}\n\n"
    error_info += f"Traceback:\n{traceback.format_exc()}"
    
    if len(error_info) > 4000:
        error_info = error_info[:4000] + "\n\n... (terlalu panjang)"
    
    try:
        if update:
            user = update.effective_user
            chat = update.effective_chat
            error_info += f"\n\nUser: {get_user_name(user)} ({user.id})"
            if chat:
                error_info += f"\nChat: {get_chat_name(chat)} ({chat.id})"
        
        await context.bot.send_message(chat_id=OWNER_ID, text=error_info)
    except Exception as e:
        logger.error(f"Gagal kirim error log: {e}")

def format_bytes(bytes_val: int) -> str:
    """Format bytes ke human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"

def format_percent(value: float) -> str:
    """Format persen"""
    return f"{value:.1f}%"
