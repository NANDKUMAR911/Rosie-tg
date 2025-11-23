"""
Register all bot command handlers here.
"""
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls import filters as call_filters
from telethon import events
from core.events import MessageEvents, CallbackEvents, command_pattern
from .handles import (
    userbot_status,
    play,
    control_commands
)



def register(bot, userbot, vc):
    
    # ============================================================
    # play
    # ============================================================
    @bot.on(events.NewMessage(pattern=command_pattern("play|vplay")))
    @MessageEvents(group=True)
    async def play_command(event):
        await play.handle(event, userbot, vc)  
    
    
    # ============================================================
    # skip
    # ============================================================
    @bot.on(events.NewMessage(pattern=command_pattern("skip|end")))
    @MessageEvents(group=True, admins_only=True)
    async def skip_command(event):
        await control_commands.handle(event, vc)  
    
    
    @bot.on(events.CallbackQuery(pattern=b"music_"))
    @CallbackEvents(admins_only=True)
    async def music_button_handler(event):
        await control_commands.buttons_handle(event, vc)
        
        
        
    # ============================================================
    # Raw Event on Usebot status change
    # ============================================================
    @userbot.on(events.Raw)
    async def _userbot_cache(event):
        await userbot_status.handle(event, bot)
    
    
    @vc.on_update(call_filters.stream_end())
    async def handler(client: PyTgCalls, update: Update):
        await control_commands.on_stream_ended(update, bot, vc)
    






