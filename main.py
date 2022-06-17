from core import HelperBot
import asyncio
import socket

from aiohttp import AsyncResolver, ClientSession, TCPConnector
from utils.config import TOKEN


bot = HelperBot()


async def main():
    async with ClientSession(
        connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET)
    ) as http_session:
        async with bot:
            bot.http_session = http_session

            await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
