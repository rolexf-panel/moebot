from telegram.ext import CommandHandler

plugin = {
    "name": "quote",
    "version": "1.0.0",
    "description": "Generate quote/acara",
    "commands": ["/quote", "/acaratiktok", "/caripesan"]
}

import httpx
import random

QUOTES = [
    "Hidup adalah pertarungan antara baik dan jahat.",
    "Kesalahan terbesar adalah tidak berani mencoba.",
    "Hidup bukan tentang menunggu badai melewati, tapi belajar menari di hujan.",
    " masa depan milik mereka yang percaya pada keindahan mimpi mereka.",
    "Jangan pernah menyerah karena kamu tidak pernah tahu betapa dekatnya kamu dengan keberhasilan.",
    "Sukses adalah tentang terus maju, bukan tentang tidak pernah gagal.",
    "Kebanyakan orang gagal bukan karena kurang kemampuan, tapi karena kurang usaha.",
    "Mimpi tanpa tindakan adalah mimpi biasa. Tindakan tanpa mimpi adalah bosan.",
]

async def quote_command(update, context):
    """Command /quote"""
    quote = random.choice(QUOTES)
    await update.message.reply_text(f"📝 **Quote of the Day**\n\n_{quote}_", parse_mode="Markdown")

async def acaratiktok_command(update, context):
    """Command /acaratiktok"""
    trends = [
        "Suaraku2024", "Trandunia", "Omkekek", "Oplosan",
        "Gajelas", "Wkwk", "Kyaaa", "Sksk",
        "Yowes", "Mabar", "Hype", "Fyp"
    ]
    await update.message.reply_text(f"🎵 **Trend TikTok**\n\n{random.choice(trends)}")

async def caripesan_command(update, context):
    """Command /caripesan"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /caripesan <kata_kunci>")
        return
    
    keyword = " ".join(context.args)
    await update.message.reply_text(f"🔍 Hasil pencarian untuk '{keyword}':\n\n(Data tidak tersedia)")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("acaratiktok", acaratiktok_command))
    application.add_handler(CommandHandler("caripesan", caripesan_command))
