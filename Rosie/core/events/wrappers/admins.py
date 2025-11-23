


RIGHTS_DICT = {
    "change_info": "change info",
    "post_messages": "post messages",
    "edit_messages": "edit messages",
    "delete_messages": "delete messages",
    "ban_users": "ban users",
    "invite_users": "invite users",
    "pin_messages": "pin messages",
    "add_admins": "add admins",
    "anonymous": "anonymous",
    "manage_call": "manage call",
    "other": "other",
    "manage_topics": "manage topics",
    "post_stories": "post stories",
    "edit_stories": "edit stories",
    "delete_stories": "delete stories",
    "manage_direct_messages": "manage direct messages",
}









async def check(event, admins_only, owner_only, **perm):
    
    chat_id = event.chat_id
    sender_id = event.sender_id
    bot_id = event.me.id
    
    admins = event.admins 
    
    if event.is_private:
        return None 
    
    admin = None 
    bot = None 
    owner = None 
    
    for user in admins:
        
        if user.user_id == sender_id and user.is_owner:
            owner = user
            admin = user
        
        if user.user_id == sender_id and user.is_admin:
            admin = user 
        
        if user.user_id == bot_id:
            bot = user
    
    
    if owner_only and not owner:
        raise Exception (f"{event.get_reply('user_need_owner')}")   
    
    if admins_only and not admin:
        raise Exception (f"{event.get_reply('user_need_admin')}")   
   
    if perm:
        for key, value in perm.items():
            if key in RIGHTS_DICT and value:
                value = RIGHTS_DICT.get(key)
                
                bot_perm = bot.admin_rights
                user_perm = admin.admin_rights
                
                if not getattr(user_perm, key):
                    raise Exception (f"{event.get_reply('user_need_perm', perm=value)}")
                    
                    
                
        
        
        
              
        
                 
        
             
                
                
            
        
        