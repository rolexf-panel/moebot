from telegram.ext import CommandHandler

plugin = {
    "name": "github",
    "version": "1.0.0",
    "description": "Cari repo GitHub",
    "commands": ["/github", "/gh"]
}

import httpx

async def github_command(update, context):
    """Command /github - cari repo GitHub"""
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /github <username> atau /github <username>/<repo>")
        return
    
    query = " ".join(context.args)
    
    if "/" in query:
        parts = query.split("/")
        user = parts[0]
        repo = parts[1]
        url = f"https://api.github.com/repos/{user}/{repo}"
    else:
        url = f"https://api.github.com/users/{query}"
    
    await update.message.reply_text("🔍 Mencari...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if "repos_url" in data:
                    user_data = data
                    text = f"👤 **{user_data.get('name', query)}**\n\n"
                    text += f"🔗 {user_data.get('html_url')}\n"
                    text += f"📝 {user_data.get('bio', 'N/A')}\n\n"
                    text += f"📂 Repo: {user_data.get('public_repos')}\n"
                    text += f"👥 Followers: {user_data.get('followers')}\n"
                    text += f"👀 Following: {user_data.get('following')}"
                else:
                    repo_data = data
                    text = f"📁 **{repo_data.get('name')}**\n\n"
                    text += f"🔗 {repo_data.get('html_url')}\n"
                    text += f"⭐ Stars: {repo_data.get('stargazers_count')}\n"
                    text += f"🍴 Forks: {repo_data.get('forks_count')}\n"
                    text += f"👁️ Watchers: {repo_data.get('watchers_count')}\n\n"
                    desc = repo_data.get('description', 'N/A')
                    text += f"📝 {desc[:200]}"
                
                await update.message.reply_text(text, parse_mode="Markdown")
            elif response.status_code == 404:
                await update.message.reply_text("Tidak ditemukan!")
            else:
                await update.message.reply_text(f"Error: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def gh_command(update, context):
    """Command /gh"""
    await github_command(update, context)

def register(application):
    """Register handler"""
    application.add_handler(CommandHandler("github", github_command))
    application.add_handler(CommandHandler("gh", gh_command))
