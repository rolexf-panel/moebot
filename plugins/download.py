from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

plugin = {
    "name": "download",
    "version": "1.1.0",
    "description": "Download & upload file",
    "commands": ["/download", "/savefile", "/savedfiles", "/deletefile", "/uploadfile"]
}

import os
import asyncio
from pathlib import Path

DOWNLOAD_DIR = Path("/tmp/moebot_downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def format_size(size):
    """Format size ke human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

async def upload_to_service(file_path: str, service: str) -> str:
    """Upload file ke layanan"""
    import httpx
    
    if service == "pixeldrain":
        async with httpx.AsyncClient(timeout=600.0) as client:
            with open(file_path, 'rb') as f:
                response = await client.post('https://pixeldrain.com/api/file', files={'file': f})
            if response.status_code == 200:
                file_id = response.json().get('id')
                return f"https://pixeldrain.com/u/{file_id}"
    
    elif service == "gofile":
        async with httpx.AsyncClient(timeout=600.0) as client:
            token_resp = await client.get('https://api.gofile.io/getServer')
            server = token_resp.json()['data']['server']
            with open(file_path, 'rb') as f:
                response = await client.post(f'https://{server}.gofile.io/uploadFile', files={'file': f})
            if response.status_code == 200:
                return response.json()['data']['downloadPage']
    
    elif service == "mediafire":
        async with httpx.AsyncClient(timeout=600.0) as client:
            with open(file_path, 'rb') as f:
                response = await client.post('https://www.mediafire.com/api/upload/upload.php', files={'file': f})
            if response.status_code == 200:
                data = response.json()
                if data.get('response') == 'OK':
                    return data['result']['direct_link']
    
    elif service in ["0x0", "0x0.st"]:
        async with httpx.AsyncClient(timeout=600.0) as client:
            with open(file_path, 'rb') as f:
                response = await client.post('https://0x0.st', files={'file': f})
            if response.status_code == 200:
                return response.text.strip()
    
    return None

async def download_file(update, context, msg, file, file_name):
    """Download file dan tampilkan opsi"""
    await update.message.reply_text("⏳ Downloading...")
    
    try:
        telegram_file = await context.bot.get_file(file.file_id)
        save_path = DOWNLOAD_DIR / file_name
        
        await telegram_file.download_to_drive(custom_path=str(save_path))
        
        file_size = os.path.getsize(save_path)
        size_str = format_size(file_size)
        
        keyboard = [
            [
                InlineKeyboardButton("📤 Pixeldrain", callback_data=f"upload_{file_name}_pixeldrain"),
                InlineKeyboardButton("📤 Gofile", callback_data=f"upload_{file_name}_gofile"),
            ],
            [
                InlineKeyboardButton("📤 Mediafire", callback_data=f"upload_{file_name}_mediafire"),
                InlineKeyboardButton("📤 0x0", callback_data=f"upload_{file_name}_0x0"),
            ],
            [
                InlineKeyboardButton("💾 Skip (Simpan saja)", callback_data=f"save_{file_name}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"✅ **Download Selesai!**\n\n"
            f"📄 File: {file_name}\n"
            f"💾 Size: {size_str}\n\n"
            f"Pilih aksi:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def download_command(update, context):
    """Command /download - download file dari reply"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply pesan yang ingin di-download!")
        return
    
    msg = update.message.reply_to_message
    
    file = None
    file_name = None
    
    if msg.document:
        file = msg.document
        file_name = file.file_name or "document"
    elif msg.photo:
        file = msg.photo[-1]
        file_name = f"photo_{file.file_id}.jpg"
    elif msg.video:
        file = msg.video
        file_name = file.file_name or "video"
    elif msg.audio:
        file = msg.audio
        file_name = file.file_name or "audio"
    elif msg.voice:
        file = msg.voice
        file_name = f"voice_{file.file_id}.ogg"
    elif msg.sticker:
        file = msg.sticker
        file_name = f"sticker_{file.file_id}.webp"
    else:
        await update.message.reply_text("Tidak ada file untuk di-download!")
        return
    
    await download_file(update, context, msg, file, file_name)

async def list_downloads_command(update, context):
    """Command /savedfiles - list file yang tersimpan"""
    files = list(DOWNLOAD_DIR.iterdir())
    
    if not files:
        await update.message.reply_text("Tidak ada file tersimpan!")
        return
    
    keyboard = []
    for f in files:
        size = format_size(f.stat().st_size)
        keyboard.append([
            InlineKeyboardButton(f"📤 {f.name} ({size})", callback_data=f"listupload_{f.name}")
        ])
    
    if len(keyboard) > 20:
        files_list = []
        for f in files:
            size = format_size(f.stat().st_size)
            files_list.append(f"• {f.name} ({size})")
        
        text = "📂 **File Tersimpan:**\n\n" + "\n".join(files_list)
        text += "\n\nGunakan /uploadfile <nama> <service> untuk upload"
        
        keyboard = [[InlineKeyboardButton("📤 Upload semua", callback_data="upload_all")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📂 **File Tersimpan:**\n\nPilih file untuk di-upload:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def uploadfile_command(update, context):
    """Command /uploadfile - upload file tersimpan"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /uploadfile <nama_file> <service>\n\n"
            "Service: pixeldrain, gofile, mediafire, 0x0"
        )
        return
    
    filename = context.args[0]
    service = context.args[1].lower()
    
    file_path = DOWNLOAD_DIR / filename
    
    if not file_path.exists():
        await update.message.reply_text(f"❌ File '{filename}' tidak ditemukan!")
        return
    
    await update.message.reply_text(f"⬆️ Uploading ke {service}...")
    
    result = await upload_to_service(str(file_path), service)
    
    if result:
        await update.message.reply_text(
            f"✅ **Upload Selesai!**\n\n{result}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Upload gagal!")

async def deletefile_command(update, context):
    """Command /deletefile - hapus file"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /deletefile <nama_file>")
        return
    
    filename = " ".join(context.args)
    file_path = DOWNLOAD_DIR / filename
    
    if file_path.exists():
        file_path.unlink()
        await update.message.reply_text(f"✅ File '{filename}' dihapus!")
    else:
        await update.message.reply_text(f"❌ File '{filename}' tidak ditemukan!")

async def callback_handler(update, context):
    """Handle callback dari inline keyboard"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("upload_"):
        parts = data[7:].rsplit("_", 1)
        if len(parts) == 2:
            file_name, service = parts
            file_path = DOWNLOAD_DIR / file_name
            
            if not file_path.exists():
                await query.edit_message_text(f"❌ File tidak ditemukan!")
                return
            
            await query.edit_message_text(f"⬆️ Uploading ke {service}...")
            
            result = await upload_to_service(str(file_path), service)
            
            if result:
                await query.edit_message_text(
                    f"✅ **Upload Selesai!**\n\n{result}",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text("❌ Upload gagal!")
    
    elif data.startswith("save_"):
        file_name = data[5:]
        await query.edit_message_text(f"💾 File '{file_name}' disimpan!")
    
    elif data.startswith("listupload_"):
        file_name = data[12:]
        
        keyboard = [
            [
                InlineKeyboardButton("📤 Pixeldrain", callback_data=f"upload_{file_name}_pixeldrain"),
                InlineKeyboardButton("📤 Gofile", callback_data=f"upload_{file_name}_gofile"),
            ],
            [
                InlineKeyboardButton("📤 Mediafire", callback_data=f"upload_{file_name}_mediafire"),
                InlineKeyboardButton("📤 0x0", callback_data=f"upload_{file_name}_0x0"),
            ],
            [
                InlineKeyboardButton("❌ Hapus", callback_data=f"deletefile_{file_name}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        file_path = DOWNLOAD_DIR / file_name
        size = format_size(file_path.stat().st_size) if file_path.exists() else "?"
        
        await query.edit_message_text(
            f"📄 **{file_name}**\n💾 Size: {size}\n\nPilih aksi:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    elif data.startswith("deletefile_"):
        file_name = data[12:]
        file_path = DOWNLOAD_DIR / file_name
        
        if file_path.exists():
            file_path.unlink()
            await query.edit_message_text(f"✅ File '{file_name}' dihapus!")
        else:
            await query.edit_message_text(f"❌ File tidak ditemukan!")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("download", download_command))
    application.add_handler(CommandHandler("savefile", download_command))
    application.add_handler(CommandHandler("savedfiles", list_downloads_command))
    application.add_handler(CommandHandler("uploadfile", uploadfile_command))
    application.add_handler(CommandHandler("deletefile", deletefile_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
