from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Attendee(BaseModel):
  id: Optional[str]
  name: str
  lastName: str
  gender: str
  email: str
  role: str
  birthdate: datetime
  city: str
  cellphone: str
  info: str
  qrcode_description: str