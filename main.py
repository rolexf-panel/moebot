import logging
import signal
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from importlib import import_module
from telegram.ext import Application, MessageHandler, filters

from moebot.config import BOT_TOKEN, LOG_LEVEL, OWNER_ID
from moebot.database import db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)

PLUGINS = {}

async def error_handler(update, context):
    """Handle semua error"""
    logger.error(f"Error: {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Terjadi kesalahan. Owner akan segera dipernotify."
            )
        except:
            pass
    
    try:
        import traceback
        error_msg = f"❌ Error!\n\n{type(context.error).__name__}: {str(context.error)}\n\n{traceback.format_exc()}"
        if len(error_msg) > 4000:
            error_msg = error_msg[:4000] + "..."
        await context.bot.send_message(chat_id=OWNER_ID, text=error_msg)
    except:
        pass

async def post_init(application: Application):
    """Init setelah bot siap"""
    logger.info("Bot siap!")
    
    if OWNER_ID:
        try:
            await application.bot.send_message(
                chat_id=OWNER_ID,
                text="✅ MoeBot sudah online!"
            )
        except:
            pass

async def shutdown(application: Application):
    """Shutdown bot dengan graceful"""
    logger.info("Mematikan bot...")
    
    if OWNER_ID:
        try:
            await application.bot.send_message(
                chat_id=OWNER_ID,
                text="🔴 MoeBot sedang dimatikan..."
            )
        except:
            pass
    
    await db.close()
    await application.stop()
    logger.info("Bot berhenti")

def load_plugins(application: Application):
    """Load semua plugin dari folder plugins/"""
    plugins_dir = Path(__file__).parent / "plugins"
    
    plugin_files = [
        "start", "help", "admin", "plugin_manager", "info",
        "broadcast", "stats", "notes", "filters", "antiflood",
        "welcome", "sed", "ai", "ytdl", "system",
        "ping", "poll", "sticker", "translate", "quote",
        "encode", "spam", "pin", "grouplink", "contact",
        "pastebin", "wiki", "urban", "movie", "image",
        "lyrics", "github", "shortlink", "emoji", "math",
        "download", "gdrive"
    ]
    
    for plugin_name in plugin_files:
        try:
            module = import_module(f"moebot.plugins.{plugin_name}")
            
            if hasattr(module, "plugin"):
                plugin_meta = module.plugin
                
                plugin_meta["instance"] = module
                PLUGINS[plugin_name] = plugin_meta
                
                if hasattr(module, "register"):
                    module.register(application)
                    logger.info(f"✓ Plugin loaded: {plugin_name} (v{plugin_meta.get('version', '1.0.0')})")
                else:
                    logger.warning(f"⚠ Plugin {plugin_name} tidak punya fungsi register()")
            else:
                logger.warning(f"⚠ Plugin {plugin_name} tidak punya metadata plugin")
                
        except Exception as e:
            logger.error(f"✗ Gagal load plugin {plugin_name}: {e}")
    
    logger.info(f"Total plugin loaded: {len(PLUGINS)}")

def get_plugin(name: str):
    """Ambil plugin berdasarkan nama"""
    return PLUGINS.get(name)

def get_all_plugins() -> dict:
    """Ambil semua plugin"""
    return PLUGINS

async def message_handler(update, context):
    """Handler pesan masuk"""
    if not update.message:
        return
    
    user = update.effective_user
    chat = update.effective_chat
    
    if user:
        await db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
    
    if chat and chat.type != "private":
        await db.add_group(
            chat_id=chat.id,
            title=chat.title,
            username=chat.username
        )
    
    await db.update_stats()

async def main_async():
    """Main async function"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN tidak ditemukan di .env!")
        sys.exit(1)
    
    logger.info("MoeBot Starting...")
    
    await db.connect()
    
    app = Application.builder() \
        .token(BOT_TOKEN) \
        .post_init(post_init) \
        .build()
    
    app.add_error_handler(error_handler)
    
    message_filter = filters.TEXT & ~filters.COMMAND
    app.add_handler(MessageHandler(message_filter, message_handler), group=1)
    
    load_plugins(app)
    
    signal.signal(signal.SIGINT, lambda s, f: None)
    signal.signal(signal.SIGTERM, lambda s, f: None)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    logger.info("MoeBot sudah berjalan. Tekan Ctrl+C untuk menghentikan.")
    
    try:
        import asyncio
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await shutdown(app)

def main():
    """Main function"""
    import asyncio
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
