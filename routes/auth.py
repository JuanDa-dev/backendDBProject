from fastapi import APIRouter
from functions.functions_jwt import write_token
from fastapi.responses import JSONResponse
from db.db import conn
from models.users import users
from cryptography.fernet import Fernet
from uuid import uuid4 as uuid
from schemas.user import User
from os import getenv

auth_routes = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)
ENCODING = getenv('ENCODING')

@auth_routes.post("/register", tags=["Auth"])
def register(user: User):
  user_id = str(uuid())
  new_user = {
    "id": user_id,
    "name": user.name,
    "password": str(f.encrypt(user.password.encode(ENCODING)), ENCODING),
    "key": str(key, ENCODING)
  }

  result = list(conn.execute(users.select().where(users.c.name == user.name)))

  if len(result) == 0:
    conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == user_id)).first()
  else:
    return JSONResponse(content={"message": "Username already exists"}, status_code=404)

@auth_routes.post("/login", tags=["Auth"])
def login(user: User):
  db_user = conn.execute(users.select().where(users.c.name == user.name)).first()
  if db_user:
    f = Fernet(bytes(db_user.key, ENCODING))
    if user.password == str(f.decrypt(bytes(db_user.password, ENCODING)), ENCODING):
      user.id = db_user.id
      return write_token(user.dict())
    else:
      return JSONResponse(content={"message": "Password incorrect" }, status_code=404)
  else:
    return JSONResponse(content={"message": "User not found"}, status_code=404)