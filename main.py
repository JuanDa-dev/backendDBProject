from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from routes.auth import auth_routes
from routes.dataEvents import data_event_routes
from routes.events import event_routes
from os import getenv
import uvicorn

app = FastAPI(openapi_tags=[{"name": "Auth", "description": "Auth routes"}])

origins = [
    "https://sigae-for-all.edimarod02.repl.co",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes, prefix="/api")
app.include_router(data_event_routes, prefix="/api")
app.include_router(event_routes, prefix="/api")
load_dotenv()

if __name__ == "__main__":
  PORT = int(getenv("PORT"))
  uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)