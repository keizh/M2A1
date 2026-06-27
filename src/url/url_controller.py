from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_307_TEMPORARY_REDIRECT
from fastapi import HTTPException
from src.url.url_models import deleted_short_url_req_model,deleted_short_url_res_model
from fastapi import status
from src.url.url_dependencies import get_url_service
from fastapi import Depends
from src.core import logger
from fastapi import APIRouter 
from src.url.url_models import create_short_url_request_model,create_short_url_response_model
from fastapi.responses import RedirectResponse

url_router = APIRouter(prefix="/url",tags=["url"])

@url_router.post("/shorten",response_model=create_short_url_response_model,status_code=status.HTTP_201_CREATED)
async def create_short_url(body:create_short_url_request_model,service=Depends(get_url_service)):
    logger.info(f"Received request to shorten URL: {body}")
    return await service.create_short_code(str(body.long_url))

@url_router.delete("/",response_model=deleted_short_url_res_model,status_code=status.HTTP_200_OK)
async def del_short_url(short_code:str,service=Depends(get_url_service)):
    return await service.remove_short_url(short_code)

@url_router.get('/redirect',response_class=RedirectResponse)
async def redirectFunction(short_code:str,service=Depends(get_url_service)):
    original_url=await service.fetch_original_url(short_code)
    if original_url:
        return original_url
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No such short code is mapped to long Code")
