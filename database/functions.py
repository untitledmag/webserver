import aiosqlite
import asyncio

db_path = 'database/storage.db'

async def is_auth_in_db(token: str):
    async with aiosqlite.connect(db_path) as db:
        # Fixed table name to 'authentication' to match create_tables
        async with db.execute('SELECT 1 FROM authentication WHERE token = ?', (token,)) as cursor:
            result = await cursor.fetchone()
            return result is not None

async def store_auth_token(token: str):
    async with aiosqlite.connect(db_path) as db:
        # Fixed syntax to 'INSERT OR REPLACE'
        await db.execute('INSERT OR REPLACE INTO authentication (token) VALUES (?)', (token,))
        await db.commit()

async def create_tables():
    import os
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS authentication (token TEXT PRIMARY KEY)"
        )
        await db.commit()
        
async def delete_auth_token(token:str):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM authentications WHERE token = ?', (token,))
        await db.commit()

async def main():
    await create_tables()

asyncio.run(main())