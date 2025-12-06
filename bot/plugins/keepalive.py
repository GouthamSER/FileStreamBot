# keepalive.py
import asyncio
import aiohttp
from bot.config import Server


PING_INTERVAL = 180  # 3 minutes


async def keep_alive():
    """Pings your server every 3 minutes to prevent sleeping."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(Server.BASE_URL) as resp:
                    print(f"[KEEPALIVE] Pinged {Server.BASE_URL} → Status {resp.status}")
            except Exception as e:
                print(f"[KEEPALIVE ERROR] {e}")
            await asyncio.sleep(PING_INTERVAL)

# Start keepalive background task
    #asyncio.create_task(keep_alive()) in bot.py or main.py
