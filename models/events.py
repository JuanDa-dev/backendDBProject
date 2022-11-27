from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime
from sqlalchemy.orm import relationship
from db.db import meta, engine

events = Table('events', meta,
                # Columns                
                Column('id', String(255), primary_key=True),
                Column('name', String(255)),
                Column('start_date', DateTime()),
                Column('end_date', DateTime()),
                Column('location', String(255)),
                Column('info', String(255)),
                
                # ForeignKeys
                Column('form_id', ForeignKey('forms.id')),
                Column('user_id', ForeignKey('users.id'))
            )

# Relationships
relationship('forms'),
relationship('users')
meta.create_all(engine)