from collections.abc import AsyncGenerator
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from src.core import setting,logger


engine = create_async_engine(
    url=setting.DB_URL,
    poolclass=NullPool,
    connect_args={"ssl": "require", "statement_cache_size": 0},
)

SessionCreator=async_sessionmaker(bind=engine,class_=AsyncSession,autoflush=False,autocommit=False,expire_on_commit=False)

async def ProvideSession()->AsyncGenerator[AsyncSession,None]:
    try:
        session=SessionCreator()
        yield session
    finally:
        await session.close()