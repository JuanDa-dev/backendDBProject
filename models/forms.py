from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Text
from sqlalchemy.orm import relationship
from db.db import meta, engine

forms = Table('forms', meta,
                # Columns
                Column('id', String(255), primary_key=True),
                Column('name', String(255)),
                Column('date', DateTime()),
                Column('description', Text)
            )

meta.create_all(engine)