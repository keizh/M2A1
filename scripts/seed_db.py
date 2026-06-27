import asyncio
import io
import random
import string
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.db.database import engine
from src.core.logger import logger

TOTAL_ROWS = 1_000_000
CHUNK_SIZE = 100_000

def generate_chunk_csv(chunk_size: int) -> io.BytesIO:
    """
    Generates fake data and formats it as a CSV inside a temporary RAM buffer.
    """
    buffer = io.BytesIO()

    characters = string.ascii_letters + string.digits
    now = date.today().isoformat()

    for _ in range(chunk_size):
        short_code = ''.join(random.choices(characters, k=8))
        original_url = f"https://example.com/data/{short_code}"

        buffer.write(f"{short_code},{original_url},{now},{now}\n".encode())

    buffer.seek(0)
    return buffer

async def seed_database():
    logger.info("Starting high-speed data ingestion...", total_rows=TOTAL_ROWS)
    start_time = time.time()
    
    async with engine.connect() as conn:
        raw_conn = await conn.get_raw_connection()
        asyncpg_conn = raw_conn.driver_connection
        
        chunks = TOTAL_ROWS // CHUNK_SIZE
        
        for i in range(chunks):
            chunk_start_time = time.time()
            
            csv_buffer = generate_chunk_csv(CHUNK_SIZE)
            
            await asyncpg_conn.copy_to_table(
                'short_url',
                source=csv_buffer,
                columns=['short_url', 'long_url', 'created_at', 'updated_at'],
                format='csv'
            )
            
  
            csv_buffer.close()
            
            await conn.commit()
            
            chunk_duration = time.time() - chunk_start_time
            logger.info(
                f"Chunk {i + 1}/{chunks} inserted", 
                rows=CHUNK_SIZE, 
                duration_seconds=round(chunk_duration, 2)
            )

    total_time = time.time() - start_time
    logger.info("Database seeding complete!", total_time_seconds=round(total_time, 2))

if __name__ == "__main__":
    asyncio.run(seed_database())