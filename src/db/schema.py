from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import MetaData
from sqlalchemy import Table , Column, Integer

metadata_obj=MetaData()

short_url_table=Table(
    "short_url",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("short_url",String(10),nullable=False),
    Column("long_url",Text,nullable=False),
    Column("created_at",Date,default=func.now()),
    Column("updated_at",Date,default=func.now()),
    UniqueConstraint('short_url',name="unique_su_constraint"),
    UniqueConstraint('long_url',name="unique_lu_constraint")
)

