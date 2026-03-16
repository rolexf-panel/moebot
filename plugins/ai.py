from telegram.ext import CommandHandler

plugin = {
    "name": "ai",
    "version": "1.0.0",
    "description": "Tanya AI menggunakan Ollama",
    "commands": ["/ai"]
}

from moebot.config import OLLAMA_BASE_URL, OLLAMA_MODEL
import httpx

async def ai_command(update, context):
    """Command /ai - tanya AI"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /ai <pertanyaan>")
        return
    
    question = " ".join(context.args)
    
    await update.message.reply_text("🤔 Sedang berpikir...")
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": question,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "Tidak ada jawaban")
                
                if len(answer) > 4000:
                    answer = answer[:4000] + "\n\n... (terlalu panjang)"
                
                await update.message.reply_text(f"🤖 {answer}")
            else:
                await update.message.reply_text(f"❌ Error: {response.status_code}")
    except httpx.ConnectError:
        await update.message.reply_text("❌ Tidak dapat terhubung ke Ollama. Pastikan Ollama berjalan!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("ai", ai_command))
