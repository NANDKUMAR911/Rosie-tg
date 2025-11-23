-- ========================================================
-- DATABASE SCHEMA: Daisy.db
-- Tables: users, posts
-- Compatible with async sqlite helper (sqlite.py)
-- ========================================================

-- ----------------------------
-- ADMINS_CACHE TABLE
-- ----------------------------
CREATE TABLE IF NOT EXISTS admins_cache (
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    bot BOOLEAN DEFAULT 0,
    rank TEXT,
    admin_rights INTEGER,
    PRIMARY KEY (chat_id, user_id)
);


-- ----------------------------
-- userbot_status TABLE
-- ----------------------------
CREATE TABLE IF NOT EXISTS userbot_status (
    chat_id INTEGER PRIMARY KEY,
    status TEXT NOT NULL
);