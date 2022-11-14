from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String
from db.db import meta, engine

users = Table('users', meta, 
              Column('id', String(255), primary_key=True), 
              Column('name', String(255)),
              Column('password', String(255)), 
              Column('key', String(255)))

meta.create_all(engine)