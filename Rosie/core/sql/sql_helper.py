import os
import sqlite3
import asyncio
import json
from typing import List, Tuple, Union, Optional, Any, Dict

DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIR, "Daisy.db")
SCHEMA_PATH = os.path.join(DIR, "schema.sql")

INIT_LOCK = asyncio.Lock()  # ensures single init at a time
INIT_DONE = False  # schema applied only once


async def _init_db() -> None:
    global INIT_DONE
    if INIT_DONE:
        return

    async with INIT_LOCK:  # prevent race conditions
        if INIT_DONE:
            return

        db_created = False

        if not os.path.exists(DB_PATH):
            open(DB_PATH, "w").close()
            db_created = True

        if db_created and os.path.exists(SCHEMA_PATH):
            # run schema in background thread safely
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            await asyncio.to_thread(_exec_script, schema_sql)

        INIT_DONE = True  # only after schema applied


def _exec_script(sql_script: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql_script)
        conn.commit()
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    d = {}
    for k in row.keys():
        val = row[k]
        if isinstance(val, int) and val in (0, 1):
            val = bool(val)
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except:
                pass
        d[k] = val
    return d


# -----------------------------
# Execute single query
# -----------------------------
async def execute(query: str, data: Optional[Union[Tuple, list]] = None) -> Optional[List[Dict]]:
    # Ensure DB + schema ready before running query
    await _init_db()

    def _run():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query, data or ())
            conn.commit()

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                return [_row_to_dict(row) for row in rows]
            return None
        finally:
            cursor.close()
            conn.close()

    return await asyncio.to_thread(_run)


# -----------------------------
# Execute many
# -----------------------------
async def execute_many(query: str, data_list: List[Tuple]) -> None:
    await _init_db()

    def _run():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.executemany(query, data_list)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    return await asyncio.to_thread(_run)


# -----------------------------
# Execute script list
# -----------------------------
async def execute_script(script_list: List[str]) -> None:
    await _init_db()

    def _run():
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.executescript("\n".join(script_list))
            conn.commit()
        finally:
            conn.close()

    return await asyncio.to_thread(_run)