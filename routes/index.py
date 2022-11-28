from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.db import conn
from models.events import events
from models.attendees import attendees
from models.QRCodes import qrcodes
from uuid import uuid4 as uuid
from schemas.attendee import Attendee

index_routes = APIRouter()

@index_routes.post('/data_events/attendees/{event_id}', tags=['dataEvents'])
def register_attendees(attendee: Attendee, event_id: str):
    attendee_id = str(uuid())
    new_attendee = {
        "id": attendee_id,
        "name": attendee.name,
        "lastName": attendee.lastName,
        "gender": attendee.gender,
        "email": attendee.email,
        "role": attendee.role,
        "birthdate": attendee.birthdate,
        "city": attendee.city,
        "cellphone": attendee.cellphone,
        "info": attendee.info
    }

    qrcode_id = attendee.qrcode_id
    new_qrcode = {
        'id': qrcode_id,
        'description': attendee.qrcode_description,
        'attended': False,
        'attendee_id': attendee_id,
        'event_id': event_id
    }

    result = conn.execute(attendees.select()
                                  .filter(attendees.c.name==attendee.name)
                                  .filter(attendees.c.lastName==attendee.lastName)
                                  .filter(attendees.c.email==attendee.email)).first()
    
    if result:
        result2 = conn.execute(qrcodes.select()
                                            .filter(qrcodes.c.attendee_id==result.id)
                                            .filter(qrcodes.c.event_id==event_id)).first()
        if result2:
            return JSONResponse(content={"message": "Attendee already registered"}, status_code=404)
        else:
            conn.execute(qrocodes.insert().values(new_qrcode))
            return conn.execute(qrcodes.select().where(qrcodes.c.id == qrcode_id)).first()
    else:
        conn.execute(attendees.insert().values(new_attendee))
        conn.execute(qrcodes.insert().values(new_qrcode))
        return conn.execute(qrcodes.select().where(qrcodes.c.id == qrcode_id)).first()

@index_routes.get('/data_events/event_by_form/{form_id}')
def get_event_by_form_id(form_id: str):
    return conn.execute(events.select().where(events.c.form_id==form_id)).first()

@index_routes.put('/data_events/attendees/{qrcode_id}')
def update_attendance(qrcode_id: str):
    conn.execute(qrcodes.update().values(attended=True).where(qrcodes.c.id==qrcode_id))
    return conn.execute(qrcodes.select().where(qrcodes.c.id==qrcode_id)).first()