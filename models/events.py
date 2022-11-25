from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, DateTime
from db.db import meta, engine

events = Table('events', meta,
                Column('id', String(255), primary_key=True),
                Column('name', String(255)),
                Column('date', DateTime()),
                Column('location', String(255)),
                Column('info', String(255))
                )
meta.create_all(engine)