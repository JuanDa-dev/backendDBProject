from fastapi import APIRouter
from pydantic import BaseModel # EmailStr
from middlewares.verify_token_route import VerifyTokenRoute

index_routes = APIRouter(route_class=VerifyTokenRoute)