import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dictionary to store active groups
active_groups = set()

# Command to enable the bot in the group
async def enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_groups.add(chat_id)
    await update.message.reply_text("Bio link protection has been ENABLED in this group!")

# Command to deactivate the bot in the group
async def deactivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_groups:
        active_groups.remove(chat_id)
        await update.message.reply_text("Bio link protection has been DISABLED in this group!")
    else:
        await update.message.reply_text("Bio link protection is already disabled in this group.")

# Message handler to check for bio links
async def check_bio_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_groups:
        # Regular expression to detect bio links
        bio_link_pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?bio\.link\/\S+', re.IGNORECASE)
        if bio_link_pattern.search(update.message.text):
            await update.message.delete()
            await update.message.reply_text("Message containing a bio link has been deleted!", quote=False)

def main():
    # Create an instance of the application
    from config import BOT_TOKEN
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("enable", enable))
    application.add_handler(CommandHandler("deactivate", deactivate))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_bio_link))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()