import os
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace with your bot's API token
YOUR_API_TOKEN = "6563477780:AAGfcroEPTWFcprx5ugI5R8L7NQXgv5dqxI"

# Download directory for content
DOWNLOAD_DIR = "ktz-Download"


def download_content(update, context):
    """Downloads content from a user-provided link."""
    chat_id = update.effective_chat.id

    # Check if a text message is present
    if not update.message.text:
        context.bot.send_message(chat_id, "Please send a link to download content.")
        return

    # Extract the link from the message
    user_link = update.message.text

    # Implement checks for valid URL format (optional)

    # Create download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    try:
        # Perform a GET request to the user-provided link (replace with appropriate API calls if used)
        response = requests.get(user_link, stream=True)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Get filename from URL or response headers (consider using more robust naming)
        filename = os.path.basename(user_link)
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        # Download the content in chunks
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        context.bot.send_message(chat_id, f"Content downloaded successfully! (Path: {filepath})")
    except requests.exceptions.RequestException as e:
        context.bot.send_message(chat_id, f"Failed to download content: {e}")
    except Exception as e:
        # Handle other potential errors
        context.bot.send_message(chat_id, f"An unexpected error occurred: {e}")


def main():
    """Starts the bot."""
    updater = Updater(YOUR_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handle text messages containing download links
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_content))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
