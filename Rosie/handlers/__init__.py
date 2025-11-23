"""
register_clients(clients) is responsible for distributing the Clients
instance to all handler modules.

The 'clients' object contains:
- bot client
- userbot client
- pytgcalls / voice client (if any)

Each handler (group, music, admin, user, callback, etc.) will receive
this same clients instance so they can access:
- send/receive messages from bot
- manage chats
- edit messages
- handle music / vc actions
- process updates

In short:
This function connects all modules to the same Clients object so the
entire project works with shared clients instead of multiple instances.
"""
from . import (
    group,
    music
)






def register_clients(bot, userbot, vc):
    group.register(bot)
    music.register(bot, userbot, vc)
    