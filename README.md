# MoeBot 🤖

<img src="https://files.catbox.moe/j2nm96.png" alt="MoeBot Banner" width="100%">

Bot Telegram multifungsi dengan sistem plugin modular menggunakan python-telegram-bot v21 (async).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-21.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fitur

### Plugin Admin
- `/ban`, `/unban`, `/mute`, `/unmute`, `/kick` - Kelola user
- `/warn` - Warning system
- `/setwelcome` - Custom welcome message
- Anti-flood detection
- Welcome/Goodbye message

### Plugin Utility
- `/ping` - Cek latency bot
- `/poll`, `/spoll` - Buat polling
- `/calc` - Kalkulator
- `/tr` - Terjemahan
- `/base64` - Encode/Decode
- `/short` - Perpendek URL
- `/paste`, `/haste` - Paste ke pastebin

### Plugin Info
- `/userinfo`, `/groupinfo`, `/id` - Info user/grup
- `/wiki` - Wikipedia search
- `/movie` - Info film (OMDB)
- `/github` - Repo info
- `/urban` - Urban Dictionary
- `/lyrics` - Cari lirik lagu

### Plugin Download/Upload
- `/download` - Download file dari Telegram
- `/savedfiles` - Kelola file tersimpan
- Upload ke: Pixeldrain, Gofile, Mediafire, 0x0

### Plugin AI & Media
- `/ai` - Chat dengan Ollama
- `/dl` - Download video/audio YouTube
- `/image`, `/wallpaper` - Cari gambar

### Plugin Lainnya
- `/stats` - Statistik bot
- `/broadcast` - Broadcast pesan (owner)
- `/sysinfo` - Info sistem (owner)
- Notes & Filters
- Dan banyak lagi...

## 🚀 Instalasi

```bash
# Clone atau download repo ini
cd moebot

# Jalankan setup interaktif
chmod +x setup.sh
./setup.sh
```

Atau manual:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy dan edit .env
cp .env.example .env
# Edit .env dengan BOT_TOKEN dan OWNER_ID

# Jalankan bot
python main.py
```

## ⚙️ Konfigurasi (.env)

```env
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_user_id
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:14b
DB_PATH=moebot.db
LOG_LEVEL=INFO
FLOOD_THRESHOLD=5
FLOOD_COOLDOWN=300
```

## 📁 Struktur Folder

```
moebot/
├── main.py              # Entry point
├── config.py            # Konfigurasi
├── database.py          # SQLite database
├── setup.sh            # Script setup
├── plugins/            # Plugin folder
│   ├── __init__.py
│   ├── start.py
│   ├── admin.py
│   ├── help.py
│   └── ... (35+ plugins)
└── utils/
    ├── decorators.py    # Decorator untuk permission
    └── helpers.py      # Fungsi helper
```

## 📝 Membuat Plugin Baru

Buat file baru di folder `plugins/`, contoh `hello.py`:

```python
from telegram.ext import CommandHandler

# Metadata plugin (wajib)
plugin = {
    "name": "hello",
    "version": "1.0.0",
    "description": "Sapa user",
    "commands": ["/hello"]
}

# Handler function
async def hello_command(update, context):
    """Command /hello"""
    await update.message.reply_text("Halo! 👋")

# Fungsi register (wajib)
def register(application):
    """Register handler ke application"""
    application.add_handler(CommandHandler("hello", hello_command))
```

### Struktur Metadata Plugin

```python
plugin = {
    "name": "nama_plugin",      # Nama unik plugin
    "version": "1.0.0",         # Version
    "description": "Deskripsi", # Deskripsi
    "commands": ["/cmd1", "/cmd2"]  # List command
}
```

### Menggunakan Database

```python
from moebot.database import db

# Simpan data
await db.save_note(chat_id, name, content, user_id)

# Ambil data
note = await db.get_note(chat_id, name)
notes = await db.get_notes(chat_id)

# Update user
await db.add_user(user_id, username, first_name, last_name)
```

### Menggunakan Decorators

```python
from moebot.utils.decorators import owner_only, admin_only, group_only

# Hanya owner yang bisa akses
@owner_only
async def owner_command(update, context):
    ...

# Hanya admin yang bisa akses
@admin_only
async def admin_command(update, context):
    ...

# Hanya di grup
@group_only
async def group_command(update, context):
    ...
```

### Inline Keyboard

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Opsi 1", callback_data="opt1")],
    [InlineKeyboardButton("Opsi 2", callback_data="opt2")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

await update.message.reply_text("Pilih:", reply_markup=reply_markup)
```

### Callback Query Handler

```python
from telegram.ext import CallbackQueryHandler

async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "opt1":
        await query.edit_message_text("Kamu pilih opsi 1!")

def register(application):
    application.add_handler(CallbackQueryHandler(callback_handler))
```

## ➕ Menambahkan Plugin ke Main

Edit `main.py`, tambahkan nama plugin ke list:

```python
plugin_files = [
    "start", "help", "admin", ...
    "hello"  # Tambahkan di sini
]
```

## 📋 Command Lengkap

| Command | Deskripsi |
|---------|-----------|
| `/start` | Mulai bot |
| `/help` | Bantuan |
| `/plugins` | List plugin |
| `/enable` | Aktifkan plugin |
| `/disable` | Nonaktifkan plugin |
| `/ban` | Ban user |
| `/unban` | Unban user |
| `/mute` | Mute user |
| `/unmute` | Unmute user |
| `/kick` | Kick user |
| `/warn` | Warn user |
| `/userinfo` | Info user |
| `/groupinfo` | Info grup |
| `/id` | Ambil ID |
| `/stats` | Statistik |
| `/broadcast` | Broadcast |
| `/save` | Simpan note |
| `/get` | Ambil note |
| `/notes` | List notes |
| `/dl` | Download YouTube |
| `/ai` | Tanya AI |
| `/sysinfo` | Info sistem |
| `/download` | Download file |
| `/savedfiles` | File tersimpan |
| `/wiki` | Wikipedia |
| `/movie` | Info film |
| `/github` | GitHub repo |
| `/calc` | Kalkulator |
| `/tr` | Terjemahkan |

## 📄 Lisensi

MIT License - lihat file `LICENSE`

## 👤 Author

MoeBot - Multi-Feature Telegram Bot
