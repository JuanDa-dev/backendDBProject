from fastapi import APIRouter
from functions.functions_jwt import write_token
from fastapi.responses import JSONResponse
from db.db import conn
from models.events import events
from uuid import uuid4 as uuid
from schemas.event import Event
from os import getenv

event_routes = APIRouter()

@event_routes.post("/create", tags=["Auth"])
def create_event(event: Event):
  event_id = str(uuid())
  new_event = {
    "id": event_id,
    "name": event.name,
    "date": event.date,
    "location": event.location,
    "info": event.info
  }

  result = list(conn.execute(events.select().filter(events.c.name==event.name).filter(events.c.date==event.date)))

  if len(result) == 0:
    conn.execute(events.insert().values(new_event))
    return conn.execute(events.select().where(events.c.id == event_id)).first()
  else:
    return JSONResponse(content={"message": "Event already exists"}, status_code=404)