from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.types import (
    ChannelParticipant,
    ChannelParticipantSelf,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantBanned
)




async def get_member_status(client, chat_id, user_id):
    
    try:
        result = await client(GetParticipantRequest(
            channel=chat_id,
            participant=user_id
        ))
    except UserNotParticipantError:
        return "not_member"  
    except Exception as e:
        raise e     
    
    participant = result.participant
    
    if not participant:
        return "not_member"
    
    if isinstance(participant, (ChannelParticipantSelf, ChannelParticipant)):
        return "member"
    elif isinstance(participant, ChannelParticipantAdmin):
        return "admin"
    elif isinstance(participant, ChannelParticipantCreator):
        return "owner"      
    elif isinstance(participant, ChannelParticipantBanned):
        return "banned"      
            