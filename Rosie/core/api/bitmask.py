# ==========================================
# Bitmask Encode/Decode for ChatAdminRights
# ==========================================

from telethon.tl.types import ChatAdminRights


# Order of rights bits — do not change sequence
RIGHTS_ORDER = [
    "change_info",
    "post_messages",
    "edit_messages",
    "delete_messages",
    "ban_users",
    "invite_users",
    "pin_messages",
    "add_admins",
    "anonymous",
    "manage_call",
    "other",
    "manage_topics",
    "post_stories",
    "edit_stories",
    "delete_stories",
    "manage_direct_messages",
]


# ==========================================
# Encode ChatAdminRights → Integer Bitmask
# ==========================================
def encode_rights(rights: ChatAdminRights) -> int:
    bitmask = 0
    for i, key in enumerate(RIGHTS_ORDER):
        if getattr(rights, key, False):
            bitmask |= (1 << i)
    return bitmask


# ==========================================
# Decode Integer Bitmask → ChatAdminRights
# ==========================================
def decode_rights(number: int) -> ChatAdminRights:
    kwargs = {}
    for i, key in enumerate(RIGHTS_ORDER):
        kwargs[key] = bool(number & (1 << i))
    return ChatAdminRights(**kwargs)