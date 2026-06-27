from typing import Optional
from pydantic import HttpUrl
from pydantic import BaseModel
from datetime import datetime


class create_short_url_request_model(BaseModel):
    long_url:HttpUrl

class create_short_url_response_model(BaseModel):
    short_url:Optional[str]=None
    long_url:Optional[HttpUrl]=None
    message:str
    status:int

class short_url_Model(BaseModel):
    id:int
    short_url:str
    long_url:HttpUrl
    # created_at:datetime
    # updated_at:datetime

    model_config={
        "from_attributes":True
    }

class deleted_short_url_res_model(BaseModel):
    message:str

class deleted_short_url_req_model(BaseModel):
    short_code:str
