# objective 
# 1. create and destroy on model on before and after testing 
# 2. dependency injection overload
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv('.env.test'),override=True)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine , async_sessionmaker
import pytest
from src.db import metadata_obj, ProvideSession
from src.main import app

DB_URL=os.getenv('DB_URL','')

engine=create_async_engine(DB_URL)

@pytest.fixture(autouse=True,scope="module")
async def create_destroy_models():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

@pytest.fixture(autouse=True,scope="module")
async def provide_session():
    async def sessionProvider():
        Session=async_sessionmaker(bind=engine,class_=AsyncSession,autoflush=False,expire_on_commit=False)
        async with Session() as session:
            yield session
    app.dependency_overrides[ProvideSession] = sessionProvider
    yield
    app.dependency_overrides={}
