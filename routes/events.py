from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.db import conn
from models.users import users
from models.forms import forms
from models.events import events
from uuid import uuid4 as uuid
from schemas.event import Event
from schemas.user import User
from middlewares.verify_token_route import VerifyTokenRoute

event_routes = APIRouter(route_class=VerifyTokenRoute)

@event_routes.post("/events/create", tags=["events"])
def create_event(event: Event):
  event_id = str(uuid())
  new_event = {
    "id": event_id,
    "name": event.name,
    "start_date": event.start_date,
    "end_date": event.end_date,
    "location": event.location,
    "info": event.info,
    "user_id": event.user_id
  }

  result = list(conn.execute(events.select()
                                  .filter(events.c.name==event.name)
                                  .filter(events.c.location==event.location)
                                  .filter(events.c.start_date>=event.start_date)
                                  .filter(events.c.end_date<=event.end_date)))

  if len(result) == 0:
    conn.execute(events.insert().values(new_event))
    return conn.execute(events.select().where(events.c.id == event_id)).first()
  else:
    return JSONResponse(content={"message": "Event already exists"}, status_code=404)

@event_routes.get('/events/get_one/{event_id}', tags=["events"])
def get_event(event_id: str):
  result = conn.execute(events.select().join(users).join(forms).filter(events.c.id == event_id)).first()
  if result:
    return result
  else:
    return JSONResponse(content={"message": "The event does not exist"}, status_code=404)

@event_routes.get('/events/get_all', tags=["events"])
def get_all_events(user: User):
  result = list(conn.execute(events.select()
                                  .join(users)
                                  .filter(users.c.name == user.name)))
  if len(result) > 0:
    return result
  else:
    return JSONResponse(content={"message": "You don't have events created"}, status_code=404)

@event_routes.delete('/events/delete/{event_id}', tags=["events"])
def delete_event(event_id: str):
  conn.execute(events.delete().where(events.c.id == event_id))
  result = conn.execute(events.select().where(events.c.id == event_id)).first()
  if result:
    return JSONResponse(content={"message": "Event not deleted"}, status_code=404)
  else:
    return "Event deleted successfully"