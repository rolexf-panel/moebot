from telegram.ext import CommandHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

plugin = {
    "name": "admin",
    "version": "1.0.0",
    "description": "Command admin: ban, unban, mute, unmute, kick, warn, setwelcome",
    "commands": ["/ban", "/unban", "/mute", "/unmute", "/kick", "/warn", "/setwelcome"]
}

from moebot.utils.decorators import admin_only, group_only

async def ban_command(update, context):
    """Command /ban"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /ban <user_id> atau reply pesan user")
        return
    
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
        else:
            user_id = int(context.args[0])
        
        await db.set_user_banned(user_id, True)
        await update.message.reply_text(f"✅ User {user_id} telah dibanned!")
    except ValueError:
        await update.message.reply_text("❌ User ID tidak valid!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def unban_command(update, context):
    """Command /unban"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        await db.set_user_banned(user_id, False)
        await update.message.reply_text(f"✅ User {user_id} telah diunban!")
    except ValueError:
        await update.message.reply_text("❌ User ID tidak valid!")

async def mute_command(update, context):
    """Command /mute"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /mute <user_id> [menit]")
        return
    
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
        else:
            user_id = int(context.args[0])
        
        chat_id = update.effective_chat.id
        duration = int(context.args[1]) if len(context.args) > 1 else 60
        
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=None,
            until_date=None
        )
        await update.message.reply_text(f"✅ User {user_id} telah dimute!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def unmute_command(update, context):
    """Command /unmute"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /unmute <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        chat_id = update.effective_chat.id
        
        from telegram import ChatPermissions
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text(f"✅ User {user_id} telah diunmute!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def kick_command(update, context):
    """Command /kick"""
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
        else:
            user_id = int(context.args[0])
        
        chat_id = update.effective_chat.id
        await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
        await context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
        await update.message.reply_text(f"✅ User {user_id} telah dikick!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def warn_command(update, context):
    """Command /warn"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("Usage: Reply pesan user untuk diwarn")
            return
        
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.effective_chat.id
        reason = " ".join(context.args) if context.args else None
        
        await db.add_warn(user_id, chat_id, reason)
        warns = await db.get_warns(user_id, chat_id)
        
        text = f"⚠️ User diwarn!\n"
        text += f"Warn ke-{len(warns)}/3\n"
        if reason:
            text += f"Alasan: {reason}"
        
        await update.message.reply_text(text)
        
        if len(warns) >= 3:
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            await context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
            await update.message.reply_text(f"User {user_id} telah dibanned karena sudah 3x warn!")
            await db.clear_warns(user_id, chat_id)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def setwelcome_command(update, context):
    """Command /setwelcome"""
    if len(context.args) < 1:
        current = await db.get_group_setting(update.effective_chat.id, "welcome_text", "Welcome {name}!")
        await update.message.reply_text(f"Welcome text saat ini:\n{current}\n\nGanti dengan: /setwelcome <text>\nGunakan {name} untuk nama user")
        return
    
    text = " ".join(context.args)
    await db.set_group_setting(update.effective_chat.id, "welcome_text", text)
    await update.message.reply_text(f"✅ Welcome text telah diupdate!\n\n{text}")

from moebot.database import db

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("setwelcome", setwelcome_command))
