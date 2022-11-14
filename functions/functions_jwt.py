from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse

SECRET_KEY = getenv('SECRET_KEY')
EXPIRE_DATE = int(getenv('EXPIRE_DATE'))
ALGORITHM = getenv('ALGORITHM')

def expire_date(days: int):
  date = datetime.now()
  new_date = date + timedelta(days)

  return new_date

def write_token(data: dict):
  token = encode(payload={**data, "exp": expire_date(EXPIRE_DATE)}, key=SECRET_KEY, algorithm=ALGORITHM)
  data['token'] = token

  return data

def validate_token(token, output=False):
  try:
    response = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    if output:
      return response
  except exceptions.DecodeError:
    return JSONResponse(content={"message": "Invalid token"}, status_code=401)
  except exceptions.ExpiredSignatureError:
    return JSONResponse(content={"message": "Token expired"}, status_code=401)