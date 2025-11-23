from core.db import UserbotStatus
from telethon.tl.types import (
    UpdateChannel
)




async def handle(event, bot):
    
    if not isinstance(event, UpdateChannel):
        return 
    
    client = event._client 
    chat_id = int(f"-100{event.channel_id}")
    chat_userbot = UserbotStatus(bot, chat_id)
    
    await chat_userbot.update_status(client.me.id)
        