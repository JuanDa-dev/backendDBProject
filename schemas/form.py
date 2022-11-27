from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Form(BaseModel):
  id: Optional[str]
  name: str
  date: datetime
  description: str