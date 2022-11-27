from fastapi import APIRouter
from functions.functions_jwt import write_token
from fastapi.responses import JSONResponse
from db.db import conn
from models.assistant import assistants
from cryptography.fernet import Fernet
from uuid import uuid4 as uuid
from schemas.assistan import Assistant
from schemas.user import User
from os import getenv

assistant_routes = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)
ENCODING = getenv('ENCODING')

@assistant_routes.post("/registerAssistant", tags=["Auth"])
def register(assistant: Assistant):
  assistant_id = str(uuid())
  new_assistant = {
    "id": assistant_id,
    "name": assistant.name,
    "gender":assistant.gender,
    "email":assistant.email,
    "city":assistant.city,
    "cellphone":assistant.cellphone,
    "password": str(f.encrypt(assistant.password.encode(ENCODING)), ENCODING),
    "key": str(key, ENCODING)
  }

  result = list(conn.execute(assistants.select().where(assistants.c.name == assistant.name)))

  if len(result) == 0:
    conn.execute(assistants.insert().values(new_assistant))
    return conn.execute(assistants.select().where(assistants.c.id == assistant_id)).first()
  else:
    return JSONResponse(content={"message": "Assistant already exists"}, status_code=404)

@assistant_routes.post("/loginAssistant", tags=["Auth"])
def login(assistant: Assistant):
  db_user = conn.execute(assistants.select().where(assistants.c.name == assistant.name)).first()
  if db_user:
    f = Fernet(bytes(db_user.key, ENCODING))
    if assistant.password == str(f.decrypt(db_user.password), ENCODING):
      assistant.id = db_user.id
      assistant.password = db_user.password
      return write_token(assistant.dict())
    else:
      return JSONResponse(content={"message": "Password incorrect" }, status_code=404)
  else:
    return JSONResponse(content={"message": "Assistant not found"}, status_code=404)