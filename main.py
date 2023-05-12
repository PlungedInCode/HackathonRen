from dotenv import load_dotenv

from bot.bot_main import Bot
from db.db_api import Database

if __name__ == '__main__':
    load_dotenv()
    db = Database()
    bot = Bot(db)
    bot.bot.run_polling()
