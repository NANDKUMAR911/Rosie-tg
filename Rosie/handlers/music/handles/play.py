import re
from ..utils import youtube
from ..utils.play_handle import play_song
from Rosie.core.db import UserbotStatus
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon import errors
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import InputPeerNotifySettings


async def handle(event, userbot, vc):
    
    chat_id = event.chat_id 
    sender_id = event.sender_id
    assistant_id = userbot.me.id
    
    first_name = userbot.me.first_name
    username = userbot.me.username
    
    if not username:
        username = f"[{first_name}](tg://user?id={assistant_id})"
    else:
        username = f"`@{username}`"    
    
    # Check userbot status
    userbot_status = UserbotStatus(event.client, chat_id)
    status = await userbot_status.get_status(assistant_id)
    
            
    # conditions of userbot status
    if status in ["admin", "member", "owner"]:
        await play_handle(event, userbot, vc)
        return
        
    elif status == "banned":
        try:
            await event.client.edit_permissions(chat_id, assistant_id)
        except Exception as e:
            await event.reply(event.get_reply("userbot_banned", username=username)) 
            return
    
    # Try to fetch invite link from chat using bot
    try:
        chat_link = await event.client(ExportChatInviteRequest(chat_id))
        link = chat_link.link
    except Exception as e:
        await event.reply(event.get_reply("invite_permission"))
        return
    
    
    
    
    # finally send the process to play handle
    await play_handle(event, userbot, vc)
        
         

# Join chat using exported invite link
async def join_chat(client, chat_id, invite_link: str):
    # Join using exported invite link
    hash_ = invite_link.replace("https://t.me/+", "")
    result = await client(ImportChatInviteRequest(hash_))
    
    # mute the jouned channel
    await client(UpdateNotifySettingsRequest(
        peer=chat_id,
        settings=InputPeerNotifySettings(
            mute_until=2**31-1   # Unmute
        )
    ))
    
    return result 



# Function to extract youtube url from text
def extract_youtube_link(text: str):
    pattern = re.compile(
        r'(https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S*?)(?=https?://|\s|$)'
    )
    
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None




# play handle function
async def play_handle(event, userbot, vc):
    
    value = event.value
    command = event.command
    sender = await event.get_sender()
    first_name = sender.first_name
    username = sender.username
    sender_id = sender.id
    chat_id = event.chat_id
    
    mode = "song"
    
    if command == "vplay":
        mode = "video"
    
    if not value:
        await event.reply(event.get_reply("song_request"))
        return 
    
    
    text = extract_youtube_link(value)
    if not text:
        text = value
    
    try:
        await event.delete()
    except:
        pass
            
    sent = await event.reply(event.get_reply("searching_song"))
    try:
        video = await youtube.search_video(text)
    except:
        await sent.edit(event.get_reply("song_not_found"))
        return
    
    
    if not video:
        await sent.edit(event.get_reply("song_not_found"))
        return
    
    video["mode"] = mode
    video["req_by"] = {
        "chat_id" : chat_id,
        "user_id" : sender_id,
        "first_name" : first_name,
        "username" : username
    }
    
    await sent.delete()
    await play_song(event.client, vc, video)
    
    
    
        
    
    
    
    
        
        
        
    
               
    
    
               
    
    
