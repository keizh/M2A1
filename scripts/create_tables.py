import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.logger import logger, set_up_logging
from src.db.database import engine
from src.db.schema import metadata_obj


async def create_tables() -> None:
    set_up_logging()
    logger.info("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)
    logger.info("Tables created successfully.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
