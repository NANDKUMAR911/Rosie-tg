import os
import asyncio
from quart import Quart
from core.clients import start_clients

app = Quart(__name__)

@app.get("/")
async def home():
    return {"status": "Bot running!"}


async def main():
    # Get port from ENV or use default 10000
    port = int(os.getenv("PORT", "5000"))

    # Start Telegram bot + userbot + pytgcalls in background
    bot_task = asyncio.create_task(start_clients())

    # Start Quart web server
    web_task = asyncio.create_task(
        app.run_task(host="0.0.0.0", port=port)
    )

    # Keep both tasks alive
    await asyncio.gather(bot_task, web_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")