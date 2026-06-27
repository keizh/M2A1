from src.url.url_service import URLService
from src.url.url_repository import URLRepository
from src.db.database import ProvideSession
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
def get_url_repository(db:AsyncSession=Depends(ProvideSession))->URLRepository:
    return URLRepository(db)

def get_url_service(url_repo:URLRepository=Depends(get_url_repository))->URLService:
    return URLService(url_repo)