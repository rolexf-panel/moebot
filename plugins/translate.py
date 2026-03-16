from telegram.ext import CommandHandler

plugin = {
    "name": "translate",
    "version": "1.0.0",
    "description": "Terjemahkan teks",
    "commands": ["/tr"]
}

import httpx

LANG_CODES = {
    "en": "English", "id": "Indonesia", "es": "Español",
    "fr": "France", "de": "Deutsch", "it": "Italiano",
    "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
    "ko": "Korean", "zh": "Chinese", "ar": "Arabic",
    "hi": "Hindi", "th": "Thai", "vi": "Vietnam"
}

async def tr_command(update, context):
    """Command /tr - terjemahkan"""
    if len(context.args) < 2:
        text = "Daftar kode bahasa:\n\n"
        for code, name in LANG_CODES.items():
            text += f"• {code} - {name}\n"
        text += "\nUsage: /tr <kode_bahasa> <teks>"
        await update.message.reply_text(text)
        return
    
    lang = context.args[0].lower()
    if lang not in LANG_CODES:
        await update.message.reply_text(f"Kode bahasa tidak valid! Gunakan kode dari daftar.")
        return
    
    text = " ".join(context.args[1:])
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.mymemory.translated.net/get",
                params={"q": text, "langpair": f"en|{lang}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("responseStatus") == 200:
                    translated = result["responseData"]["translatedText"]
                    await update.message.reply_text(
                        f"**Terjemahan** ({LANG_CODES[lang]}):\n\n{translated}",
                        parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text("Gagal menerjemahkan!")
            else:
                await update.message.reply_text("Error API!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("tr", tr_command))
