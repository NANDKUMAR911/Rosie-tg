"""
Module to manage Telegram group admins: caches admin lists, updates on promote/demote,
provides admin info, and supports reporting or auditing actions.
"""
from core.db import AdminsCache
from telethon.tl.types import (
    UpdateChannelParticipant,
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
    ChannelParticipantBanned,
    ChannelParticipantSelf,
    ChannelParticipant
)




async def handle(event):
    
    if not isinstance(event, UpdateChannelParticipant):
        return 
    
    client = event._client 
    
    member =  ChannelParticipant
    owner = ChannelParticipantCreator
    admin = ChannelParticipantAdmin
    bot = ChannelParticipantSelf
    banned = ChannelParticipantBanned
    
    chat_id = int(f"-100{event.channel_id}")
    prev = event.prev_participant
    new = event.new_participant
    
    chat_admins = AdminsCache(client, chat_id)
    
    update = False 
    
    if not prev or isinstance(prev, (banned)):
        if isinstance(new, (owner, admin, bot)):
            update = True 
    
    if isinstance(prev, (member, bot, admin, owner)):
        if isinstance(new, (member, bot, admin, owner)):
            update = True 
    
    if isinstance(prev, (bot, admin, owner)):
        if not new or isinstance(new, banned): 
            update = True  
    
    if update:
        await chat_admins.update_admins()
        
            
    