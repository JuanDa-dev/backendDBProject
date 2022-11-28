from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.db import conn
from models.forms import forms
from models.events import events
from models.attendees import attendees
from models.QRCodes import qrcodes
from uuid import uuid4 as uuid
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

@data_event_routes.get('/data_events/attendees/{event_id}', tags=['dataEvents'])
def get_attendees(event_id: str):
    result = list(conn.execute(qrcodes.select().join(events).join(attendees)))
    if len(result) == 0:
        return JSONResponse(content={"message": "There aren't attendees registered"}, status_code=404)
    else:
        return result