from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Event(BaseModel):
  id: Optional[str]
  name: str
  start_date: datetime
  end_date: datetime
  location: str
  info: str
  user_id: str