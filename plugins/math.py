from telegram.ext import CommandHandler

plugin = {
    "name": "math",
    "version": "1.0.0",
    "description": "Kalkulator",
    "commands": ["/calc", "/math"]
}

import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

async def calc_command(update, context):
    """Command /calc - kalkulator"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /calc <ekspresi>\n\nContoh: /calc 2+2*3")
        return
    
    expr = " ".join(context.args)
    
    safe_ops = {'+': '+', '-': '-', '*': '*', '/': '/', '**': '**', '%': '%', '(': '(', ')': ')'}
    
    try:
        result = eval(expr)
        await update.message.reply_text(f"📊 **Hasil:**\n\n`{result}`", parse_mode="Markdown")
    except ZeroDivisionError:
        await update.message.reply_text("❌ Error: Pembagian dengan nol!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Ekspresi tidak valid!")

async def math_command(update, context):
    """Command /math"""
    await calc_command(update, context)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("math", math_command))
