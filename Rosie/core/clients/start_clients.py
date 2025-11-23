from . import config
from pytgcalls import PyTgCalls
from pytgcalls import idle
from telethon import TelegramClient
from telethon.sessions import StringSession
from handlers import register_clients

api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
session_string = config.SESSION_STRING


async def start_clients():

    # BOT
    bot = TelegramClient("Rosie", api_id, api_hash)
    await bot.start(bot_token=bot_token)
    bot.me = await bot.get_me()
    print(f"BOT STARTED : {bot.me.first_name}")
    
    
    # USERBOT
    userbot = TelegramClient(StringSession(session_string), api_id, api_hash)
    
    # VC
    vc = PyTgCalls(userbot)
    await vc.start()
    
    userbot.me = await userbot.get_me()
    print(f"USERBOT STARTED : {userbot.me.first_name}")
    

    # register clients
    register_clients(bot, userbot, vc)
    return bot