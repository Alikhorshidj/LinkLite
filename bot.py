import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from summarizer import summarize_url

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋 لینک مقاله یا فایل PDF خودتو بفرست تا خلاصه‌ش رو برات بیارم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("http"):
        await update.message.reply_text("⏳ در حال خواندن مقاله...")
        summary = summarize_url(text)
        await update.message.reply_text(summary or "متأسفم، نتونستم خلاصه کنم 😢")
    else:
        await update.message.reply_text("لطفاً یک لینک معتبر بفرست 🌐")

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
