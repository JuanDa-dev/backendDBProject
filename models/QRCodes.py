from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean
from sqlalchemy.orm import relationship
from db.db import meta, engine

qrcodes = Table('qrcodes', meta,
                # Columns
                Column('id', String(255), primary_key=True),
                Column('description', String(255)),
                Column('attended', Boolean),

                # ForeignKeys
                Column('attendee_id', ForeignKey('attendees.id')),
                Column('event_id', ForeignKey('events.id'))
            )

# relationship
relationship('events')
meta.create_all(engine)