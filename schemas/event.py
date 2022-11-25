from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Event(BaseModel):
  id: Optional[str]
  name: str
  date: datetime
  location: str
  info: str