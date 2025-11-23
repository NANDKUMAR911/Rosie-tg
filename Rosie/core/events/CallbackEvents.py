import asyncio
import functools
from telethon import events, errors
from core.db import AdminsCache 
from .wrappers import admins as admins_cache
from core.replies import font_style, get_reply



prevent = {}

async def remove_prevent(user_id):
    await asyncio.sleep(1)
    if user_id in prevent:
        prevent.pop(user_id)
    


def CallbackEvents(admins_only=False, owner_only=False, **perm):
    """
    Decorator for Telethon callback event handlers.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event, *args, **kwargs):
            
            clicker_id = event.sender_id
            
            if clicker_id in prevent:
                await event.answer()
                asyncio.create_task(remove_prevent(clicker_id))
                return
            
            prevent[clicker_id] = True
            
            
            # ─────────────────────────────────────────────────────
            # Basic Setup
            # ─────────────────────────────────────────────────────
            client = event.client
            chat_id = event.chat_id
            sender_id = event.sender_id

            event.me = client.me
            event.get_reply = lambda key, **kw: get_reply(key, **kw)

            chat_admins = AdminsCache(client, chat_id)
            
            event.admins = []
            
            
            # Fetch admin list + disabled commands
            if not event.is_private:
                _admins = await chat_admins.get_admins()
                event.admins = _admins.admins


            # ─────────────────────────────────────────────────────
            # Admin Checks (admins_only / owner_only)
            # ─────────────────────────────────────────────────────
            if admins_only or owner_only:
                try:
                    await admins_cache.check(event, admins_only, owner_only, **perm)
                except Exception as e:
                    await event.answer(f"{e}", alert=True)
                    return

            

            # ─────────────────────────────────────────────────────
            # Main Handler Execution + Error Handling
            # ─────────────────────────────────────────────────────
            try:
                await func(event, *args, **kwargs)  
                         # ────────────────── Entity Not Found Fix ──────────────────
            except Exception as e:
                e = str(e)
                print(e)
                error_msg = font_style.to_smallcaps(e)
                await event.answer()

        return wrapper

    return decorator