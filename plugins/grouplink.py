from telegram.ext import CommandHandler

plugin = {
    "name": "grouplink",
    "version": "1.0.0",
    "description": "Kelola invite link grup",
    "commands": ["/invitelink", "/createinvite", "/revokeinvite"]
}

from moebot.utils.decorators import admin_only, group_only

async def invitelink_command(update, context):
    """Command /invitelink"""
    chat = update.effective_chat
    
    try:
        link = await context.bot.create_chat_invite_link(chat_id=chat.id)
        await update.message.reply_text(f"🔗 **Invite Link**\n\n{link.invite_link}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def createinvite_command(update, context):
    """Command /createinvite"""
    chat = update.effective_chat
    
    try:
        member = await context.bot.get_chat_member(chat.id, context.bot.id)
        if member.status not in ["administrator", "creator"]:
            await update.message.reply_text("❌ Bot harus jadi admin!")
            return
        
        link = await context.bot.create_chat_invite_link(
            chat_id=chat.id,
            name="MoeBot Invite"
        )
        await update.message.reply_text(f"✅ Invite link dibuat!\n\n{link.invite_link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def revokeinvite_command(update, context):
    """Command /revokeinvite"""
    chat = update.effective_chat
    
    try:
        link = await context.bot.revoke_chat_invite_link(chat.id, chat.invite_link)
        await update.message.reply_text("✅ Invite link di-revoke!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("invitelink", invitelink_command))
    application.add_handler(CommandHandler("createinvite", createinvite_command))
    application.add_handler(CommandHandler("revokeinvite", revokeinvite_command))
