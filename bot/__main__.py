# bot/__main__.py
import asyncio
from bot import TelegramBot
from bot.server import server
from keepalive import keep_alive


async def start_all():
    # Start KEEPALIVE loop (background)
    asyncio.create_task(keep_alive())

    # Start your web server task
    asyncio.create_task(server.serve())

    # Start the Telegram bot
    await TelegramBot.start()
    print("Bot is running with WebServer + KeepAlive.")

    # Idle loop (keep running)
    from hydrogram.idle import idle
    await idle()

    # On shutdown
    await TelegramBot.stop()


if __name__ == "__main__":
    asyncio.run(start_all())
