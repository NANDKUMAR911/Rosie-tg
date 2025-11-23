"""
Register all bot command handlers here.
"""
from telethon import events
from core.events import MessageEvents
from .handles import (
    admins_cache
)



def register(bot):
    
    # ============================================================
    # Raw events to cache admins list
    # ============================================================
    @bot.on(events.Raw)
    async def cache_admins_handle(event):
        await admins_cache.handle(event)      
        
        
        







