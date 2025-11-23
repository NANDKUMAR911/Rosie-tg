import asyncio
import functools
from telethon import events, errors
from core.db import AdminsCache 
from .wrappers import admins as admins_cache
from core.replies import font_style, get_reply



def MessageEvents(admins_only=False, owner_only=False, group=False, private=False, channel=False, **perm):
    """
    Decorator for Telethon event handlers.
    Handles:
      • Error catching
      • Command parsing
      • Admin checks
      • Group/Private/Channel restrictions
      • Disabled commands
      • Mention parsing (/ban @user 3d)
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event, *args, **kwargs):
            
            if not event.sender_id:
                return
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
            # Command Parsing
            # ─────────────────────────────────────────────────────
            event.prefix = None
            event.command = None
            event.value = None

            if event.pattern_match:
                try:
                    event.prefix = event.pattern_match.group(1)
                except:
                    pass

                try:
                    event.command = event.pattern_match.group(2)
                except:
                    pass

                try:
                    event.value = event.pattern_match.group(3)
                except:
                    pass

            
            # ─────────────────────────────────────────────────────
            # Chat Type Restriction Check
            # ─────────────────────────────────────────────────────
            restrict_chat = None

            if private and not event.is_private:
                restrict_chat = event.get_reply("pm_only")

            elif group and not event.is_group:
                restrict_chat = event.get_reply("group_only")

            elif channel and not event.is_channel:
                restrict_chat = event.get_reply("channel_only")

            elif channel and event.is_group:
                restrict_chat = event.get_reply("channel_only")

            elif not channel and event.is_channel and not event.is_group:
                return

            if restrict_chat:
                await event.reply(restrict_chat)
                return

            # ─────────────────────────────────────────────────────
            # Admin Checks (admins_only / owner_only)
            # ─────────────────────────────────────────────────────
            if admins_only or owner_only:
                try:
                    await admins_cache.check(event, admins_only, owner_only, **perm)
                except Exception as e:
                    await event.reply(f"{e}")
                    return

            

            # ─────────────────────────────────────────────────────
            # Main Handler Execution + Error Handling
            # ─────────────────────────────────────────────────────
            try:
                await func(event, *args, **kwargs)  
                         # ────────────────── Entity Not Found Fix ──────────────────
            except Exception as e:
                e = str(e)
                raise e
                error_msg = font_style.to_smallcaps(e)
                await event.reply(error_msg)

        return wrapper

    return decorator