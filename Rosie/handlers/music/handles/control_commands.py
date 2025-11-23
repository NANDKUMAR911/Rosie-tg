import asyncio
from ..utils.play_handle import play_next_song, end_song, pause_song, resume_song
from telethon import Button




async def handle(event, vc):
    
    command = event.command
    
    if command == "skip":
        await skip_handle(event, vc)
    elif command == "end":
        await end_handle(event, vc)

    
async def end_handle(event, vc):
    
    try:
        await end_song(event.client, event.chat_id, vc)
    except Exception as e:
        if "bot not streaming" in str(e):
            await event.reply(event.get_reply("bot_not_streaming"))
        else:
            await event.reply(f"{e}")
        return 
    
    try:
        await event.delete()
    except:
        pass    
    
    sent = await event.reply(event.get_reply("ended"))
    
    await asyncio.sleep(2)
    await sent.delete()    
        
          
    

async def skip_handle(event, vc):
    try:
        await play_next_song(event.client, event.chat_id, vc)
    except Exception as e:
        if "bot not streaming" in str(e):
            await event.reply(event.get_reply("bot_not_streaming"))
        else:
            await event.reply(f"{e}")
        return    
    
    try:
        await event.delete()
    except:
        pass 
        
    sent = await event.reply(event.get_reply("skipped"))
    
    await asyncio.sleep(2)
    await sent.delete()
    
    

async def on_stream_ended(update, bot, vc):
    chat_id = update.chat_id
    try:
        played = await play_next_song(bot, chat_id, vc)
    except Exception as e:
        try:
            await bot.send_message(chat_id, f"{e}")
        except:
            pass   
            
            


async def buttons_handle(event, vc):
    
    data = event.data.decode("utf-8")   # example: music_skip, music_end
    chat_id = event.chat_id
    
    if data == "music_seekbar":
        await event.asnwer()
        return
    
    if data == "music_stop":
        try:
            await end_song(event.client, event.chat_id, vc)
            await event.answer()    
        except Exception as e:
            if "bot not streaming" in str(e):
                await event.answer(event.get_reply("bot_not_streaming"), alert=True)
            else:
                await event.answer(f"{e}")
        return 
    
    
    elif data == "music_pause":
        resume_icon = "▷"  
        msg = await event.get_message()
        buttons = msg.buttons
        
        msg_id = msg.id
        
        
        new_btn = []
        for row in buttons:
            new_row = []
            
            for btn in row:
                if "music_pause" in str(btn.data):
                    new_row.append(Button.inline(resume_icon, b"music_resume"))
                else:
                    new_row.append(Button.inline(btn.text, btn.data))
            
            new_btn.append(new_row)
        
        try:
            await pause_song(chat_id, msg_id, vc)
            await event.edit(buttons=new_btn)    
        except Exception as e:
            if "bot not streaming" in str(e):
                await event.answer(event.get_reply("bot_not_streaming"), alert=True)
            elif "This is not current playing message id." in str(e):
                await event.answer(event.get_reply("current_playing_controls"))
            else:    
                pass
        
        
                            
    
    
    elif data == "music_resume":
        pause_icon = "।।"  
        msg = await event.get_message()
        buttons = msg.buttons
        
        new_btn = []
        for row in buttons:
            new_row = []
            
            for btn in row:
                if "music_resume" in str(btn.data):
                    new_row.append(Button.inline(pause_icon, b"music_pause"))
                else:
                    new_row.append(Button.inline(btn.text, btn.data))
            
            new_btn.append(new_row)
        
        try:
            await resume_song(chat_id, msg_id, vc)
            await event.edit(buttons=new_btn)    
        except Exception as e:
            if "bot not streaming" in str(e):
                await event.answer(event.get_reply("bot_not_streaming"), alert=True)
            elif "This is not current playing message id." in str(e):
                await event.answer(event.get_reply("current_playing_controls"))
            else:    
                pass               
            
            
        
        
           
            
                
            
        