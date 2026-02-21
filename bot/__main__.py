import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from log_setup.logging import setup_logging
from db.database import init_db
from keyboards.menu_commands import set_main_menu

from handlers.user import router as user_router
from handlers.admin import router as admin_router

async def main():

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🚀 Bot starting...")

    # Load configuration
    config: Config = load_config('.env')

    # Create bot and set token
    bot = Bot(config.bot.token)
    dp = Dispatcher()

    # Initialize database
    await init_db()

    # Setup main menu commands
    await set_main_menu(bot)

    # Include routers
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Create global variables for the project
    admin_ids = config.bot.admin_ids
    CHANNEL_ID = config.channal.id
    CHANNEL_URL = config.channal.url

    # Start polling and pass global variables
    await dp.start_polling(
        bot,
        admin_ids=admin_ids, CHANNEL_ID=CHANNEL_ID, CHANNEL_URL=CHANNEL_URL
    )


if __name__ == "__main__":
    asyncio.run(main())
