import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from moebot.config import OWNER_ID
from moebot.database import db

logger = logging.getLogger(__name__)

def get_user_level(user_id: int, chat_id: int = None) -> str:
    """Dapatkan level user: owner, admin, user, banned"""
    if user_id == OWNER_ID:
        return "owner"
    return "user"

async def check_permission(update: Update, required_level: str) -> bool:
    """Cek permission user"""
    user = update.effective_user
    if not user:
        return False
    
    user_id = user.id
    chat_id = update.effective_chat.id if update.effective_chat else None
    
    if user_id == OWNER_ID:
        return True
    
    if await db.is_user_banned(user_id):
        return False
    
    level = get_user_level(user_id, chat_id)
    
    levels = ["banned", "user", "admin", "owner"]
    try:
        user_level_idx = levels.index(level)
        required_idx = levels.index(required_level)
        return user_level_idx >= required_idx
    except ValueError:
        return False

def owner_only(func):
    """Decorator: Hanya owner yang bisa akses"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("❌ Command ini hanya untuk owner!")
            return
        return await func(update, context)
    return wrapper

def admin_only(func):
    """Decorator: Hanya admin yang bisa akses"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user.id == OWNER_ID:
            return await func(update, context)
        
        if not await check_permission(update, "admin"):
            await update.message.reply_text("❌ Command ini hanya untuk admin!")
            return
        return await func(update, context)
    return wrapper

def not_banned(func):
    """Decorator: User tidak boleh banned"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if not user:
            return
        
        if user.id == OWNER_ID:
            return await func(update, context)
        
        if await db.is_user_banned(user.id):
            await update.message.reply_text("❌ Kamu dibanned!")
            return
        return await func(update, context)
    return wrapper

def group_only(func):
    """Decorator: Hanya bisa di grup"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type == "private":
            await update.message.reply_text("❌ Command ini hanya bisa di grup!")
            return
        return await func(update, context)
    return wrapper

def private_only(func):
    """Decorator: Hanya bisa di private chat"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type != "private":
            await update.message.reply_text("❌ Command ini hanya bisa di private chat!")
            return
        return await func(update, context)
    return wrapper

def typing_action(func):
    """Decorator: Tampilkan typing action"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        return await func(update, context)
    return wrapper
