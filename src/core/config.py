from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    DB_URL:str
    environment:Literal['dev','prod']='dev'
    Title:str
    
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding='utf-8',extra="ignore")
    

setting = Settings()