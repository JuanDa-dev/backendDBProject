from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, DateTime, Boolean
from db.db import meta, engine

attendees = Table('attendees', meta,
                Column('id', String(255), primary_key=True),
                Column('name', String(255)),
                Column('lastName', String(255)),
                Column('gender', String(255)),
                Column('email', String(255), unique=True),
                Column('role', String(255)),
                Column('birthdate', DateTime()),
                Column('city', String(255)),
                Column('cellphone', String(255)),
                Column('info', String(255)),
                Column('attended', Boolean)
            )

meta.create_all(engine)