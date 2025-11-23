"""
Module: admins_cache Helper
Purpose: Provides helper functions to handle SQL queries for the
admins_cache table, storing Telegram group admin info such as
chat ID, user ID, username, name, bot status, rank, and admin_rights.
"""
import asyncio
from telethon import TelegramClient
from core.api import RequestChannelAdmins, bitmask
from core.sql import execute, execute_many



__lock__ = {}

class AdminsCache:
    
    
    def __init__(self, client: TelegramClient, chat_id: int):
        self.client = client
        self.chat_id = chat_id
    
    """
    SQL QUERIES FOR ADMINS_CACHE TO GET OR INSERT ADMINS IN SQLITE
    """   
    async def _fetch_admins(self):
        query = "SELECT * FROM admins_cache WHERE chat_id = ?;"
        results = await execute(query, (self.chat_id,))
        return results
    
    async def _cache_admins(self, data: list):
        admins_list = []
        chat_id = self.chat_id
        
        for user in data:
            user_id = user.get("user_id")
            status = user.get("status")
            first_name = user.get("first_name", "deleted account")
            last_name = user.get("last_name")
            username = user.get("username")
            bot = user.get("bot")
            rank = user.get("rank")
            rights = user.get("admin_rights", 0)
            
            tup = (chat_id, user_id, status, username, first_name, last_name, bot, rank, rights)
            admins_list.append(tup)
        
        
        delete_query = "DELETE FROM admins_cache WHERE chat_id = ?;"    
            
        insert_query = """INSERT INTO admins_cache (
            chat_id,
            user_id,
            status,
            username,
            first_name,
            last_name,
            bot,
            rank,
            admin_rights
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(chat_id, user_id) DO UPDATE
        SET 
            status = excluded.status,
            username = excluded.username,
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            bot = excluded.bot,
            rank = excluded.rank,
            admin_rights = excluded.admin_rights;"""
        
        await execute(delete_query, (chat_id,))
        await execute_many(insert_query, admins_list)
        
        
        
    """
    CALLABLE METHODS
    """
    async def get_admins(self):
        admins = await self._fetch_admins()
        
        if not admins and self.chat_id not in __lock__:
            __lock__[self.chat_id] = True
            try:
                admins = await RequestChannelAdmins(self.client, self.chat_id)
            except Exception as e:
                admins = []
            
            asyncio.create_task(self._cache_admins(admins))  
        
        
        return ChatAdmins(self.chat_id, admins) 
    
    
    async def update_admins(self):
        try:
            admins = await RequestChannelAdmins(self.client, self.chat_id)
            asyncio.create_task(self._cache_admins(admins)) 
        except Exception as e:
            admins = []
            asyncio.create_task(self._cache_admins(admins))
                 
        return ChatAdmins(self.chat_id, admins) 
          
        
        
        
         
         
    
        
        
        
        


"""
HELPER CLASS FOR ADMINS 
"""   

class ChatAdmins:
    def __init__(self, chat_id: int, admins_list: list):
        
        self.chat_id = chat_id
        self.admins = []
        
        for user in admins_list:
            self.admins.append(Admin(user))
    
    
    def __repr__(self):
        return f"""ChatAdmins(
            chat_id = {self.chat_id},
            admins = {self.admins})
        """
     
            
class Admin:
    def __init__(self, user: dict):
        
        status = user.get("status")
        
        self.user_id = user.get("user_id")
        self.is_admin = True
        self.is_owner = True if status=="owner" else False
        self.first_name = user.get("first_name", "deleted account")
        self.last_name = user.get("last_name")
        self.username = user.get("username")
        self.bot = user.get("bot")
        rank = user.get("rank")
        
        if not rank:
            rank = "Owner" if status == "Owner" else "Admin"
        self.rank = rank    
            
        rights = user.get("admin_rights", 0)
        self.admin_rights = bitmask.decode_rights(rights)
    
    def __repr__(self):
        return f"""Admin(user_id = {self.user_id}
        is_admin = {self.is_admin},
        is_owner = {self.is_owner},
        first_nane = {self.first_name},
        last_name = {self.last_name},
        username = {self.username},
        bot = {self.bot},
        rank = {self.rank}, 
        admin_rights = {self.admin_rights})
        """   
        
        
        
        
        
                
                
        
        
          
        
        


