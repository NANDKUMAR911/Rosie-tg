import asyncio  
from core.sql import execute  
from core.api import get_member_status  


# ------------------------------------------------------------
# _fetch_status():
# - Fetches the userbot status for a specific chat from the DB.
# - If not found, it tries to fetch status from Telegram using
#   get_member_status().
# - If fetching from Telegram fails (user not found / left),
#   it removes the existing record from DB.
# - If new status is fetched successfully, it schedules a task
#   to insert/update the status in the database.
# ------------------------------------------------------------
async def _fetch_status(client, chat_id, user_id):  
    query = "SELECT * FROM userbot_status WHERE chat_id = ?;"    
    status = await execute(query, (chat_id,))   

    # If status is missing in database
    if not status:  
        try:  
            # Try fetching directly from Telegram
            status = await get_member_status(client, chat_id, user_id)  
        except Exception as e:  
            # If Telegram fetch fails, delete corrupted DB entry
            query = "DELETE FROM userbot_status WHERE chat_id = ?;"  
            await execute(query, (chat_id,))  
            return None      

        # Save the fetched status to DB (async, non-blocking)
        asyncio.create_task(_insert_status(chat_id, status))  
        return status  

    else:  
        # If DB entry exists but is empty or invalid
        if not status:  
            return "not_member"      

        # Extract "status" field from the row
        status = status[0].get("status", "not_member")  
        return status      


# ------------------------------------------------------------
# _update_status():
# - Always fetches fresh status from Telegram
# - If Telegram fetch fails, delete DB entry
# - Saves the updated status asynchronously
# ------------------------------------------------------------
async def _update_status(client, chat_id, user_id):  
    try:  
        status = await get_member_status(client, chat_id, user_id)  
    except Exception as e:  
        query = "DELETE FROM userbot_status WHERE chat_id = ?;"  
        await execute(query, (chat_id,))  
        return None  

    # Save updated status in the background
    asyncio.create_task(_insert_status(chat_id, status))  
    return status  


# ------------------------------------------------------------
# _insert_status():
# - Inserts or updates a chat's status in the userbot_status table
#   using ON CONFLICT(chat_id) DO UPDATE.
# ------------------------------------------------------------
async def _insert_status(chat_id, status):  
    query = """
    INSERT INTO userbot_status (chat_id, status)
    VALUES (?, ?)
    ON CONFLICT(chat_id) DO UPDATE SET
        status = excluded.status;
    """  
      
    await execute(query, (chat_id, status))                  


# ------------------------------------------------------------
# UserbotStatus class:
# - A helper class for managing userbot status for a chat.
# - Provides methods to fetch or update the status.
# ------------------------------------------------------------
class UserbotStatus:  
    def __init__(self, client, chat_id):  
        self.client = client  
        self.chat_id = chat_id   
      
    # Get userbot status (from DB or Telegram fallback)
    async def get_status(self, user_id: int):  
        status = await _fetch_status(self.client, self.chat_id, user_id)  
        return status  
      
    # Update status from Telegram and store in DB
    async def update_status(self, user_id: int):  
        return await _update_status(self.client, self.chat_id, user_id)