import os
from dotenv import load_dotenv
from bot_app import AnonymousBot

def main():
    
    load_dotenv()
    
    if not os.getenv("BOT_TOKEN"):
        raise ValueError("BOT_TOKEN не найден в .env файле!")

    app = AnonymousBot()
    app.run()

if __name__ == "__main__":
    main()
