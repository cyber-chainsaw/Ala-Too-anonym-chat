# Anonymous Telegram Chat Bot

A professional anonymous chat bot for Telegram built with **Python**, **pyTelegramBotAPI**, and **SOLID** principles.

## Features
- **Random Pairing**: Instantly connect users for anonymous conversations.
- **Full Media Support**: Relay text, stickers, GIFs, photos, videos, voice notes, and "circles".
- **Premium Reveal**: Integrated **Telegram Stars (XTR)** payment system to reveal partner identities.
- **Safety First**: Automatic refunds if the reveal function encounters an error.
- **Professional Architecture**: Scalable code structure separating logic from interface.

## Project Structure
- `main.py`: The entry point that initializes and runs the bot.
- `bot_app.py`: Contains the `AnonymousBot` class and all Telegram handlers.
- `chat_manager.py`: Manages queues and active chat sessions.
- `.env`: (Local only) Stores your `BOT_TOKEN`.
- `.gitignore`: Ensures your secrets stay private.

## Setup Instructions

1. **Install Requirements**:
   ```bash
   pip install pyTelegramBotAPI python-dotenv
