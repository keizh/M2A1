from src.url.url_interface import URLRepositoryInterface
from sqlalchemy import select , delete
from src.url.url_models import short_url_Model
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import logger
from src.db import short_url_table
from sqlalchemy.exc import DataError, IntegrityError, DatabaseError
from fastapi import HTTPException

class URLRepository(URLRepositoryInterface):
    def __init__(self,db:AsyncSession):
        self.db=db
    
    async def create_url(self,short_url,long_url)->short_url_Model|None:
        try:
            stmt=insert(short_url_table).values(short_url=short_url,long_url=long_url).returning(short_url_table)
            result = await self.db.execute(stmt)
            await self.db.commit()

            row=result.mappings().first()

            if row:
                logger.info(f'URL created successfully {row["short_url"]}',short_url=row['short_url'],long_url=row['long_url'])
                return short_url_Model.model_validate(row)
            else:
                return None
        except IntegrityError as e:
            await self.db.rollback()
            orig = getattr(e, 'orig', None)
            real = getattr(orig, '__cause__', None)        # the asyncpg UniqueViolationError
            sqlState = getattr(real, 'sqlstate', None)
            constraint_name = getattr(real, 'constraint_name', None)
            logger.error('IntegrityError in create_url', error=e, sqlState=sqlState, constraint_name=constraint_name , orig=orig)
            if constraint_name in ['unique_su_constraint']:
                raise HTTPException(status_code=500, detail="internal server error")
            elif constraint_name in ['unique_lu_constraint']:
                raise HTTPException(status_code=409, detail="longurl record already exists")
            raise HTTPException(status_code=500, detail=f"Integrity Error: constraint={constraint_name}, sqlState={sqlState}")
        except DataError as e:
            await self.db.rollback()
            logger.error('DataError in create_url', error=e)
            raise HTTPException(status_code=500, detail="DataError")
        except DatabaseError as e:
            await self.db.rollback()
            logger.error('DatabaseError in create_url', error=e)
            raise HTTPException(status_code=500, detail="DatabaseError")
        except Exception as e:
            await self.db.rollback()
            logger.error('Error creating URL',error=e,short_url=short_url,long_url=long_url)
            raise HTTPException(status_code=500, detail='Something went wrong') from e


    async def get_by_short_code(self,short_code:str)->short_url_Model|None:
        try:
            stmp=select(short_url_table).where(short_url_table.c.short_url==short_code)
            result = await self.db.execute(stmp)
            row=result.mappings().first()
            if row:
                return short_url_Model.model_validate(row)
            else:
                return None
        except Exception as e:
            logger.error('get_by_short_code',error=e)
            raise HTTPException(status_code=500, detail="Something went wrong") from e

    async def get_by_long_url(self,long_url:str)->short_url_Model|None:
        try:
            stmt=select(short_url_table).where(short_url_table.c.long_url == long_url)
            result = await self.db.execute(stmt)
            row = result.mappings().first()

            if row:
                return short_url_Model.model_validate(row)
            else:
                return None        
        except Exception as e:
            logger.error('get_by_long_url',error=e)
            raise HTTPException(status_code=500, detail='Something went wrong') from e

    async def delete_short_code(self,short_code:str)->short_url_Model|None:
        try:
            stmt=delete(short_url_table).where(short_url_table.c.short_url == short_code).returning(short_url_table)
            result=await self.db.execute(stmt)
            await self.db.commit()

            row = result.mappings().first()

            if row:
                return short_url_Model.model_validate(row)
            else:
                return None
        except Exception as e:
            await self.db.rollback()
            logger.error('delete_short_code', short_code=short_code, error=e)
            raise HTTPException(status_code=500, detail='Something went wrong') from e
            