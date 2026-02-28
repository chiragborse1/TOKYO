from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from core.agent import chat, clear_history
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🗼 TOKYO is online!\n\nI'm your personal AI agent. How can I help you today?"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command"""
    result = clear_history()
    await update.message.reply_text(f"🗑️ {result}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    user_message = update.message.text
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    # Get response from TOKYO
    response = chat(user_message)
    
    # Send response
    await update.message.reply_text(response)

async def error_handler(update, context):
    """Handle errors"""
    print(f"Error: {context.error}")

def run_bot():
    """Start the Telegram bot"""
    print("🗼 TOKYO Telegram Bot starting...")
    
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("✅ TOKYO Bot is running! Open Telegram and message your bot.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    run_bot()