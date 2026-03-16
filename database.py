import aiosqlite
import logging
from pathlib import Path
from typing import Optional
from moebot.config import DB_PATH

logger = logging.getLogger(__name__)

db_path = Path(DB_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

class Database:
    def __init__(self):
        self.conn: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        """Connect ke database dan jalankan migrasi"""
        self.conn = await aiosqlite.connect(str(db_path))
        self.conn.row_factory = aiosqlite.Row
        await self.migrate()
        logger.info("Database terhubung")
    
    async def close(self):
        """Tutup koneksi database"""
        if self.conn:
            await self.conn.close()
            logger.info("Database ditutup")
    
    async def migrate(self):
        """Jalankan migrasi schema database"""
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                is_admin INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                username TEXT,
                is_admin INTEGER DEFAULT 0,
                welcome_enabled INTEGER DEFAULT 1,
                welcome_text TEXT DEFAULT 'Selamat datang {name}!',
                goodbye_enabled INTEGER DEFAULT 0,
                goodbye_text TEXT DEFAULT 'Selamat tinggal {name}',
                captcha_enabled INTEGER DEFAULT 0,
                antiflood_enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS plugin_states (
                plugin_name TEXT PRIMARY KEY,
                enabled INTEGER DEFAULT 1,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER,
                setting_key TEXT,
                setting_value TEXT,
                PRIMARY KEY (user_id, setting_key)
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                name TEXT,
                content TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, name)
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                keyword TEXT,
                response TEXT,
                created_by INTEGER,
                is_regex INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS warns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS flooders (
                user_id INTEGER,
                chat_id INTEGER,
                count INTEGER DEFAULT 0,
                last_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, chat_id)
            )
        """):
            pass
        
        async with self.conn.execute_fetchall("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                messages_today INTEGER DEFAULT 0,
                messages_total INTEGER DEFAULT 0,
                date DATE DEFAULT (date('now'))
            )
        """):
            pass
        
        await self.conn.commit()
        logger.info("Migrasi database selesai")
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        """Ambil data user"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str = None):
        """Tambah atau update user"""
        await self.conn.execute("""
            INSERT INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                last_seen = CURRENT_TIMESTAMP
        """, (user_id, username, first_name, last_name))
        await self.conn.commit()
    
    async def get_group(self, chat_id: int) -> Optional[dict]:
        """Ambil data grup"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM groups WHERE chat_id = ?", (chat_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def add_group(self, chat_id: int, title: str, username: str = None):
        """Tambah atau update grup"""
        await self.conn.execute("""
            INSERT INTO groups (chat_id, title, username)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                title = excluded.title,
                username = excluded.username
        """, (chat_id, title, username))
        await self.conn.commit()
    
    async def get_plugin_state(self, plugin_name: str) -> bool:
        """Ambil status plugin"""
        async with self.conn.execute_fetchall(
            "SELECT enabled FROM plugin_states WHERE plugin_name = ?", (plugin_name,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] == 1 if row else True
    
    async def set_plugin_state(self, plugin_name: str, enabled: bool):
        """Set status plugin"""
        await self.conn.execute("""
            INSERT INTO plugin_states (plugin_name, enabled)
            VALUES (?, ?)
            ON CONFLICT(plugin_name) DO UPDATE SET
                enabled = excluded.enabled,
                updated_at = CURRENT_TIMESTAMP
        """, (plugin_name, enabled))
        await self.conn.commit()
    
    async def get_all_plugins(self) -> list:
        """Ambil semua plugin dan statusnya"""
        async with self.conn.execute_fetchall(
            "SELECT plugin_name, enabled FROM plugin_states"
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"name": r[0], "enabled": r[1]} for r in rows]
    
    async def set_user_admin(self, user_id: int, is_admin: bool, chat_id: int = None):
        """Set user sebagai admin"""
        if chat_id:
            await self.conn.execute(
                "UPDATE users SET is_admin = ? WHERE user_id = ?", (is_admin, user_id)
            )
        else:
            await self.conn.execute(
                "UPDATE users SET is_admin = ? WHERE user_id = ?", (is_admin, user_id)
            )
        await self.conn.commit()
    
    async def set_user_banned(self, user_id: int, is_banned: bool):
        """Ban/unban user"""
        await self.conn.execute(
            "UPDATE users SET is_banned = ? WHERE user_id = ?", (is_banned, user_id)
        )
        await self.conn.commit()
    
    async def is_user_banned(self, user_id: int) -> bool:
        """Cek apakah user dibanned"""
        async with self.conn.execute_fetchall(
            "SELECT is_banned FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] == 1 if row else False
    
    async def is_admin(self, user_id: int, chat_id: int = None) -> bool:
        """Cek apakah user admin"""
        async with self.conn.execute_fetchall(
            "SELECT is_admin FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] == 1 if row else False
    
    async def save_note(self, chat_id: int, name: str, content: str, user_id: int):
        """Simpan note"""
        await self.conn.execute("""
            INSERT INTO notes (chat_id, name, content, created_by)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(chat_id, name) DO UPDATE SET
                content = excluded.content,
                created_by = excluded.created_by
        """, (chat_id, name, content, user_id))
        await self.conn.commit()
    
    async def get_note(self, chat_id: int, name: str) -> Optional[dict]:
        """Ambil note"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM notes WHERE chat_id = ? AND name = ?", (chat_id, name)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_notes(self, chat_id: int) -> list:
        """Ambil semua note di grup"""
        async with self.conn.execute_fetchall(
            "SELECT name FROM notes WHERE chat_id = ?", (chat_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]
    
    async def delete_note(self, chat_id: int, name: str) -> bool:
        """Hapus note"""
        cursor = await self.conn.execute(
            "DELETE FROM notes WHERE chat_id = ? AND name = ?", (chat_id, name)
        )
        await self.conn.commit()
        return cursor.rowcount > 0
    
    async def add_filter(self, chat_id: int, keyword: str, response: str, user_id: int, is_regex: bool = False):
        """Tambah filter"""
        await self.conn.execute("""
            INSERT INTO filters (chat_id, keyword, response, created_by, is_regex)
            VALUES (?, ?, ?, ?, ?)
        """, (chat_id, keyword, response, user_id, is_regex))
        await self.conn.commit()
    
    async def get_filters(self, chat_id: int) -> list:
        """Ambil semua filter di grup"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM filters WHERE chat_id = ?", (chat_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    
    async def delete_filter(self, chat_id: int, keyword: str) -> bool:
        """Hapus filter"""
        cursor = await self.conn.execute(
            "DELETE FROM filters WHERE chat_id = ? AND keyword = ?", (chat_id, keyword)
        )
        await self.conn.commit()
        return cursor.rowcount > 0
    
    async def update_flood_count(self, user_id: int, chat_id: int) -> int:
        """Update count flood dan return count"""
        await self.conn.execute("""
            INSERT INTO flooders (user_id, chat_id, count)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, chat_id) DO UPDATE SET
                count = count + 1,
                last_message = CURRENT_TIMESTAMP
        """, (user_id, chat_id))
        await self.conn.commit()
        
        async with self.conn.execute_fetchall(
            "SELECT count FROM flooders WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
    
    async def reset_flood_count(self, user_id: int, chat_id: int):
        """Reset count flood"""
        await self.conn.execute(
            "DELETE FROM flooders WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        )
        await self.conn.commit()
    
    async def add_warn(self, user_id: int, chat_id: int, reason: str = None):
        """Tambah warn"""
        await self.conn.execute(
            "INSERT INTO warns (user_id, chat_id, reason) VALUES (?, ?, ?)",
            (user_id, chat_id, reason)
        )
        await self.conn.commit()
    
    async def get_warns(self, user_id: int, chat_id: int) -> list:
        """Ambil semua warn user"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM warns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    
    async def clear_warns(self, user_id: int, chat_id: int):
        """Clear semua warn user"""
        await self.conn.execute(
            "DELETE FROM warns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        )
        await self.conn.commit()
    
    async def update_stats(self):
        """Update statistik pesan"""
        await self.conn.execute("""
            INSERT INTO stats (id, messages_today, messages_total, date)
            VALUES (1, 1, 1, date('now'))
            ON CONFLICT(id) DO UPDATE SET
                messages_today = messages_today + 1,
                messages_total = messages_total + 1,
                date = date('now')
        """)
        await self.conn.commit()
    
    async def get_stats(self) -> dict:
        """Ambil statistik"""
        async with self.conn.execute_fetchall(
            "SELECT * FROM stats WHERE id = 1"
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {"messages_today": 0, "messages_total": 0}
    
    async def reset_daily_stats(self):
        """Reset statistik harian"""
        await self.conn.execute("""
            UPDATE stats SET messages_today = 0 WHERE id = 1
        """)
        await self.conn.commit()
    
    async def get_all_user_ids(self) -> list:
        """Ambil semua user_id"""
        async with self.conn.execute_fetchall(
            "SELECT user_id FROM users"
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]
    
    async def get_all_group_ids(self) -> list:
        """Ambil semua chat_id grup"""
        async with self.conn.execute_fetchall(
            "SELECT chat_id FROM groups"
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]
    
    async def get_group_setting(self, chat_id: int, key: str, default=None):
        """Ambil setting grup"""
        async with self.conn.execute_fetchall(
            f"SELECT {key} FROM groups WHERE chat_id = ?", (chat_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else default
    
    async def set_group_setting(self, chat_id: int, key: str, value):
        """Set setting grup"""
        await self.conn.execute(
            f"UPDATE groups SET {key} = ? WHERE chat_id = ?", (value, chat_id)
        )
        await self.conn.commit()

db = Database()
