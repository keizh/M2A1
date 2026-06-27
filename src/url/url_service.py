from fastapi import status
from fastapi import HTTPException
from src.url.url_repository import URLRepository
import string
import secrets
from src.core import setting

class URLService():
    def __init__(self,url_repo:URLRepository):
        self.url_repo=url_repo
    
    def __generate_short_code(self)->str:
        alphabet = string.ascii_letters + string.digits
        short_code = ''.join(secrets.choice(alphabet) for i in range(10))
        # return short_code
        if setting.environment == 'test':
            return 'krishna123'
        return short_code
        
    async def create_short_code(self,long_url):
        short_code=self.__generate_short_code()
        data_record=await self.url_repo.create_url(short_code,long_url)
        if data_record:
            return { "message":"short url successfully created", 
                    "short_url": data_record.short_url,
                    "long_url": data_record.long_url,
                     "status":200 }
        else:
              raise HTTPException(status_code=500, detail="Failed to create create_short_code")
        
    
    async def fetch_original_url(self, short_code: str) -> str | None:
        res=await self.url_repo.get_by_short_code(short_code)
        if res:
            return res.long_url
        return None

    async def fetch_short_url(self, long_code: str) -> dict | None:
        res=await self.url_repo.get_by_long_url(long_code)
        if res:
            return res.short_url
        return None

    async def remove_short_url(self, short_code: str) -> dict:
        res = await self.url_repo.delete_short_code(short_code)
        if res:
            return {"message":"short_code succesfully deleted",
                    "status_code":200}
        else:
            raise HTTPException(status_code=404,detail='No such short code exists')
