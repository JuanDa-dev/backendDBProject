from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.db import conn
from models.forms import forms
from models.events import events
from models.attendees import attendees
from models.QRCodes import qrcodes
from uuid import uuid4 as uuid
from schemas.attendee import Attendee
from schemas.form import Form
from middlewares.verify_token_route import VerifyTokenRoute

data_event_routes = APIRouter(route_class=VerifyTokenRoute)

@data_event_routes.post('/data_events/createform/{event_id}', tags=['dataEvents'])
def create_form(form: Form, event_id: str):
    form_id = str(uuid())
    new_form = {
        "id": form_id,
        "name": form.name,
        "date": form.date,
        "description": form.description
    }

    # Creo el nuevo formulario
    conn.execute(forms.insert().values(new_form))
    # Actualizo el evento
    conn.execute(events.update().values(form_id=form_id).where(events.c.id == event_id))
    return conn.execute(forms.select().where(forms.c.id == form_id)).first()

@data_event_routes.post('/data_events/attendees/{event_id}', tags=['dataEvents'])
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

    qrcode_id = str(uuid())
    new_qrcode = {
        'id': qrcode_id,
        'description': attendee.qrcode_description,
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

@data_event_routes.get('/data_events/attendees/{event_id}', tags=['dataEvents'])
def get_attendees(event_id: str):
    result = list(conn.execute(qrcodes.select().join(events).join(attendees)))
    if len(result) == 0:
        return JSONResponse(content={"message": "There aren't attendees registered"}, status_code=404)
    else:
        return result