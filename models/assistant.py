from enum import unique
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String
from db.db import meta, engine

assistants = Table('assistants', meta,
                Column('id', String(255), primary_key=True),
                Column('name', String(255)),
                Column('gender', String(255)),
                Column('email', String(255)),
                Column('city', String(255)),
                Column('cellphone',String(10)),
                Column('password',String(255)),
                Column('key',String(255))
                )
meta.create_all(engine)