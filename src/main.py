from src.url.url_controller import url_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core import set_up_logging , logger , setting
from src.db import engine,metadata_obj

@asynccontextmanager
async def lifespan(app:FastAPI):
    set_up_logging()
    # Only rebuild the schema in local dev. In prod ( Vercel + Neon ) this
    # would run on every cold start and WIPE the live database, so it is gated
    # behind environment == 'dev'. Prod schema is created once via a separate
    # one-time script.
    if setting.environment == 'dev':
        async with engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")
    

set_up_logging()
app=FastAPI(title=setting.Title,lifespan=lifespan)
app.include_router(url_router)
