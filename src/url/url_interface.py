from src.url.url_models import short_url_Model
from abc import abstractmethod,ABC

class URLRepositoryInterface(ABC):

    @abstractmethod
    async def create_url(self,short_url,long_url)->short_url_Model|None:
        pass

    @abstractmethod
    async def get_by_short_code(self,short_code:str)->short_url_Model|None:
        pass

    @abstractmethod
    async def get_by_long_url(self,long_url:str)->short_url_Model|None:
        pass

    @abstractmethod
    async def delete_short_code(self,short_code:str)->short_url_Model|None:
        pass
