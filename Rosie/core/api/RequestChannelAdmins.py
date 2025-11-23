# ==========================================
# Full Channel Admins Request with Offset & Limit
# ==========================================

from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.channels import GetParticipantsRequest
from . import bitmask
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator
)








async def RequestChannelAdmins(client: TelegramClient, chat_id: int | str, offset: int = 0, limit: int = 100):
    """
    Fetches admins of a channel/group using offset and limit.

    Args:
        client (TelegramClient): Telethon client
        chat_id (int | str): Channel or group ID / username
        offset (int, optional): Starting offset. Defaults to 0.
        limit (int, optional): Number of admins to fetch. Defaults to 100.

    Returns:
        list: List of admin user objects
    """
    result = await client(GetParticipantsRequest(
        channel=chat_id,
        filter=ChannelParticipantsAdmins(),
        offset=offset,
        limit=limit,
        hash=0
    ))
    
    participants = result.participants
    users = result.users 
    
    admins = []
    
    for admin in participants:
        
        status = "admin" if isinstance(admin, ChannelParticipantAdmin) else "owner"
        info = None 
        
        for user in users:
            if user.id == admin.user_id:
                info = user
                break
        
        data = {
            "user_id" : admin.user_id,
            "status" : status,
            "first_name" : info.first_name,
            "last_name" : info.last_name,
            "username" : info.username,
            "bot": info.bot,
            "rank" : admin.rank,
            "admin_rights" : bitmask.encode_rights(admin.admin_rights)
        }
        
        admins.append(data)  
    
    return admins    
        
    
        
            
                
            
        