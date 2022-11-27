from pydantic import BaseModel
from typing import Optional

class Assistant(BaseModel):
  id: Optional[str]
  name: str
  gender:str
  email:str
  city:str
  cellphone:str
  password: str
  key:str